from django.shortcuts import render
from django.http import FileResponse

def index(request):
    render(request, "index.html")

def video_download(request):
    pass

def running_line():
    pass
