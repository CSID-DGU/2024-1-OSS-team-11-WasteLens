from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ListPost.as_view()),
    # path('<int:pk>/', views.DetailPost.as_view()),

    path('detect_image/', views.detect_image, name = 'detect_image'),
    # path('result/', views.result, name='result'),
]