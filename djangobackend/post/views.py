from django.shortcuts import render
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

# Create your views here.

class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


from .models import Classifier
def classify_image(request):
    if request.method == 'POST':
        image = request.FILES['image']

        # 이미지 전처리
        # ...

        # AI 모델 로드 및 예측
        model = Classifier.load_model()
        output = model(input_tensor)
        predicted = max(output, 1)

        # 예측 결과 반환
        result = class_labels[predicted.item()]
        return JsonResponse({'result': result})

