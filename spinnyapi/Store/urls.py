from django.urls import path
from .views import BoxListAPIView, UserBoxesAPIView, BoxAddAPIView, BoxDeleteAPIView, BoxUpdateAPIView

urlpatterns = [
    path('boxes/', BoxListAPIView.as_view(), name='box-list'),
    path('user-boxes/', UserBoxesAPIView.as_view(), name='user-boxes-list'),
    path('boxes/add/', BoxAddAPIView.as_view(), name='box-add'),
    path('boxes/<int:pk>/delete/', BoxDeleteAPIView.as_view(), name='box-delete'),
    path('boxes/<int:pk>/update/', BoxUpdateAPIView.as_view(), name='box-update'),
]
