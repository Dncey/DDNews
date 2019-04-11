from django.shortcuts import render

from rest_framework.views import APIView

# Create your views here.

def IndexView(request):
    return render(request,'index.html',status=200)