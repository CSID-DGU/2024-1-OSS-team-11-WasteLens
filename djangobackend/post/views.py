from pathlib import Path
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
import torch
from django.shortcuts import render, redirect
import cv2
from .models import DetectionResult
import base64
from django.core.files.base import ContentFile


# model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
# # model.load_state_dict(torch.load(weight_path))
# # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#
# def detect_image(request):
#     detected_objects = []
#     if request.method == 'POST':
#         if 'image' in request.FILES:
#             # 파일 업로드 방식으로 이미지 받기
#             image_file = request.FILES['image']
#             fs = FileSystemStorage()
#             image_path = fs.save(image_file.name, image_file)
#             image_path = os.path.join(settings.MEDIA_ROOT, image_path)
#         elif 'image' in request.POST:
#             # Base64 인코딩된 이미지 데이터 처리 (카메라로 찍은 사진)
#             format, imgstr = request.POST['image'].split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
#             fs = FileSystemStorage()
#             image_path = fs.save(data.name, data)
#             image_path = os.path.join(settings.MEDIA_ROOT, image_path)
#             image_file = data
#
#         # 이미지 처리 및 객체 탐지
#
#         img = Image.open(image_path)
#         results = model(img)
#
#
#         # 결과 저장
#         image_dir, image_filename = os.path.split(image_path)
#         result_filename = os.path.splitext(image_filename)[0] + '.txt'
#         result_path = os.path.join(image_dir, result_filename)
#
#         with open(result_path, 'w') as f:
#             for result in results.xyxy[0]:
#                 x1, y1, x2, y2, conf, cls = result
#                 class_id = model.names[int(cls)]
#                 confidence = float(conf)
#                 box = [int(x1), int(y1), int(x2), int(y2)]
#                 # line = f"{class_id} {confidence} {' '.join(map(str, box))}\n"
#                 # f.write(line)
#
#                 # 데이터베이스에 저장
#                 DetectionResult.objects.create(
#                     class_id=class_id,
#                     confidence=confidence,
#                     x1=box[0],
#                     y1=box[1],
#                     x2=box[2],
#                     y2=box[3],
#                     image_path=image_path,
#                     image=image_file,
#                     result_path=result_path
#                 )
#
#                 # 탐지된 객체 추가
#                 detected_objects.append({
#                     'class_id': class_id,
#                     'confidence': confidence,
#                     'box': box
#                 })
#
#         # 결과 렌더링
#         return render(request, 'post/result.html', {
#             'detected_objects': detected_objects,
#             'image_path': image_path,
#         })
#         # return redirect('result', result_path=result_path, image_path = 'image_path')
#
#     # 이미지 업로드 폼 렌더링
#     return render(request, 'post/detect_image.html')
#
# # def result(request, result_path, image_path):
# #     # 이미지 로드
# #     # image = cv2.imread(result_path)
# #
# #     # 결과 렌더링
# #     return render(request, 'post/result.html', {
# #         'result_path': result_path,
# #         'image_path' : image_path
# #     })
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
        for result in results.xyxy[0]:
            x_min, y_min, x_max, y_max, confidence, label = result.tolist()
            DetectionResult.objects.create(
                image=image_instance,
                label=model.names[int(label)],
                confidence=confidence,
                x_min=int(x_min),
                y_min=int(y_min),
                x_max=int(x_max),
                y_max=int(y_max)
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