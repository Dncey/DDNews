from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import render

from news.models import User
import random
import re
from django_redis import get_redis_connection
from rest_framework.views import APIView
from DDNews.lib.captcha.captcha import captcha
import hashlib
from rest_framework_jwt.settings import api_settings

# Create your views here.

#获取图片验证码
class Generate_ImageCode(APIView):
    def get(self,request,uuid):
        #连接redis
        conn = get_redis_connection('default')
        # 使用captcha工具生成图片验证码
        name, text, image = captcha.generate_captcha()
        # 把text存入redis数据库中(图片内容)
        try:
            conn.setex('ImageCode_%s' % uuid, 300, text)
        except:
            return Response({'errno':500,'errmsg':'保存图片验证码失败'},status=500)
        # 返回图片
        return HttpResponse(image)


#生成注册手机验证码
class Generate_Smscode_register(APIView):
    def post(self,request):
        #获取请求参数
        try:
            mobile = request.data['mobile']
            imageCode = request.data['imageCode']
            uuid = request.data['imageCodeId']
        except:
            return Response({'errmsg':'参数缺失'})
        #判断手机号是否正确
        is_truemobile = re.match(r'1[356789]\d{9}$',mobile)
        if not is_truemobile:
            return Response({'errmsg':'手机号错误'})

        # 连接redis
        conn = get_redis_connection('default')
        #尝试获取图片验证码
        try:
            rel_imgcode = conn.get('ImageCode_%s' % uuid)
            if rel_imgcode:
                rel_imgcode = rel_imgcode.decode()
                conn.delete('ImageCode_%s' % uuid)
        except:
            return Response({'errmsg':'获取图片验证码失败'})

        if not rel_imgcode:
            return Response({'errmsg':'图片验证码过期'})

        print(rel_imgcode)
        #判断图片验证码是否相同,都变成大写方便比较
        if imageCode.upper() !=rel_imgcode.upper():
            return Response({'errmsg':'图片验证码错误'})


        #查询手机号是否已经注册

        count = User.objects.filter(mobile=mobile).count()


        if count==1:
            return Response({'errmsg':'手机号已经注册'})

        #连接sms_code的redis
        db_sms = get_redis_connection('sms_code')

        flag = db_sms.get('sms_code_flag_%s'%mobile)
        if flag:
            return Response({"errmsg":'操作过于频繁'})


        #生成短信验证码
        result = random.randint(0,999999)
        sms_code = '%06d' %result

        #使用第三方发送短信

        print(sms_code)


        #使用管道减少对redis的多次操作一次提交多个请求
        pl = db_sms.pipeline()
        # redis保存手机号
        pl.setex('sms_code_register_%s'%mobile,300,sms_code)
        #设置一个标志是否频繁请求
        pl.setex('sms_code_flag_%s'%mobile,60,sms_code)

        #用管道最后需要执行
        pl.execute()

        return Response({'errmsg':'OK'})


#生成忘记密码短信验证码
class Generate_Smscode_forget(APIView):
    def post(self,request):
        #获取请求参数
        try:
            mobile = request.data['mobile']
            imageCode = request.data['imageCode']
            uuid = request.data['imageCodeId']
        except:
            return Response({'errmsg':'参数缺失'})
        #判断手机号是否正确
        is_truemobile = re.match(r'1[356789]\d{9}$',mobile)
        if not is_truemobile:
            return Response({'errmsg':'手机号错误'})

        # 连接redis
        conn = get_redis_connection('default')
        #尝试获取图片验证码
        try:
            rel_imgcode = conn.get('ImageCode_%s' % uuid)
            if rel_imgcode:
                rel_imgcode = rel_imgcode.decode()
                conn.delete('ImageCode_%s' % uuid)
        except:
            return Response({'errmsg':'获取图片验证码失败'})

        if not rel_imgcode:
            return Response({'errmsg':'图片验证码过期'})

        print(rel_imgcode)
        #判断图片验证码是否相同,都变成大写方便比较
        if imageCode.upper() !=rel_imgcode.upper():
            return Response({'errmsg':'图片验证码错误'})


        #查询手机号是否已经注册
        try:
            count = User.objects.filter(mobile=mobile).count()
        except:
            return Response({'errmsg':'查询数据库出错'})

        if count==0:
            return Response({'errmsg':'手机号未注册'})

        #连接sms_code的redis
        db_sms = get_redis_connection('sms_code')

        flag = db_sms.get('sms_code_flag_%s'%mobile)
        if flag:
            return Response({"errmsg":'操作过于频繁'})


        #生成短信验证码
        result = random.randint(0,999999)
        sms_code = '%06d' %result

        #使用第三方发送短信

        print(sms_code)


        #使用管道减少对redis的多次操作一次提交多个请求
        pl = db_sms.pipeline()
        # redis保存手机号
        pl.setex('sms_code_forget_%s'%mobile,300,sms_code)
        #设置一个标志是否频繁请求
        pl.setex('sms_code_flag_%s'%mobile,60,sms_code)

        #用管道最后需要执行
        pl.execute()

        return Response({'errmsg':'OK'})

#用户注册

class User_Register(APIView):
    def post(self,request):
        mobile = request.data.get('mobile')
        sms_code = request.data.get('sms_code')
        password = request.data.get('password')
        is_checked = request.data.get('is_checked')
        confirm_pwd = request.data.get('confirm_pwd')
        print(is_checked)
        if not is_checked :
            return Response({'errmsg':'请选择用户评论|发布新闻协议'})



        if password != confirm_pwd:
            return Response({'errmsg':'密码输入不一致'})

        # 连接sms_code的redis
        db_sms = get_redis_connection('sms_code')
        try:
            res = db_sms.get('sms_code_register_%s'%mobile)
        except:
            return Response({'errmsg':'查询数据哭出错'})

        if not res:
            return Response({'errmsg':'手机验证码过期'})

        if sms_code != res.decode():
            return Response({'errmsg': '验证码错误'})

        #验证手机号是否已存在
        count = User.objects.filter(mobile=mobile).count()

        if count == 1:
            return Response({'errmsg': '手机号已经注册'})

        #创建md5加密对象
        md5= hashlib.md5()

        #对数据进行加密
        md5.update(password.encode())
        #获取加密后的数据
        passwd = md5.hexdigest()

        #往数据库添加数据
        try:
            user = User.objects.create(username=mobile,mobile=mobile,password=passwd)
        except:
            return Response({"errmsg":'数据库保存数据失败'},status=500)

        #生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        data = {'errmsg':'OK',
                'data':{'token':token,
                        'username':user.username,
                        'user_id':user.id,
                        'avatar_url':user.avatar_url
                        }}
        print(token)
        return Response(data)


#用户登录
class User_Login(APIView):
    def post(self,request):
        login_text = request.data.get('login_text')
        password = request.data.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode())
        #获取加密后的值
        passwd = md5.hexdigest()

        mobile = re.match(r'1[356789]\d{9}$', login_text)

        email = re.match(r"[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){1,3}$",login_text)

        if mobile:
            user = User.objects.filter(password=passwd,mobile=login_text).first()
        elif email:
            user = User.objects.filter(password=passwd,email=login_text).first()
        else:
            user = User.objects.filter(password=passwd,username=login_text).first()

        if not user:
            return Response({'errmsg':'用户或密码错误'})

        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)


        data = {
            'errmsg':'OK',
            'data':{
                'token':token,
                'user_id':user.id,
                'username':user.username,
                'avatar_url':user.avatar_url
            }
        }
        return Response(data)


#用户忘记密码

class User_ResetPwd(APIView):
    def post(self,request):
        mobile = request.data.get('mobile')
        smscode = request.data.get('smscode')
        password =request.data.get('password')

        # 连接sms_code的redis
        db_sms = get_redis_connection('sms_code')

        #从redis中取出验证码
        try:
            res = db_sms.get('sms_code_forget_%s'%mobile)
        except:
            return Response({'errmsg':'查询数据哭出错'})

        if not res:
            return Response({'errmsg':'短信验证码过期'})

        if smscode != res.decode():
            return Response({'errmsg':'验证码错误'})

        # 验证手机号是否已存在
        count = User.objects.filter(mobile=mobile).count()

        if count != 1:
            return Response({'errmsg': '手机号未注册'})
        md5 = hashlib.md5()
        md5.update(password.encode())
        passwd = md5.hexdigest()

        try:
            user = User.objects.filter(mobile=mobile).first()
            user.password =passwd
            user.save()
        except:
            return Response({'errmsg':'保存数据失败'})

        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        data = {'errmsg': 'OK',
                'data': {'token': token,
                         'username': user.username,
                         'user_id': user.id,
                         'avatar_url': user.avatar_url
                         }}

        return Response(data)
