from pathlib import Path
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
from PIL import Image
import torch
from .models import DetectionResult
import base64
from django.core.files.base import ContentFile


from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Image
from .serializers import DetectionResultSerializer
from django.db.models import Prefetch

@csrf_exempt
@api_view(['POST'])
def upload_image(request):
    image = request.FILES.get('image')
    if image:
        image_instance = Image(image=image)
        image_instance.save()
        return Response({'success': True, 'image_id': image_instance.id})
    else:
        return Response({'success': False, 'error': 'No image provided'})


model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')


@api_view(['GET'])
def get_detection_results(request, image_id):
    try:
        image_instance = Image.objects.get(id=image_id)
        results = model(image_instance.image.path)

        # Initialize variables to track the highest confidence result
        highest_confidence = 0
        best_result = None

        # Iterate through the detection results to find the one with the highest confidence
        for result in results.xyxy[0]:
            x_min, y_min, x_max, y_max, confidence, label = result.tolist()

            if confidence > highest_confidence:
                highest_confidence = confidence
                best_result = {
                    "label": model.names[int(label)],
                    "confidence": confidence,
                    "x_min": int(x_min),
                    "y_min": int(y_min),
                    "x_max": int(x_max),
                    "y_max": int(y_max)
                }

        # If a best result was found, save it to the database
        if best_result:
            DetectionResult.objects.create(
                image=image_instance,
                label=best_result["label"],
                confidence=best_result["confidence"],
                x_min=best_result["x_min"],
                y_min=best_result["y_min"],
                x_max=best_result["x_max"],
                y_max=best_result["y_max"]
            )

        detection_results = DetectionResult.objects.filter(image=image_instance)
        serializer = DetectionResultSerializer(detection_results, many=True)
        return Response(serializer.data)
    except Image.DoesNotExist:
        return Response({'error': 'Image not found'}, status=404)



@api_view(['GET'])
def detection_result_list(request):
    detection_results = DetectionResult.objects.prefetch_related(
        Prefetch('image')
    ).all()
    serializer = DetectionResultSerializer(detection_results, many=True)
    return Response(serializer.data)