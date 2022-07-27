from django.urls import path
from . import views

urlpatterns = [
    path('',views.req_data),
    path('get/',views.getdata),
    path('get/<str:pk>/',views.getvideo),
    path('post/',views.postdata),
    path('video_charge/',views.charges),
]