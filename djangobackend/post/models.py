from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200) # title 컬럼
    content = models.TextField()             # content 컬럼

    def __str__(self):
        """A string representation of the model."""
        return self.title

class DetectionResult(models.Model):
    class_id  = models.CharField(max_length=255)
    confidence = models.FloatField()
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    image_path = models.CharField(max_length=255)
    result_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.class_id } ({self.confidence*100:.2f}%)"

