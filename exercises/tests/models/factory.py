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
