from django.db import models

# Create your models here.
class Attachment(models.Model):
    name = models.CharField(max_length = 30)
    source = models.FileField(upload_to = 'attachment/')

    def __unicode__(self):
        return self.name

class KeyValue(models.Model):
    key = models.CharField(max_length = 500)
    value = models.CharField(max_length = 500)

    def __unicode__(self):
        return self.key