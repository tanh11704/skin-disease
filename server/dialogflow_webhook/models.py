from django.db import models

# Create your models here.
class Disease(models.Model):
    name = models.CharField(max_length=255)
    definition = models.TextField()
    symptoms = models.TextField()
    cause = models.TextField()
    treatment = models.TextField()
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'diseases'
        verbose_name = 'Disease'
        verbose_name_plural = 'Diseases'

    def __str__(self):
        return self.name