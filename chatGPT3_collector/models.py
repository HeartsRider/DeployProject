from django.db import models

# Create your models here.

class ChatGPT3RequestorModel(models.Model):
    apikey = models.CharField(max_length=100)
    payload = models.CharField(max_length=100)
    class Meta:
        managed = True
    def __str__(self):
        return self.payload
