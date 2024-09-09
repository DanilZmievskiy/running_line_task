from django.db import models

class Request(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
