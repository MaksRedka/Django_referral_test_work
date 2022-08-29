from operator import le
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    ref_code = models.CharField(max_length=12, blank=True)
    recomended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="ref_by")
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.ref_code}'

    def get_recommended_profile(self):
        qs = Profile.objects.all()
        my_recs = [p for p in qs if p.recomended_by == self.user]
        return my_recs

    def save(self, *args, **kwargs):
        if self.ref_code == "":
            code = generate_ref_code()
            self.ref_code = code
        
        recommended_by = self.recomended_by
        points = 0
        recommender = Profile.objects.get(user=recommended_by)
        if recommended_by is not None:
            my_recs = self.get_recommended_profile()
            resc_len = len(my_recs)
            if len(my_recs) > 0:
                self.points += 1

                while recommender is not None or points != 0:
                    recommender.points += 1
                    points -= 1
                    recommended_by = recommender.recomended_by
                    recommender = Profile.objects.get(user=recommended_by)
                
                if recommender is None and points != 0:
                    recommender.points += points
        else:        
            my_recs = self.get_recommended_profile()
            if len(my_recs) > 0:
                self.points += len(my_recs) + 1

        super().save(*args, **kwargs)