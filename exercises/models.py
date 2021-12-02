from django.db import models



class MuscleGroup(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Exercise(models.Model):
    purpose_choices = (
        ('Squat', 'Squat'),('Bench', 'Bench'),('Deadlift', 'Deadlift'),)
    tier_choices = (('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('Other', 'Other'),)
    mechanic_choices = (('Compound', 'Compound'), ('Isolation', 'Isolation'))
    force_choices = (('Push', 'Push'), ('Pull', 'Pull'))

    name = models.CharField(max_length=60, unique=True)
    purpose = models.CharField(max_length=60, choices=purpose_choices,
        help_text="Which main exercise does this improve?")
    tier = models.CharField(max_length=60, choices=tier_choices,
        help_text="T1 exercises are the competition exercises.\
            T2 exercises are close variations of the main lifts. \
            T3 exercises develop the musculature eg. quads for squats. \
            Other exercises develop supplementary muscles")
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    mechanic = models.CharField(max_length=60, choices=mechanic_choices)
    force = models.CharField(max_length=60, choices=force_choices)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, null=True, blank=True)
    # User should see exercises where user is NULL (mixed exercises)
    # and where user==currentUser

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name="UserUniqueExercise")
            ]

    def __str__(self):
        return self.name
    