import collections

FIXTURE_FIELDS = ['gegen', 'athome', 'prob']
class FixtureInfo(collections.namedtuple('_FixtureInfo', FIXTURE_FIELDS)):
    __slots__ = ()
    
COMBINATION_FIELDS = ['teams', 'score', 'benchscore', 'cleanies']
class RotationCombinations(collections.namedtuple('_CombinationInfo', COMBINATION_FIELDS)):
    __slots__ = ()
