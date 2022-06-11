from factory import SubFactory
from factory.django import DjangoModelFactory


class TierFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.Tier'

    name = 'test_tier'


class PurposeFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.Purpose'

    name = 'test_purpose'


class MechanicFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.Mechanic'

    name = 'test_mechanic'


class ProgressionTypeFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.ProgressionType'

    name = 'test_progression_type'


class ProgressionTypeAllocationFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.ProgressionTypeAllocation'

    mechanic = SubFactory(MechanicFactory)
    tier = SubFactory(TierFactory)
    min_reps = 8
    max_reps = 12
    min_rir = 1
    max_rir = 3


class ProgressionFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.Progression'

    progression_type = SubFactory(ProgressionTypeFactory)
    rep_delta = 0
    rir_delta = -2
    weight_change = 0.5
    rep_change = 2


class ForceFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.Force'

    name = 'test_force'
    base_weekly_sets = 10


class ExerciseFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.Exercise'

    name = 'test_exercise'
    force = SubFactory(ForceFactory)
    purpose = SubFactory(PurposeFactory)
    mechanic = SubFactory(MechanicFactory)
    tier = SubFactory(TierFactory)
