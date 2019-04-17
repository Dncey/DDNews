from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
import rest_framework_jwt.authentication

class GetUserfollowd(APIView):
    def get(self,request):
        print("zz")