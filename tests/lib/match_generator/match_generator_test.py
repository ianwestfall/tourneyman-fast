import itertools
from typing import Sequence, Tuple, Set

import pytest

from database.models import Stage, Competitor, Pool, Match
from lib.match_generators.match_generator import PoolMatchGenerator, MatchGenerator, \
    SingleEliminationBracketMatchGenerator, DoubleEliminationBracketMatchGenerator
from tests.factories import StageFactory, CompetitorFactory
from tests.utils import DatabaseAwareTest


# noinspection PyMethodMayBeStatic
class TestMatchGenerator(DatabaseAwareTest):
    def test_get_match_generator_invalid_stage_type_raises_error(self, db):
        stage: Stage = StageFactory()
        stage.type = -1
        with pytest.raises(ValueError):
            MatchGenerator.get_match_generator(stage)

    def test_get_match_generator_pool_stage_type_returns_correctly(self, db):
        stage: Stage = StageFactory(type=Stage.StageType.POOL)
        mg = MatchGenerator.get_match_generator(stage)
        assert isinstance(mg, PoolMatchGenerator)

    def test_get_match_generator_single_bracket_stage_type_returns_correctly(self, db):
        stage: Stage = StageFactory(type=Stage.StageType.BRACKET_SINGLE_ELIMINATION)
        mg = MatchGenerator.get_match_generator(stage)
        assert isinstance(mg, SingleEliminationBracketMatchGenerator)

    def test_get_match_generator_double_bracket_stage_type_returns_correctly(self, db):
        stage: Stage = StageFactory(type=Stage.StageType.BRACKET_DOUBLE_ELIMINATION)
        mg = MatchGenerator.get_match_generator(stage)
        assert isinstance(mg, DoubleEliminationBracketMatchGenerator)


# noinspection PyMethodMayBeStatic
class TestPoolMatchGenerator(DatabaseAwareTest):
    def test_non_pending_stages_raise_errors(self, db):
        stage: Stage = StageFactory(status=Stage.StageStatus.ACTIVE)
        CompetitorFactory.create_batch(10, tournament=stage.tournament)

        with pytest.raises(ValueError):
            PoolMatchGenerator(stage)

        # Make sure no pools or matches were created
        assert len(db.query(Pool).all()) == 0
        assert len(db.query(Match).all()) == 0

    def test_enough_competitors_for_one_pool(self, db):
        stage: Stage = StageFactory()
        competitors: Sequence[Competitor] = CompetitorFactory.create_batch(5, tournament=stage.tournament)

        pmg = PoolMatchGenerator(stage)
        pmg.generate_matches(db, autocommit=True)

        # Make sure one pool was created with 10 matches, one for each combination of competitors
        assert len(stage.pools) == 1
        assert stage.pools[0].ordinal == 0

        expected_competitor_id_pairs = self._generate_match_combinations(competitors)
        assert len(stage.pools[0].matches) == len(expected_competitor_id_pairs)

        actual_competitor_id_pairs = self._get_competitor_id_pairs(stage.pools[0])
        assert actual_competitor_id_pairs == expected_competitor_id_pairs

        # Make sure the ordinals are an in order range from 0 to num matches
        actual_ordinals = [match.ordinal for match in stage.pools[0].matches]
        assert actual_ordinals == list(range(len(stage.pools[0].matches)))

    def _generate_match_combinations(self, competitors: Sequence[Competitor]) -> Set[Tuple[int, int]]:
        return {
            (c1.id, c2.id) if c1.id < c2.id else (c2.id, c1.id)
            for c1, c2 in itertools.product(competitors, competitors)
            if c1 != c2
        }

    def _get_competitor_id_pairs(self, pool: Pool) -> Set[Tuple[int, int]]:
        return {
            (match.competitor_1_id, match.competitor_2_id)
            if match.competitor_1_id < match.competitor_2_id else (match.competitor_2_id, match.competitor_1_id)
            for match in pool.matches
        }

    def test_enough_competitors_for_many_pools(self, db):
        stage: Stage = StageFactory()
        CompetitorFactory.create_batch(17, tournament=stage.tournament)

        pmg = PoolMatchGenerator(stage)
        pmg.generate_matches(db, autocommit=True)

        # Make sure three pools were created, with 6, 6, and 5 competitors, respectively
        assert len(stage.pools) == 3

        def verify_matches(pool: Pool, expected_num_competitors: int):
            p_competitors = set()
            for m in pool.matches:
                p_competitors.add(m.competitor_1)
                p_competitors.add(m.competitor_2)
            assert len(p_competitors) == expected_num_competitors
            expected_competitor_id_pairs = self._generate_match_combinations(list(p_competitors))
            assert len(pool.matches) == len(expected_competitor_id_pairs)
            actual_competitor_id_pairs = self._get_competitor_id_pairs(pool)
            assert actual_competitor_id_pairs == expected_competitor_id_pairs

        assert stage.pools[0].ordinal == 0
        verify_matches(stage.pools[0], 6)

        assert stage.pools[1].ordinal == 1
        verify_matches(stage.pools[1], 6)

        assert stage.pools[2].ordinal == 2
        verify_matches(stage.pools[2], 5)

        # Verify that the ordinals are an in order range from 0 to num matches
        actual_ordinals = [match.ordinal for pool in stage.pools for match in pool.matches]
        assert actual_ordinals == list(range(40))

    def test_invalid_configuration_raises_error(self, db):
        stage: Stage = StageFactory(params={})
        CompetitorFactory.create_batch(3, tournament=stage.tournament)

        pmg = PoolMatchGenerator(stage)
        with pytest.raises(ValueError):
            pmg.generate_matches(db, autocommit=True)

        # Make sure no pools or matches were created
        assert len(db.query(Pool).all()) == 0
        assert len(db.query(Match).all()) == 0

    def test_too_few_competitors_for_minimum_pool_size_raises_error(self, db):
        stage: Stage = StageFactory()
        CompetitorFactory.create_batch(3, tournament=stage.tournament)

        pmg = PoolMatchGenerator(stage)
        with pytest.raises(ValueError):
            pmg.generate_matches(db, autocommit=True)

        # Make sure no pools or matches were created
        assert len(db.query(Pool).all()) == 0
        assert len(db.query(Match).all()) == 0

