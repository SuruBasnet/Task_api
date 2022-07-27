from django.shortcuts import render , redirect
from .models import videos
from .forms import Videosform
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from moviepy.editor import VideoFileClip
import os

# Create your views here.
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

def home(request):
    v = videos.objects.all()
    content = {'videos' : v}
    return render(request,'index.html',content)

def videopage(request,pk):
  vid = videos.objects.get(id=pk)
  content = {'video':vid}
  return render(request, 'video.html',content)


def create(request):
 videoform = Videosform()
 if request.method == 'POST':
  vid = Videosform(request.POST,request.FILES)
  if vid.is_valid():
    v = vid.save()
    vp = v.videoes
    vi = v.id
    c = length_validator(vp)
    d = size_validator(vp)
    if d == None:
      video =  videos.objects.get(id=vi)
      video.delete()
      print('d')
      messages.error(request,'Video file must be less than 1gb')
    if c == None:
      video =  videos.objects.get(id=vi)
      video.delete()
      print('c')
      messages.error(request,'Video file must be less than 10min')
    else:
        return redirect('home')
  else:
    messages.error(request, 'Only video files of mp4 or mkv is allowed!')
 content = {'form':videoform}
 return render(request,'video_form.html',content)

def edit(request,pk):
 video_0 = videos.objects.get(id=pk)
 videoform = Videosform(instance=video_0)
 if request.method == 'POST':
  vid  = Videosform(request.POST,request.FILES)
  if vid.is_valid():
    video_0.caption = request.POST.get('caption')
    video_0.videoes = request.FILES.get('videoes')
    video_0.save()
    vp = video_0.videoes
    vi = video_0.id
    c = length_validator(vp)
    d = size_validator(vp)
    if d == None:
      video =  videos.objects.get(id=vi)
      video.delete()
      print('d')
      messages.error(request,'Video file must be less than 1gb')
    if c == None:
      video =  videos.objects.get(id=vi)
      video.delete()
      print('c')
      messages.error(request,'Video file must be less than 10min')
    else:
        return redirect('home')
  else:
    messages.error(request, 'Only video files of mp4 or mkv is allowed!')
 content = {'form':videoform}
 return render(request,'video_form.html',content)

def delete(request,pk):
    v = videos.objects.get(id=pk)
    if request.method == 'POST':
        v.delete()
        return redirect('home')
    content = {'v':v}
    return render(request,'delete.html',content)
