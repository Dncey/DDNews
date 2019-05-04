from rest_framework.serializers import Serializer,ModelSerializer
from news.models import User,User_Fans,News,Comment,User_Collection
from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers


class Author_Good_News(ModelSerializer):

    class Meta:
        model = News
        fields = ("id","index_image_url","clicks","title")

#获取作者信息
class GetAuthor_Info_Serializer(ModelSerializer):

    followed =SerializerMethodField()
    fans = SerializerMethodField()
    good_articles = SerializerMethodField()
    class Meta:
        model = User
        fields = ("avatar_url","id","username","followed","fans","good_articles")

    def get_fans(self,obj):
        fans = User_Fans.objects.filter(follow=obj).count()
        if fans:
            return fans
        else:
            return 0
    def get_followed(self,obj):
        followed = User_Fans.objects.filter(fan=obj).count()
        if followed:
            return followed
        else:
            return 0
    def get_good_articles(self,obj):
        article = News.objects.filter(user=obj).order_by("-clicks").all()[:5]
        return Author_Good_News(article,many=True).data


# 作者信息序列化器
class User_Avatar_Url_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar_url', 'id', 'username','signature')


# 作者的关注
class Author_Followed(ModelSerializer):

    user_info = SerializerMethodField()
    class Meta:
        model = User_Fans
        fields = ("user_info",)

    def get_user_info(self,obj):
        user = User.objects.filter(id=obj.follow_id).all()
        return User_Avatar_Url_Serializer(user,many=True).data

# 作者的粉丝
class Author_Fans(ModelSerializer):

    user_info = SerializerMethodField()
    class Meta:
        model = User_Fans
        fields = ("user_info",)

    def get_user_info(self,obj):
        user = User.objects.filter(id=obj.fan_id).all()
        return User_Avatar_Url_Serializer(user,many=True).data


# 收藏信息子新闻列表
class CollectionNewListSerializer(ModelSerializer):
    report_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # 该新闻评论数
    comment = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('id', 'title', 'source', 'index_image_url', 'digest', 'report_time', 'user', 'clicks', 'comment')

    def get_comment(self, obj):
        comment = Comment.objects.filter(new=obj).count()
        if comment:
            return comment
        else:
            return 0


# 收藏新闻列表获取序列化器
class Get_UserNewsCollection_Serializer(ModelSerializer):
    # 嵌套作者信息返回
    user = User_Avatar_Url_Serializer()
    new = CollectionNewListSerializer()

    class Meta:
        model = User_Collection
        fields = ('id', 'user', 'new')
