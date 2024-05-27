from rest_framework import serializers
from .models import DetectionResult



class DetectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResult
        fields = '__all__'
        read_only_fields = ('id',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image_id'] = instance.image.pk  # instance.image.id 대신 instance.image.pk 사용
        return rep