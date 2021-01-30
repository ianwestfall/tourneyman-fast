import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint, ForeignKey, or_
from sqlalchemy.orm import Session, relationship

from api.schemas.security import UserCreate
from api.schemas.tournament import TournamentCreate, TournamentUpdate
from database.db import Base


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
        pending = 0
        ready = 1
        active = 2
        complete = 3

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=False)
    status = Column(Integer, default=TournamentStatus.pending, nullable=False)
    public = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    owner = relationship('User', back_populates='tournaments')

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
