from django.db import models
from django.conf import settings

import datetime

class Lead(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    #credit_score = models.SmallIntegerField(default=0)
    #phone_number = models.CharField(max_length=255)
    #created_on = models.DateTimeField(auto_now_add=True)
    #converted = models.BooleanField(default=False)
    #converted_on = models.DateTimeField()
    #
    #def save(self, *args, **kwargs):
    #    if 'converted' in kwargs:
    #        if kwargs['converted'] != self.converted:
    #            self.converted_on = datetime.datetime.now()
    # 
    #def __str__(self):
    #    return self.name
