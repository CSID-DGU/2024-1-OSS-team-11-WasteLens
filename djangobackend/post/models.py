from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

class DetectionResult(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='detection_results')
    label = models.CharField(max_length=100)
    confidence = models.FloatField()
    x_min = models.IntegerField()
    y_min = models.IntegerField()
    x_max = models.IntegerField()
    y_max = models.IntegerField()

    def __str__(self):
        return f"{self.label } ({self.confidence*100:.2f}%)"

