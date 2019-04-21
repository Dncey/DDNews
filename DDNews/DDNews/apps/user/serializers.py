from rest_framework.serializers import Serializer,ModelSerializer
from news.models import User,User_Fans,News
from rest_framework.serializers import SerializerMethodField


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


# 作者的粉丝
class Author_Fans_Followed(ModelSerializer):

    user_info = SerializerMethodField()
    class Meta:
        model = User_Fans
        fields = ("user_info",)

    def get_user_info(self,obj):
        user =User.objects.filter(id=obj.fan_id).all()
        return User_Avatar_Url_Serializer(user).data