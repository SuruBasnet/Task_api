from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import videos
from .serializers import VideoSerializer
from moviepy.editor import VideoFileClip
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import filesizeformat
import os
# from static import images

def length_validator(filename):
  filestr = str(filename)
  video_path = staticfiles_storage.path("videos/" + filestr)
  file_size = os.path.getsize(video_path)
  print(file_size)
  clip = VideoFileClip(video_path)
  duration = clip.duration
  if duration < 600:
    return filename
  else:
    return None

def size_validator(filename):
  filestr = str(filename)
  video_path = staticfiles_storage.path("videos/" + filestr)
  file_size = os.path.getsize(video_path)
  if file_size < 1000000000:
    return filename
  else:
    return None

def charge_length_validator(filename):
  filestr = str(filename)
  video_path = staticfiles_storage.path("videos/" + filestr)
  clip = VideoFileClip(video_path)
  duration = clip.duration
  if duration < 378:
    return True
  else:
    return None

def charge_size_validator(filename):
  filestr = str(filename)
  video_path = staticfiles_storage.path("videos/" + filestr)
  file_size = os.path.getsize(video_path)
  if file_size < 500000000:
    return True
  else:
    return None

@api_view(['GET'])
def req_data(request):
  l = {
    'get/' : 'get all the list of videoes',
    'get/<date>' : 'To get videos uploaded on a specific date example-(get/2022(y)-07(m)-23(d))',
    'post/' : 'To post videoes (key - content, videoes)',
    'video_charge/' : 'To get charges of video(key - content , videoes)'
  }

  return Response(l)

@api_view(['GET'])
def getdata(request):
  video = videos.objects.all()
  serializer = VideoSerializer(video,many=True)

  return Response(serializer.data)


@api_view(['GET'])
def getvideo(request,pk):
  video = videos.objects.filter(created=pk)
  serializer = VideoSerializer(video,many=True)

  return Response(serializer.data)


@api_view(['POST'])
def postdata(request):
    serializer = VideoSerializer(data=request.data)

    if serializer.is_valid():
        v = serializer.save()
        vp = v.videoes
        vi = v.id
        c = length_validator(vp)
        d = size_validator(vp)
        if d == None:
          video =  videos.objects.get(id=vi)
          video.delete()
          return Response('Video file must be less than 1gb')
        if c == None:
          video =  videos.objects.get(id=vi)
          video.delete()
          return Response('Video file must be less than 10min')
        else:
          return Response(serializer.data)
        
    else:
      return Response('Only video file of mp4 or mkv is allowed!')

@api_view(['POST'])
def charges(request):
    serializer = VideoSerializer(data=request.data)
    price = 0

    if serializer.is_valid():
        v = serializer.save()
        vp = v.videoes
        vi = v.id
        c = charge_length_validator(vp)
        d = charge_size_validator(vp)
        print(c)
        print(d)
        if c == None:
          price += 20
        elif c == True:
          price += 12.5
        if d == None:
          price += 12.5
        elif d == True:
          price += 5
        video =  videos.objects.get(id=vi)
        video.delete()
        str_price = str(price)
        return Response('Charge for this video: $' +  str_price)
        
    else:
      return Response('Only video file of mp4 or mkv is allowed!')