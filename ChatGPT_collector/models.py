from django.db import models

class ChatGPTRequestorModel(models.Model):
    apikey = models.CharField(max_length=100)
    payload = models.CharField(max_length=100)

    def __str__(self):
        return self.payload
