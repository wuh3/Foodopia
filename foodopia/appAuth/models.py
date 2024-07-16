from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
import appMealplan.models as mp
import random
# from djangoblog.utils import get_current_site

def _get_random_nickename() -> str:
    random_number = random.randint(1000, 9999)
    name = f"YourString_{random_number}"
    return name
class FoodopiaUser(AbstractUser):
    nickname = models.CharField(_('nickname'), max_length=100, default=_get_random_nickename)
    age = models.IntegerField(_('age'), blank=True)
    sex = models.CharField(_('sex'), max_length=50, choices=[
        ("male", "male"),
        ("female", "female")
    ], blank=False)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    meal_plan = models.ForeignKey(mp.MealPlan,
                                  models.SET_NULL,
                                  blank=True,
                                  null=True,)
    
    def get_absolute_url(self):
        return reverse(
            'User_Information: ', kwargs={
                'Username': self.username})

    def __str__(self):
        return self.email

    # def get_full_url(self):
    #     site = get_current_site().domain
    #     url = "https://{site}{path}".format(site=site,
    #                                         path=self.get_absolute_url())
    #     return url

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'