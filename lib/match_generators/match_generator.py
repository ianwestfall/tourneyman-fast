import itertools
from abc import ABC, abstractmethod
from math import floor
from random import shuffle
from typing import List

from database.db import Session
from database.models import Stage, Competitor, Pool, Match


class MatchGenerator(ABC):
    def __init__(self, stage: Stage):
        self._stage = stage
        self._match_ordinal = 0

        if self._stage.status != Stage.StageStatus.PENDING:
            raise ValueError('Only stages in status = pending are allowed')

    @staticmethod
    def get_match_generator(stage: Stage):
        """
        Returns an instance of the appropriate MatchGenerator sub-type for the given stage.
        """
        if stage.type == Stage.StageType.POOL:
            return PoolMatchGenerator(stage)
        elif stage.type == Stage.StageType.BRACKET_SINGLE_ELIMINATION:
            return SingleEliminationBracketMatchGenerator(stage)
        elif stage.type == Stage.StageType.BRACKET_DOUBLE_ELIMINATION:
            return DoubleEliminationBracketMatchGenerator(stage)
        else:
            raise ValueError(f'No match generator configured for type {stage.type}')

    def next_match_ordinal(self):
        self._match_ordinal += 1
        return self._match_ordinal - 1

    @abstractmethod
    def generate_matches(self, db: Session, autocommit=True):
        raise NotImplementedError()


class PoolMatchGenerator(MatchGenerator):
    def generate_matches(self, db: Session, autocommit=True):
        # Grab the config values
        minimum_pool_size: int = self._stage.parsed_params['minimum_pool_size']
        if minimum_pool_size > len(self._stage.tournament.competitors):
            # There's not enough competitors for even a single pool
            raise ValueError('There are not enough competitors for even a single pool')
        if minimum_pool_size == 0:
            raise ValueError('Cannot have a pool size of 0')

        # Copy the competitors list so we don't muck up the ORM list
        competitors: List[Competitor] = [competitor for competitor in self._stage.tournament.competitors]
        # Randomize the order so we get randomized pools
        shuffle(competitors)

        # Determine how many pools are necessary
        num_pools = floor(len(competitors) / minimum_pool_size)

        for i in range(num_pools):
            # Create a new pool
            pool = Pool(stage=self._stage, ordinal=i)

            # Use the pool's ordinal value to grab its competitors
            pool_competitors = [competitor
                                for idx, competitor in enumerate(competitors)
                                if idx % num_pools == pool.ordinal]

            # Generate matches for the pool
            matches = self._generate_matches_for_pool(pool, pool_competitors)

            # Add the pool and matches to the DB
            db.add(pool)
            for match in matches:
                db.add(match)

        if autocommit:
            db.commit()

    def _generate_matches_for_pool(self, pool: Pool, competitors: List[Competitor]) -> List[Match]:
        """
        Given the pool, generate and return a list of matches. Each competitor should face each other competitor.
        :param pool: the Pool to contain the matches
        :param competitors: the Competitors included in the pool
        :return: a list of generated matches for the given pool and competitors list
        """
        # Generate all the possible pairings, then filter out pairings where a competitor faces itself, and duplicates
        pairings = itertools.product(competitors, competitors)
        pairings = {
            (c1, c2) if c1.id < c2.id else (c2, c1)
            for c1, c2 in pairings
            if c1 != c2
        }

        matches = []
        for pairing in pairings:
            matches.append(Match(
                pool=pool,
                ordinal=self.next_match_ordinal(),
                competitor_1=pairing[0],
                competitor_2=pairing[1],
            ))

        # Randomize the match order to reduce the number of 'double headers'
        shuffle(matches)  # TODO: There's probably an optimal way to do this

        return matches


class SingleEliminationBracketMatchGenerator(MatchGenerator):
    def generate_matches(self, db: Session, autocommit=True):
        raise NotImplementedError()


class DoubleEliminationBracketMatchGenerator(MatchGenerator):
    def generate_matches(self, db: Session, autocommit=True):
        raise NotImplementedError()
