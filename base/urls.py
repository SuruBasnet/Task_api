from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('videopage/<str:pk>/',views.videopage,name='videopage'),
    path('create/',views.create,name='create'),
    path('delete/<str:pk>/',views.delete,name='delete'),
    path('edit/<str:pk>/',views.edit,name='edit'),
]