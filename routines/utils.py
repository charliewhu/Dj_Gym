from exercises.models import Rir

def rounder(num, multiple):
    return multiple * round(num/multiple)

def get_1rm_percent(reps, rir):
    if rir < 5:
        obj = Rir.objects.get(
            reps=reps,
            rir=rir
            )
        return obj.percent
    else: 
        return None

def get_1rm(weight, reps, rir):
    if rir < 5:
        obj = Rir.objects.get(
            reps=reps,
            rir=rir
            )

        one_rm = weight / obj.percent
        return one_rm
    else: 
        return None