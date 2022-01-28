from django.db import models



class Force(models.Model):
    """eg Hip Hinge, Vertical Push"""
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name  = models.CharField(max_length=20, unique=True)
    force = models.ManyToManyField(Force)
    
    def __str__(self):
        return self.name


class Exercise(models.Model):
    purpose_choices = (
        ('Squat', 'Squat'),('Bench', 'Bench'),('Deadlift', 'Deadlift'),)
    tier_choices = (('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('Other', 'Other'),)
    mechanic_choices = (('Compound', 'Compound'), ('Isolation', 'Isolation'))
    # maybe more detail here (vert/horiz pull, vert/horiz press, leg press, hip hinge)

    name = models.CharField(max_length=60, unique=True)
    plpurpose = models.CharField(max_length=60, choices=purpose_choices,
        help_text="Which powerlifting exercise does this improve?", null=True)
    pltier = models.CharField(max_length=60, choices=tier_choices,
        help_text="T1 exercises are the competition exercises.\
            T2 exercises are close variations of the main lifts. \
            T3 exercises develop the musculature eg. quads for squats. \
            Other exercises develop supplementary muscles", null=True)
    mechanic = models.CharField(max_length=60, choices=mechanic_choices)
    force = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, null=True, blank=True)
    # User should see exercises where user is NULL (mixed exercises)
    # and where user==currentUser

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name="UserUniqueExercise")
            ]

    def __str__(self):
        return self.name
    

class ExerciseVolume(models.Model):
    pass