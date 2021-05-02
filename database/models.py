import enum
from collections import defaultdict
from typing import Optional, List, Dict, Sequence

from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint, ForeignKey, or_, JSON
from sqlalchemy.orm import Session, relationship, backref

from api.schemas.competitor import CompetitorCreate, CompetitorUpdate
from api.schemas.security import UserCreate
from api.schemas.stage import StageCreate
from api.schemas.tournament import TournamentCreate, TournamentUpdate
from database.db import Base
from lib.status_updaters import TournamentStatusUpdater


class TournamentError(Exception):
    pass


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    tournaments = relationship('Tournament', back_populates='owner')

    @staticmethod
    def by_id(user_id: int, db: Session):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def by_email(email: str, db: Session):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(user: UserCreate, db: Session):
        # This assumes that the password is already hashed
        db_user = User(email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()


class Tournament(Base):
    __tablename__ = 'tournament'

    class TournamentStatus(enum.IntEnum):
        PENDING = 0
        READY = 1
        ACTIVE = 2
        COMPLETE = 3

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=False)
    status = Column(Integer, default=TournamentStatus.PENDING, nullable=False)
    public = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    owner = relationship('User', back_populates='tournaments')

    competitors = relationship('Competitor', back_populates='tournament', cascade='all, delete', passive_deletes=True)
    stages: Sequence['Stage'] = relationship('Stage', back_populates='tournament', cascade='all, delete, delete-orphan',
                                             passive_deletes=True, order_by='Stage.ordinal')

    status_options = list(map(int, TournamentStatus))

    __table_args__ = (
        CheckConstraint(f'status IN ({",".join(map(str, status_options))})', name='valid_status'),
    )

    @staticmethod
    def create(tournament: TournamentCreate, user: User, db: Session):
        db_tournament = Tournament(
            name=tournament.name,
            organization=tournament.organization,
            start_date=tournament.start_date,
            public=tournament.public,
            owner_id=user.id,
        )
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
        return db_tournament

    @staticmethod
    def by_id_visible(tournament_id: int, user: User, db: Session):
        query = db.query(Tournament).filter(Tournament.id == tournament_id)

        if user:
            # Only allow tournaments the current user can see
            query = query.filter(or_(
                Tournament.public.is_(True),
                Tournament.owner_id == user.id,
            ))
        else:
            query = query.filter(Tournament.public.is_(True))

        return query.first()

    @staticmethod
    def get_all_visible(user: User, db: Session, is_filtered_by_user: bool = False, skip: int = 0, limit: int = 100):
        query = db.query(Tournament)

        if user:
            if is_filtered_by_user:
                # Only this users tournaments
                query = query.filter(Tournament.owner_id == user.id)
            else:
                # All public or owned by this user
                query = query.filter(or_(
                    Tournament.public.is_(True),
                    Tournament.owner_id == user.id,
                ))
        else:
            query = query.filter(Tournament.public.is_(True))

        # Newest tournaments first
        query = query.order_by(Tournament.start_date.desc())

        # Apply the paging
        return query.offset(skip).limit(limit).all()

    def change_status(self, status: int, db: Session):
        TournamentStatusUpdater.update_status(self, status, db)
        db.commit()
        db.refresh(self)

    def update(self, tournament: TournamentUpdate, db: Session):
        self.name = tournament.name
        self.organization = tournament.organization
        self.start_date = tournament.start_date
        self.public = tournament.public

        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self, db: Session):
        db.delete(self)
        db.commit()

    def delete_stages(self, db: Session, autocommit=True):
        # The delete-orphan cascade setting on the stages relationship lets us just do this
        self.stages = []
        if autocommit:
            db.commit()

    def delete_competitors(self, db: Session, autocommit=True):
        for competitor in self.competitors:
            competitor.delete(db=db, autocommit=False)

        if autocommit:
            db.commit()

    def get_last_stage(self):
        """
        Gets the last stage, if any exist
        """
        return self.stages[-1] if self.stages else None

    def progress(self, db: Session, autocommit=True):
        """
        Find the current active stage, if any.
        If no active stage, start the first stage and generate matches.
        If active stage, make sure all of its matches are complete.
            If complete, close the stage and start the next one.
                If current stage is the last stage, close out the tournament.
            If not complete, raise error.
        """
        stage_to_start = None
        if self.status == Tournament.TournamentStatus.READY:
            # The tournament has not yet started, so start it and generate matches for the first stage
            stage_to_start = self.stages[0]
            self.status = Tournament.TournamentStatus.ACTIVE
            db.add(self)
        elif self.status == Tournament.TournamentStatus.ACTIVE:
            # The tournament is already active, so ensure the current stage is complete before moving to the next one
            active_stages = [stage for stage in self.stages if stage.status == Stage.StageStatus.ACTIVE]

            if len(active_stages) != 1:
                raise TournamentError(f'Unexpected number of stages are currently active: {len(active_stages)}')

            current_stage = active_stages[0]
            current_stage.progress(db, autocommit=False)

            # Grab the first stage in status pending, it's the next one to start
            pending_stages = [stage for stage in self.stages if stage.status == Stage.StageStatus.PENDING]
            if len(pending_stages):
                stage_to_start = pending_stages[0]
        else:
            raise TournamentError(f'A tournament with status {self.status} cannot be progressed')

        # The next stage needs to be started
        if stage_to_start:
            stage_to_start.progress(db, autocommit=False)
        else:
            # If there's no stage to start, the tournament is complete
            self.status = Tournament.TournamentStatus.COMPLETE
            db.add(self)

        if autocommit:
            db.commit()
            db.refresh(self)


class Competitor(Base):
    __tablename__ = 'competitor'

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id', ondelete='CASCADE'), nullable=False)
    tournament = relationship('Tournament', back_populates='competitors')
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    location = Column(String, nullable=True)

    __table_args__ = (
        # All competitors must have at least a last name (individual) or an organization (team)
        CheckConstraint('last_name IS NOT NULL OR organization IS NOT NULL'),
    )

    @staticmethod
    def create(tournament: Tournament, competitor: CompetitorCreate, db: Session):
        db_competitor = Competitor(
            tournament_id=tournament.id,
            first_name=competitor.first_name,
            last_name=competitor.last_name,
            organization=competitor.organization,
            location=competitor.location,
        )
        db.add(db_competitor)
        db.commit()
        db.refresh(db_competitor)
        return db_competitor

    @staticmethod
    def create_batch(tournament: Tournament, competitors: List[CompetitorCreate], db: Session, autocommit=True):
        batch = []
        for competitor in competitors:
            batch.append(Competitor(
                tournament_id=tournament.id,
                first_name=competitor.first_name,
                last_name=competitor.last_name,
                organization=competitor.organization,
                location=competitor.location,
            ))
        # No need to refresh after this since it doesn't associate the objects to the session
        db.bulk_save_objects(batch, return_defaults=True)

        if autocommit:
            db.commit()

        return batch

    @staticmethod
    def by_id(competitor_id: int, db: Session):
        return db.query(Competitor).filter(Competitor.id == competitor_id).first()

    def update(self, competitor: CompetitorUpdate, db: Session):
        self.first_name = competitor.first_name
        self.last_name = competitor.last_name
        self.organization = competitor.organization
        self.location = competitor.location

        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self, db: Session, autocommit=True):
        db.delete(self)

        if autocommit:
            db.commit()


class Stage(Base):
    __tablename__ = 'stage'

    class StageType(enum.IntEnum):
        POOL = 0
        BRACKET_SINGLE_ELIMINATION = 1
        BRACKET_DOUBLE_ELIMINATION = 2

        @classmethod
        def is_valid_stage_ordering(cls, first, second):
            """
            Defines which type of stages can occur in sequence. Maps stage type -> all valid stage types that can follow
            it.
            """
            valid_orders = defaultdict(set)
            valid_orders[cls.POOL] = {cls.POOL, cls.BRACKET_SINGLE_ELIMINATION, cls.BRACKET_DOUBLE_ELIMINATION}

            return second in valid_orders[first]

        @classmethod
        def parse_params(cls, stage_type, params) -> Dict:
            parsed_params = {}

            if stage_type == cls.POOL:
                parsed_params['minimum_pool_size'] = int(params.get('minimum_pool_size', 0))
            else:
                parsed_params['seeded'] = bool(params.get('seeded', False))

            return parsed_params

    class StageStatus(enum.IntEnum):
        PENDING = 0
        ACTIVE = 1
        COMPLETE = 2

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id', ondelete='CASCADE'), nullable=False)
    tournament = relationship('Tournament', back_populates='stages')
    ordinal = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=StageStatus.PENDING)
    params = Column(JSON, nullable=False)

    pools = relationship('Pool', back_populates='stage', cascade='all, delete', passive_deletes=True,
                         order_by='Pool.ordinal')

    type_options = list(map(int, StageType))
    status_options = list(map(int, StageStatus))

    __table_args__ = (
        CheckConstraint(f'type IN ({",".join(map(str, type_options))})', name='valid_type'),
        CheckConstraint(f'status IN ({",".join(map(str, status_options))})', name='valid_status'),
    )

    @property
    def parsed_params(self):
        return Stage.StageType.parse_params(self.type, self.params)

    @staticmethod
    def create(tournament: Tournament, stage: StageCreate, db: Session, autocommit=True):
        # Make sure the requested stage type is compatible with the existing stages
        most_recent_stage: Optional[Stage] = tournament.get_last_stage()
        most_recent_stage_type: Optional[Stage.StageType] = Stage.StageType(most_recent_stage.type) \
            if most_recent_stage else None
        next_stage_type: Stage.StageType = Stage.StageType(stage.type)

        if most_recent_stage_type is not None and not Stage.StageType.is_valid_stage_ordering(
                most_recent_stage_type,
                next_stage_type,
        ):
            raise ValueError(f'Stages of type {stage.type} cannot follow stages of type {next_stage_type}')

        db_stage = Stage(
            tournament_id=tournament.id,
            ordinal=len(tournament.stages),
            type=stage.type,
            params=stage.params,
        )
        db.add(db_stage)

        if autocommit:
            db.commit()
            db.refresh(db_stage)
        return db_stage

    @staticmethod
    def by_id(stage_id: int, db: Session):
        return db.query(Stage).filter(Stage.id == stage_id).first()

    def update(self, stage: StageCreate, db: Session, autocommit: bool = True):
        self.type = stage.type
        self.params = stage.params

        db.add(self)
        if autocommit:
            db.commit()
            db.refresh(self)

    def delete(self, validate_ordinal: bool = True, db: Session = None, autocommit=True):
        # Make sure this is the final stage
        if validate_ordinal and self != self.tournament.get_last_stage():
            raise ValueError(f'Stage {self.id} is not the last stage of tournament {self.tournament_id}')

        db.delete(self)

        if autocommit:
            db.commit()

    def all_matches_complete(self):
        """
        If there's a single match for this stage that isn't in status complete, return False, otherwise True
        """
        num_matches = len([match for pool in self.pools for match in pool.matches])
        if num_matches == 0:
            raise TournamentError('Matches have not been generated yet for this stage')

        incomplete_matches = [
            match
            for pool in self.pools
            for match in pool.matches
            if match.status != Match.MatchStatus.COMPLETE
        ]
        return len(incomplete_matches) == 0

    def progress(self, db: Session, autocommit=True):
        """
        If status is pending, generate matches and update status to active
        If status is active, make sure all matches are complete and update status to complete
        Otherwise, raise TournamentError
        """
        if self.status == Stage.StageStatus.PENDING:
            # Generate pools and matches and update the status to active
            self._generate_pools_and_matches(db, autocommit=False)
            self.status = Stage.StageStatus.ACTIVE
        elif self.status == Stage.StageStatus.ACTIVE:
            # If all matches are complete, update status to complete, otherwise raise an error
            if self.all_matches_complete():
                self.status = Stage.StageStatus.COMPLETE
            else:
                raise TournamentError('Cannot complete current stage; it still has pending matches')
        else:
            raise TournamentError(f'Cannot progress a stage that is already complete')

        db.add(self)

        if autocommit:
            db.commit()

    def _generate_pools_and_matches(self, db: Session, autocommit=True):
        from lib.match_generators.match_generator import MatchGenerator
        try:
            match_generator = MatchGenerator.get_match_generator(self)
            match_generator.generate_matches(db, autocommit=False)
        except ValueError as e:
            raise TournamentError(e)
        else:
            if autocommit:
                db.commit()


class Pool(Base):
    __tablename__ = 'pool'

    id = Column(Integer, primary_key=True, index=True)
    ordinal = Column(Integer, nullable=False)
    stage_id = Column(Integer, ForeignKey('stage.id', ondelete='CASCADE'), nullable=False)
    stage = relationship('Stage', back_populates='pools')

    matches = relationship('Match', back_populates='pool', cascade='all, delete', passive_deletes=True,
                           order_by='Match.ordinal')


class Match(Base):
    __tablename__ = 'match'

    class MatchStatus(enum.IntEnum):
        PENDING = 0
        ACTIVE = 1
        COMPLETE = 2

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey('pool.id', ondelete='CASCADE'), nullable=False)
    pool = relationship('Pool', back_populates='matches')
    ordinal = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=MatchStatus.PENDING)

    # The competitors could be populated at creation, or after the feeder matches complete
    competitor_1_id = Column(Integer, ForeignKey('competitor.id'), nullable=True)
    competitor_1 = relationship('Competitor', primaryjoin='Competitor.id==Match.competitor_1_id')
    competitor_1_score = Column(Integer, nullable=True)
    competitor_2_id = Column(Integer, ForeignKey('competitor.id'), nullable=True)
    competitor_2 = relationship('Competitor', primaryjoin='Competitor.id==Match.competitor_2_id')
    competitor_2_score = Column(Integer, nullable=True)

    # A match can point to another match so that when this match finishes, the winner populates a competitor slot on
    # the next match. Which competitor slot is populated depends on the
    next_match_id = Column(Integer, ForeignKey('match.id'), nullable=True)
    feeder_matches = relationship('Match', backref=backref('next_match', remote_side=[id]))
    next_match_competitor_slot = Column(Integer, nullable=True)

    status_options = list(map(int, MatchStatus))

    __table_args__ = (
        CheckConstraint(f'status IN ({",".join(map(str, status_options))})', name='valid_status'),
    )
