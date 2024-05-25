# # from django.shortcuts import render, redirect
# # from rest_framework import generics
# # from .models import Post
# # from .serializers import PostSerializer
# # import os
# # import cv2
# # from django.conf import settings
# # import subprocess
# #
# # # Create your views here.
# #
# # # class ListPost(generics.ListCreateAPIView):
# # #     queryset = Post.objects.all()
# # #     serializer_class = PostSerializer
# # #
# # # class DetailPost(generics.RetrieveUpdateDestroyAPIView):
# # #     queryset = Post.objects.all()
# # #     serializer_class = PostSerializer
# #
# # def detect_image(request):
# #     if request.method == 'POST' and 'image' in request.FILES:
# #         image_file = request.FILES['image']
# #         image_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
# #         with open(image_path, 'wb+') as destination:
# #             for chunk in image_file.chunks():
# #                 destination.write(chunk)
# #
# #         # YOLOv5 detect.py 실행
# #         yolov5_path = os.path.join(settings.BASE_DIR, 'yolov5')
# #         weights_path = os.path.join(settings.BASE_DIR, 'best.pt')
# #         result = subprocess.run([
# #             'python', os.path.join(yolov5_path, 'detect.py'),
# #             '--weights', weights_path,
# #             '--img416', '--conf 0.5',
# #             '--source', image_path,
# #             '--project', 'media',
# #             '--name', os.path.splitext(image_path)[0] + '_output'
# #         ], capture_output=True, text=True)
# #
# #         print(result)
# #
# #         output_image_path = os.path.splitext(image_path)[0] + '_output.jpg'
# #         result_file = os.path.splitext(image_path)[0] + '.txt'
# #         with open(result_file, 'w') as f:
# #             f.write(result.stdout)
# #
# #
# #         return redirect('result', image_path=image_path, result_file=result_file, output_image_path=output_image_path)
# #     else:
# #         return render(request, 'post/detect_image.html')
# #
# #
# # def result(request, image_path, result_file, output_image_path):
# #     # 이미지 로드
# #     image = cv2.imread(output_image_path)
# #
# #     # detect.py 결과 파일 읽기
# #     detected_objects = []
# #     if os.path.exists(result_file):
# #         with open(result_file, 'r') as f:
# #             for line in f.readlines():
# #                 line = line.strip()
# #                 if line:
# #                     class_id, confidence, x1, y1, x2, y2 = map(float, line.split())
# #                     detected_objects.append({
# #                         'class_id': int(class_id),
# #                         'confidence': confidence,
# #                         'box': (int(x1), int(y1), int(x2), int(y2))
# #                     })
# #     else:
# #         print("Result file not found at", result_file)
# #
# #     # 결과 렌더링
# #     return render(request, 'post/result.html', {
# #         'image_path': image_path,
# #         'output_image_path': output_image_path,
# #         'detected_objects': detected_objects,
# #         'image': image
# #     })
#
# from pathlib import Path
# import pathlib
# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath
# import os
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from PIL import Image
# import torch
# from django.shortcuts import render, redirect
# import cv2
#
#
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
# # model.load_state_dict(torch.load(weight_path))
# # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#
# def detect_image(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         # 이미지 파일 받기
#         image_file = request.FILES['image']
#         fs = FileSystemStorage()
#         image_path = fs.save(image_file.name, image_file)
#         image_path = os.path.join(settings.MEDIA_ROOT, image_path)
#
#         # 이미지 처리
#         img = Image.open(image_path)
#         results = model(img)  # 모델 실행
#
#         # 결과 저장
#         image_dir, image_filename = os.path.split(image_path)
#         result_filename = os.path.splitext(image_filename)[0] + '.txt'
#         result_path = os.path.join(image_dir, result_filename)
#
#
#         with open(result_path, 'w') as f:
#             for result in results.xyxy[0]:
#                 x1, y1, x2, y2, conf, cls = result
#                 class_name = model.names[int(cls)]
#                 confidence = float(conf)
#                 box = [int(x1), int(y1), int(x2), int(y2)]
#                 line = f"{class_name} {confidence} {' '.join(map(str, box))}\n"
#                 f.write(line)
#
#         # 이미지 렌더링
#         return render(request, 'post/result.html', {
#             'result_path': result_path,
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

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)


# model.load_state_dict(torch.load(weight_path))
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def detect_image(request):
    detected_objects = []
    if request.method == 'POST':
        if 'image' in request.FILES:
            # 파일 업로드 방식으로 이미지 받기
            image_file = request.FILES['image']
            fs = FileSystemStorage()
            image_path = fs.save(image_file.name, image_file)
            image_path = os.path.join(settings.MEDIA_ROOT, image_path)
        elif 'image' in request.POST:
            # Base64 인코딩된 이미지 데이터 처리 (카메라로 찍은 사진)
            format, imgstr = request.POST['image'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
            fs = FileSystemStorage()
            image_path = fs.save(data.name, data)
            image_path = os.path.join(settings.MEDIA_ROOT, image_path)

        # 이미지 처리 및 객체 탐지
        img = Image.open(image_path)
        results = model(img)

        # 결과 저장
        image_dir, image_filename = os.path.split(image_path)
        result_filename = os.path.splitext(image_filename)[0] + '.txt'
        result_path = os.path.join(image_dir, result_filename)

        with open(result_path, 'w') as f:
            for result in results.xyxy[0]:
                x1, y1, x2, y2, conf, cls = result
                class_id = model.names[int(cls)]
                confidence = float(conf)
                box = [int(x1), int(y1), int(x2), int(y2)]
                line = f"{class_id} {confidence} {' '.join(map(str, box))}\n"
                f.write(line)

                # 데이터베이스에 저장
                DetectionResult.objects.create(
                    class_id=class_id,
                    confidence=confidence,
                    x1=box[0],
                    y1=box[1],
                    x2=box[2],
                    y2=box[3],
                    image_path=image_path,
                    result_path=result_path
                )

                # 탐지된 객체 추가
                detected_objects.append({
                    'class_id': class_id,
                    'confidence': confidence,
                    'box': box
                })

        # 결과 렌더링
        return render(request, 'post/result.html', {
            'detected_objects': detected_objects,
            'image_path': image_path,
        })
        # return redirect('result', result_path=result_path, image_path = 'image_path')

    # 이미지 업로드 폼 렌더링
    return render(request, 'post/detect_image.html')

# def result(request, result_path, image_path):
#     # 이미지 로드
#     # image = cv2.imread(result_path)
#
#     # 결과 렌더링
#     return render(request, 'post/result.html', {
#         'result_path': result_path,
#         'image_path' : image_path
#     })

