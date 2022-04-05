from unicodedata import name
from django.test import TestCase
from django.conf import settings
from django.contrib import auth
from django.db.models import Q

from accounts.models import User, FrequencyAllocation, Split, SplitDay, SplitDayForce, SplitItem, TrainingFocus
from exercises.models import Exercise, Force, Mechanic, Progression, ProgressionType, ProgressionTypeAllocation, Purpose, Tier

# Create your tests here.


class UserTestCase(TestCase):

    def setUp(self):  # create a user
        user_a = User(email='test@test.com')
        user_a_pw = 'some_123_password'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a  # make available for other methods
        user_b = User.objects.create_user(
            'test2@test.com', 'some_123_password')
        self.user_b = user_b
        self.superuser = User.objects.create_superuser(
            email='t@t.com', password='123')

        self.trainingfocus = TrainingFocus.objects.create(
            name='test_training_focus')

        self.split = Split.objects.create(
            name='test_split')

        self.splititem = SplitItem.objects.create(
            split=self.split,
            name='test_splititem')

        self.force = Force.objects.create(
            name='test_force',
            base_weekly_sets=10,
        )

        self.splitday = SplitDay.objects.create(
            split_item=self.splititem,
            name='test_splitday',
            # force=self.splitdayforce,
            order=1)

        self.splitdayforce = SplitDayForce.objects.create(
            day=self.splitday,
            force=self.force,
            hierarchy=1)

        self.frequencyallocation = FrequencyAllocation.objects.create(
            training_focus=self.trainingfocus,
            training_days=4,
            split=self.split,
            hierarchy=1
        )

        self.tier = Tier.objects.create(
            name='T1'
        )

        self.purpose = Purpose.objects.create(
            name='Squat'
        )

        self.mechanic = Mechanic.objects.create(
            name='Compound'
        )

        self.prog_type = ProgressionType.objects.create(
            name='Test',
        )

        self.prog_type_allocation = ProgressionTypeAllocation.objects.create(
            training_focus=self.user_a.training_focus,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
            target_rir=3,
            min_rir=2
        )

        self.progression = Progression.objects.create(
            progression_type=self.prog_type,
            rep_delta=0,
            rir_delta=-2,
            weight_change=0.5,
            rep_change=2,
        )

        self.exercise1 = Exercise.objects.create(
            name="test_exercise",
            mechanic=self.mechanic,
            force=self.force,
            purpose=self.purpose,
            tier=self.tier,
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
            is_active=1,
            is_unilateral=0,
        )

        self.exercise2 = Exercise.objects.create(
            name="test_exercise2",
            user=self.user_a,
            mechanic=self.mechanic,
            force=self.force,
            purpose=self.purpose,
            tier=self.tier,
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
            is_active=1,
            is_unilateral=0,
        )

    def test_users_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 3)
        self.assertNotEqual(user_count, 0)  # not 0 users

    def test_usera_password(self):
        self.assertEqual(self.user_a.check_password('some_123_password'), True)

    def test_create_user(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')

    def test_user_a_perms(self):
        self.assertTrue(self.user_a.is_staff)
        self.assertTrue(self.user_a.is_superuser)
        self.assertFalse(self.user_a.is_admin)

    def test_userb_perms(self):
        self.assertFalse(self.user_b.is_staff)
        self.assertFalse(self.user_b.is_superuser)
        self.assertFalse(self.user_b.is_admin)

    def test_superuser_perms(self):
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_admin)

    def test_user_password(self):
        user_qs = User.objects.filter(email__iexact='test@test.com')
        self.assertTrue(
            self.user_a.check_password(self.user_a_pw)
        )
        self.assertFalse(
            self.user_a.check_password("fakepassword")
        )

    def test_login_url(self):
        login_url = settings.LOGIN_URL
        data = {"email": "test@test.com", "password": self.user_a_pw}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_login_success(self):
        self.client.login(email=self.user_a.email,
                          password=self.user_a.password)

    def test_should_not_have_split(self):
        self.assertFalse(self.user_a.should_have_split())

    def test_should_have_split(self):
        self.user_a.training_focus = self.trainingfocus
        self.user_a.training_days = 4
        self.assertTrue(self.user_a.should_have_split())

    def test_get_split_from_frequency_allocation(self):
        self.user_a.training_focus = self.trainingfocus
        self.user_a.training_days = 4
        self.user_a.save()
        self.assertEqual(
            self.user_a.get_split_from_frequency_allocation(),
            self.frequencyallocation.split
        )

    def test_assign_split(self):
        self.user_a.training_focus = self.trainingfocus
        self.user_a.training_days = 4
        self.user_a.save()
        self.user_a.assign_split()
        self.assertEqual(self.split, self.user_a.split)

    def test_split_days_count(self):
        self.assertEqual(self.user_a.split_days_count(), 0)

    def test_is_training_focus_changed(self):
        self.trainingfocus2 = TrainingFocus.objects.create(
            name='test_training_focus2')
        self.user_a.training_focus = self.trainingfocus2
        self.assertTrue(self.user_a.is_training_focus_changed())
        self.user_a.save()
        self.assertFalse(self.user_a.is_training_focus_changed())
        self.user_c = User(email='test3@test.com')
        self.assertFalse(self.user_c.is_training_focus_changed())
        self.user_d = User(email='test3@test.com',
                           training_focus=self.trainingfocus
                           )
        self.assertTrue(self.user_d.is_training_focus_changed())

    def test_has_exercises(self):
        self.assertFalse(self.user_b.has_exercises())

    def test_has_exercises_true(self):
        self.assertTrue(self.user_a.has_exercises())

    def test_get_exercises(self):
        self.assertEqual(Exercise.objects.filter(user=self.user_a).count(),
                         self.user_a.get_exercises().count())
        self.assertEqual(self.user_b.get_exercises().count(), 0)

    def test_reassign_exercises(self):
        # GIVEN a User with no Exercises
        # WHEN
        self.user_b.reassign_exercises()
        # THEN
        exercises = Exercise.objects.filter(user=None).count()
        user_exercises = self.user_b.exercise_set.count()
        self.assertEqual(exercises, user_exercises)

    def test_reassign_exercises2(self):
        # GIVEN a User with a list of custom exercises
        current_exercises = self.user_a.exercise_set.all().count()
        # WHEN
        self.user_a.reassign_exercises()
        # THEN
        new_exercises = self.user_a.exercise_set.all().count()
        self.assertEqual(current_exercises, new_exercises)
