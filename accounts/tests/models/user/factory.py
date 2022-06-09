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
