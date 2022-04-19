from factory import SubFactory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    email = 'test@test.com'


class TrainingFocusFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.TrainingFocus'

    name = 'test_training_focus'


class ForceFactory(DjangoModelFactory):
    class Meta:
        model = 'exercises.Force'

    name = 'test_force'


class SplitFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.Split'

    name = 'test_split'


class SplitItemFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.SplitItem'

    split = SubFactory(SplitFactory)
    name = 'test_split_item'


class SplitDayFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.SplitDay'

    split_item = SubFactory(SplitItemFactory)
    force = SubFactory(ForceFactory)
    name = 'test_split_day'
    order = 1


class SplitDayForceFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.SplitDayForce'

    day = SubFactory(SplitDayFactory)
    force = SubFactory(ForceFactory)
    hierarchy = 1


class FrequencyAllocationFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.FrequencyAllocation'

    training_focus = SubFactory(TrainingFocusFactory)
    training_days = 4
    split = SubFactory(SplitFactory)
    hierarchy = 1
