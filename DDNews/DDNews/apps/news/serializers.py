from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer
from .models import News,User

#作者信息序列化器
class User_Avatar_Url_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields=('avatar_url','id')

#新闻列表获取序列化器
class Get_Newslist_Serializer(ModelSerializer):
    #嵌套作者信息返回
    user = User_Avatar_Url_Serializer()
    report_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = News
        fields = ('id','title','source','index_image_url','digest','report_time','user','is_spider','source_avatar_url')



#详情页返回新闻发布者信息
class User_Report_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields=('avatar_url','id','signature','username')


#新闻详情页序列化器
class New_Detail_Serializer(ModelSerializer):
    user = User_Report_Serializer()
    report_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = News
        fields = (
        'id', 'title', 'source', 'digest', 'report_time', 'user','content','digest_label')