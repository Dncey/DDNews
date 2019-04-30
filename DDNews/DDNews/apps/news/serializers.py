from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import News,User,Comment
import random


#作者信息序列化器
class User_Avatar_Url_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields=('avatar_url','id','username')

#新闻列表获取序列化器
class Get_Newslist_Serializer(ModelSerializer):
    #嵌套作者信息返回
    user = User_Avatar_Url_Serializer()
    report_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # 该新闻评论数
    comment = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ('id','title','source','index_image_url','digest','report_time','user','is_spider','source_avatar_url','clicks','comment')

    def get_comment(self,obj):
        comment = Comment.objects.filter(new=obj).count()
        if comment:
            return comment
        else:
            return 0


#推荐作者序列化器
class GetGoodAuthor(ModelSerializer):

    class Meta:
        model=User
        fields = ('id','signature','avatar_url','username')

#新闻详情页返回新闻发布者信息
class User_Report_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields=('avatar_url','id','signature','username')

#新闻详情页相关新闻
class Relate_News(ModelSerializer):
    class Meta:
        model = News
        fields = ("id", "index_image_url", "clicks", "title")

#新闻详情页序列化器
class New_Detail_Serializer(ModelSerializer):
    user = User_Report_Serializer()
    report_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    #获取右侧相关新闻信息
    relate_news = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = (
        'id', 'title', 'source', 'digest', 'report_time', 'user','content','digest_label','clicks','relate_news')

    def get_relate_news(self,obj):
        num = random.randint(0,500)
        news = News.objects.filter(category_id=obj.category_id,status=0).order_by('-clicks').all()[num:num+5]


        return Relate_News(news,many=True).data


#新闻评论
class New_Add_Comment_Serializer(ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    #嵌套序列化器
    user = User_Avatar_Url_Serializer(read_only=True)
    new_id = serializers.IntegerField()
    parent_id = serializers.CharField(write_only=True)
    class Meta:
        model = Comment
        fields =('id','user','new_id','create_time','content','like','parent_id')
        extra_kwargs = {
                        'create_time':{'read_only':True},
                        'like':{'read_only':True},
                        }


    def validate(self, attrs):
        new_id = attrs['new_id']
        parent_id=attrs['parent_id']
        if parent_id =='null':
            del attrs['parent_id']
        else:
            try:
                Comment.objects.get(id=parent_id)
            except:
                raise serializers.ValidationError("参数错误")

        try:
            News.objects.get(id=new_id)
        except:
            raise serializers.ValidationError("参数错误")

        return attrs

    def create(self, validated_data):


        #当前评论的用户
        user = self.context['request'].user
        validated_data['user'] = user


        comment = Comment.objects.create(**validated_data)

        return comment

#孙子评论
# class Subs_Comment_Serializer(ModelSerializer):
#     user = User_Avatar_Url_Serializer()
#     class Meta:
#         model = Comment
#         fields = ('id', 'user', 'content', 'like','subs')
#

#儿子评论
class Childrens_Conten_Serializer(ModelSerializer):
    user = User_Avatar_Url_Serializer()
    subs = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields =('id','like','subs','content','user')

    def get_subs(self, obj):
        # try:
        if obj.subs:
            return Childrens_Conten_Serializer(obj.subs,many=True).data
        else:
            return None

    # def get_user(self,obj):
    #     return obj.instance.user.username

#父级评论
class New_Get_Comment_Serializer(ModelSerializer):

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # 嵌套序列化器
    user = User_Avatar_Url_Serializer()
    new_id = serializers.IntegerField()
    subs = Childrens_Conten_Serializer(many=True)
    class Meta:
        model = Comment
        fields =('id','user','new_id','create_time','content','like','subs')


#推荐新闻序列化器
class GetGoodNewsSerializer(ModelSerializer):

    class Meta:
        model = News
        fields=('id','title')