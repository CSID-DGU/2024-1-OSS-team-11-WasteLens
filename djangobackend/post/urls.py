from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ListPost.as_view()),
    # path('<int:pk>/', views.DetailPost.as_view()),

    # path('detect_image/', views.detect_image, name = 'detect_image'),
    # path('result/', views.result, name='result'),
    path('upload/', views.upload_image, name = 'upload_image'),
    path('detection-results/<int:image_id>/', views.get_detection_results, name='get_detection_results'),
    path('detection-results/', views.detection_result_list, name='detection_result_list'),
]