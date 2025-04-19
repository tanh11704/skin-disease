from django.db import models

# Create your models here.
class ImageUpload(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ImageUpload(id={self.id}, uploaded_at={self.uploaded_at})"