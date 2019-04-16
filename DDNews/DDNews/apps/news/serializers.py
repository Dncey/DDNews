from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer
from .models import News,User


class User_Avatar_Url_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields=('avatar_url','id')


class Get_Newslist_Serializer(ModelSerializer):
    user = User_Avatar_Url_Serializer()
    report_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = News
        fields = ('id','title','source','index_image_url','digest','report_time','user','is_spider','source_avatar_url')