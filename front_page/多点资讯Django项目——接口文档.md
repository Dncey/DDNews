# ---接口文档

- 本项目接口遵循 RESTful 设计风格
- 请求需要携带 csrf_token
- 无基本参数
- 基本返回内容如下：

```
{
    "errno": "0",
    "errmsg": "ok"
}
```

### 错误代码说明

**错误返回值格式：**

```
{
    "errno": "4101",
    "errmsg": "用户未登录"
}
```

| 错误代码 | 错误信息   | 详情描述               |
| -------- | ---------- | ---------------------- |
| 0        | OK         | 成功                   |
| 4001     | DBERR      | 数据库查询错误         |
| 4002     | NODATA     | 无数据                 |
| 4003     | DATAEXIST  | 数据已存在             |
| 4004     | DATAERR    | 数据错误               |
| 4101     | SESSIONERR | 用户未登录             |
| 4102     | LOGINERR   | 用户登录失败           |
| 4103     | PARAMERR   | 参数错误               |
| 4104     | USERERR    | 用户不存在或未激活     |
| 4105     | ROLEERR    | 用户身份错误           |
| 4106     | PWDERR     | 密码错误               |
| 4201     | REQERR     | 非法请求或请求次数受限 |
| 4202     | IPERR      | IP受限                 |
| 4301     | THIRDERR   | 第三方系统错误         |
| 4302     | IOERR      | 文件读写错误           |
| 4500     | SERVERERR  | 内部错误               |
| 4501     | UNKOWNERR  | 未知错误               |



# 1.登录注册模块

- 获取图片验证码
- 获取短信验证码
- 注册
- 登录
- 判断是否登录
- 退出登录



## 1.1获取图片验证码

### URL

/img_code?code_id=uuid

### 请求方式

GET

### 请求参数

| 参数名      | 必选  | 类型 | 说明             |
| ----------- | ----- | ---- | ---------------- |
| imageCodeId | true  | str  | 验证码编号(uuid) |


### 返回结果

image







##1.2获取短信验证码

### URL

/passport/sendSMSCode/

### 请求方式

POST

### 支持格式

JSON

### 请求参数

| 参数名      | 必选 | 类型 | 说明                 |
| ----------- | ---- | ---- | -------------------- |
| mobile      | true | str  | 手机号               |
| imageCodeId | true | str  | 图形验证码编号(uuid) |
| imageCode   | true | str  | 图片验证码内容       |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "发送成功"
}
```



## 1.3注册



### URL

/passport/register/

### 请求方式

POST

### 支持格式

JSON

### 请求参数

| 参数名   | 必选 | 类型 | 说明       |
| -------- | ---- | ---- | ---------- |
| mobile   | true | str  | 手机号     |
| sms_code | true | str  | 短信验证码 |
| password | true | str  | 密码       |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "注册成功"
}
```



## 1.4登陆



### URL

/passport/login/

### 请求方式

POST

### 支持格式

JSON

### 请求参数

| 参数名   | 必选 | 类型 | 说明   |
| -------- | ---- | ---- | ------ |
| lgoin_text  | true | str  | 手机号/用户名/邮箱 |
| password | true | str  | 密码   |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "登录成功"
}
```





##1.5获取登录状态（模板判断是否有用户信息）

### URL

/passport/session

### 请求方式

GET

### 请求参数

无

### 返回结果

```
// 已登录：
{
    "errno": "0",
    "errmsg": "OK",
    "data": {
        "name": "用户名"，
        "user_id": "用户id"
    }
}
// 未登录：
{
    "errno": "4101",
    "errmsg": "未登录"
}
```





##1.6退出登录

### URL

/passport/logout

### 是否需要登录

是

### 请求方式

DELETE

### 请求参数

无

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK"
}
```

##1.7忘记密码

### URL

/passport/resetpwd/

### 是否需要登录

否

### 请求方式

post

### 请求参数

| 参数名   | 必选 | 类型 | 说明   |
| -------- | ---- | ---- | ------ |
| mobile   | true | str  | 手机号 |
| smscode   | true | str  | 短信验证码 |
| password | true | str  | 密码   |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK"
}
```



# 2.用户中心

- 个人中心
- 上传个人头像
- 用户名修改
- 用户实名认证



## 2.1获取用户信息



### URL

/api/v1.0/user

### 是否需要登录

是

### 请求方式

GET

### 请求参数

无

### 返回结果

```
{
    "data": {
        "avatar_url": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS",
        "mobile": "18599998888",
        "name": "哈哈哈哈哈哈"
    },
    "errmsg": "OK",
    "errno": "0"
}
```

### 返回字段说明

| 返回值字段 | 类型 | 字段说明     |
| ---------- | ---- | ------------ |
| avatar_url | str  | 用户头像地址 |
| mobile     | str  | 用户手机     |
| name       | str  | 用户昵称     |



## 2.2用户名修改

### URL

/api/v1.0/user/name

### 是否需要登录

是

### 请求方式

POST

### 支持格式

JSON

### 请求参数

| 参数名 | 必选 | 类型 | 说明   |
| ------ | ---- | ---- | ------ |
| name   | true | str  | 用户名 |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK"
}
```





##2.3上传个人头像



### URL

/api/v1.0/user/avatar

### 是否需要登录

是

### 请求方式

POST

### 请求参数

| 参数名 | 必选 | 类型 | 说明     |
| ------ | ---- | ---- | -------- |
| avatar | true | file | 头像文件 |

### 返回结果

```
{
    "data": {
        "avatar_url": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS"
    },
    "errno": "0",
    "errmsg": "OK"
}
```

### 返回字段说明

| 返回值字段 | 类型 | 字段说明                 |
| ---------- | ---- | ------------------------ |
| avatar_url | str  | 用户上传成功后的头像地址 |





## 2.4获取用户实名信息

### URL

/api/v1.0/user/auth

### 是否需要登录

是

### 请求方式

GET

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK"
    "data": {"real_name":用户真实姓名，
    		"id_card":身份证号
    }
}
```

###返回字段说明

| 参数名    | 必选 | 类型 | 说明           |
| --------- | ---- | ---- | -------------- |
| real_name | true | str  | 用户真实姓名   |
| id_card   | true | str  | 用户身份证号码 |

### 

##2.5设置用户实名信息

### URL

/api/v1.0/user/auth

### 是否需要登录

是

### 请求方式

POST

### 支持格式

JSON

### 请求参数

| 参数名    | 必选 | 类型 | 说明           |
| --------- | ---- | ---- | -------------- |
| real_name | true | str  | 用户真实姓名   |
| id_card   | true | str  | 用户身份证号码 |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK"
}
```



#3.新闻模块

- 新闻搜索
- 新闻分类
- 新闻列表
- 新闻详情页面
- 新闻发布
- 新闻审核
- 新闻排行
- 精选新闻



## 3.1 新闻搜索



### URL

/search.html/?title=xxxx

### 是否需要登录

否

### 请求方式

GET

### 请求参数

title

### 返回结果

```
{
    "data": [
            {
                "address": "地址地址",
                "area_name": "东城区",
                "ctime": "2017-11-12",
                "house_id": 5,
                "img_url": "http://oyucyko3w.bkt.clouddn.com/FhxrJOpjswkGN2bUgufuXPdXcV6w",
                "order_count": 0,
                "price": 10000,
                "room_count": 1,
                "title": "我是房屋标题",
                "user_avatar": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS"
            },
            {
                "address": "1111",
                "area_name": "东城区",
                "ctime": "2017-11-12",
                "house_id": 6,
                "img_url": "http://oyucyko3w.bkt.clouddn.com/FkVQ8OMKcjjtyF6jqlIl7GCH1CbG",
                "order_count": 0,
                "price": 19000,
                "room_count": 1,
                "title": "测试房屋3",
                "user_avatar": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS"
            }
        ]
    ,
    "errmsg": "ok",
    "errno": "0"
}
```

### 返回字段说明

- data

| 返回值字段 | 类型  | 字段说明 |
| ---------- | ----- | -------- |
| houses     | array | 房屋列表 |

- houses

| 返回值字段  | 类型 | 字段说明           |
| ----------- | ---- | ------------------ |
| house_id    | int  | 房屋id             |
| order_count | int  | 订单数据           |
| title       | str  | 标题               |
| ctime       | str  | 创建时间           |
| price       | str  | 价格               |
| area_name   | int  | 城区名             |
| address     | str  | 房屋地址           |
| room_count  | int  | 房间数目           |
| img_urls    | str  | 房屋图片           |
| user_avatar | str  | 该房屋所有者的头像 |



## 3.2城区列表

### URL

/api/v1.0/areas

### 请求方式

GET

### 请求参数

无

### 返回结果

```
{
    "errmsg": "OK",
    "errno": "0",
    "data": [
        {
            "aid": 1,
            "aname": "东城区"
        },
        {
            "aid": 2,
            "aname": "西城区"
        },
        {
            "aid": 3,
            "aname": "朝阳区"
        }
    ]
}
```

### 返回字段说明

| 返回值字段 | 类型 | 字段说明 |
| ---------- | ---- | -------- |
| aid        | int  | 城区id   |
| aname      | int  | 城区名字 |



##3.3发布房源

### URL

/api/v1.0/houses

### 是否需要登录

是

### 请求方式

POST

### 支持格式

JSON

### 请求参数

| 参数名     | 必选 | 类型  | 说明                                 |
| ---------- | ---- | ----- | ------------------------------------ |
| title      | true | str   | 标题                                 |
| price      | true | str   | 价格                                 |
| area_id    | true | int   | 城区id                               |
| address    | true | str   | 房屋地址                             |
| room_count | true | int   | 房间数目                             |
| acreage    | true | int   | 房屋面积                             |
| unit       | true | str   | 房屋单元，如：几室几厅               |
| capacity   | true | int   | 房屋容纳的人数                       |
| beds       | true | str   | 房屋床铺的配置                       |
| deposit    | true | str   | 房屋押金                             |
| min_days   | true | int   | 最少入住天数                         |
| max_days   | true | int   | 最大入住天数，0表示不限制            |
| facility   | true | array | 用户选择的设施信息id列表，如：[7, 8] |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK",
    "data": {
        "house_id": 1
    }
}
```

### 返回字段说明

| 返回值字段 | 类型 | 字段说明 |
| ---------- | ---- | -------- |
| house_id   | int  | 房屋id   |

## 3.4上传房源图片



### URL

/api/v1.0/houses/\<int:house_id>/images

### 是否需要登录

是

### 请求方式

POST

### 请求参数

| 参数名      | 必选 | 类型 | 说明     |
| ----------- | ---- | ---- | -------- |
| house_image | true | file | 图片文件 |

### 返回结果

```
{
    "data": {
        "url": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS"
    },
    "errno": "0",
    "errmsg": "OK"
}
```

### 返回字段说明

| 返回值字段 | 类型 | 字段说明                     |
| ---------- | ---- | ---------------------------- |
| url        | str  | 用户上传成功后的房源图片地址 |





##3.5房屋详情页面



### URL

/api/v1.0/houses/\<int:house_id>

### 请求方式

GET

### 请求参数

无

### 返回结果

```
{
    "data": {
        "house": {
            "acreage": 5,
            "address": "我是地址",
            "beds": "5张床",
            "capacity": 5,
            "comments": [
                {
                    "comment": "哎哟不错哟",
                    "ctime": "2017-11-14 11:17:07",
                    "user_name": "匿名用户"
                }
            ],
            "deposit": 500,
            "facilities": [
                1
            ],
            "hid": 4,
            "img_urls": [
                "http://oyucyko3w.bkt.clouddn.com/FhgvJiGF9Wfjse8ZhAXb_pYObECQ",
                "http://oyucyko3w.bkt.clouddn.com/FkagyA8TiuxnLsz7ofLfA_CY34Nw"
            ],
            "max_days": 5,
            "min_days": 5,
            "price": 500,
            "room_count": 5,
            "title": "555",
            "unit": "5",
            "user_avatar": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS",
            "user_id": 1,
            "user_name": "哈哈哈哈哈哈"
        },
        "user_id": 1
    },
    "errmsg": "OK",
    "errno": "0"
}
```

### 返回字段说明

- data

| 返回值字段 | 类型 | 字段说明                                    |
| ---------- | ---- | ------------------------------------------- |
| user_id    | int  | 当前登录用户的用户id，如果没有登录，则为 -1 |
| house      | dict | 房屋详细信息                                |

- house

| 返回值字段  | 类型  | 字段说明                   |
| ----------- | ----- | -------------------------- |
| acreage     | int   | 房屋面积                   |
| title       | str   | 标题                       |
| price       | str   | 价格                       |
| area_id     | int   | 城区id                     |
| address     | str   | 房屋地址                   |
| room_count  | int   | 房间数目                   |
| unit        | str   | 房屋单元，如：几室几厅     |
| capacity 是 | int   | 房屋容纳的人数             |
| beds        | str   | 房屋床铺的配置             |
| deposit     | str   | 房屋押金                   |
| min_days    | int   | 最少入住天数               |
| max_days    | int   | 最大入住天数，0表示不限制  |
| facility    | array | 设施信息id列表，如：[7, 8] |
| comments    | array | 该房屋的评论列表           |
| img_urls    | array | 房屋图片列表               |
| user_avatar | str   | 该房屋所有者的头像         |
| user_id     | str   | 该房屋所有者的用户id       |
| user_name   | str   | 该房屋所有者的昵称         |

- comments

| 返回值字段 | 类型 | 字段说明   |
| ---------- | ---- | ---------- |
| comment    | str  | 评论内容   |
| ctime      | str  | 评论时间   |
| user_name  | str  | 评论人昵称 |



##3.6首页房屋推荐展示



### URL

/api/v1.0/houses/index

### 请求方式

GET

### 请求参数

无

### 返回结果

```
{
    "data": [
        {
            "house_id": 4,
            "img_url": "http://oyucyko3w.bkt.clouddn.com/FhgvJiGF9Wfjse8ZhAXb_pYObECQ",
            "title": "555"
        },
        {
            "house_id": 5,
            "img_url": "http://oyucyko3w.bkt.clouddn.com/FhxrJOpjswkGN2bUgufuXPdXcV6w",
            "title": "我是房屋标题"
        },
        {
            "house_id": 6,
            "img_url": "http://oyucyko3w.bkt.clouddn.com/FkVQ8OMKcjjtyF6jqlIl7GCH1CbG",
            "title": "测试房屋3"
        }
    ],
    "errmsg": "OK",
    "errno": "0"
}
```

### 返回字段说明

| 返回值字段 | 类型 | 字段说明   |
| ---------- | ---- | ---------- |
| house_id   | int  | 房屋id     |
| img_url    | str  | 房屋主图片 |
| title      | str  | 房屋标题   |



##3.7 房屋数据搜索

### URL

/api/v1.0/houses

### 请求方式

GET

### 请求参数

| 参数名        | 必选  | 类型 | 说明                                                         |
| ------------- | ----- | ---- | ------------------------------------------------------------ |
| aid           | false | int  | 区域id                                                       |
| sd(start_day) | false | str  | 开始日期                                                     |
| ed(end_day)   | false | str  | 结束时间                                                     |
| sk(sort_key)  | false | str  | 排序方式 booking(订单量), price-inc(低到高), price-des(高到低) |
| p(page)       | false | int  | 页数，不传默认为1                                            |

### 返回结果

```
{
    "data": {
        "houses": [
            {
                "address": "1111",
                "area_name": "东城区",
                "ctime": "2017-11-12",
                "house_id": 6,
                "img_url": "http://oyucyko3w.bkt.clouddn.com/FkVQ8OMKcjjtyF6jqlIl7GCH1CbG",
                "order_count": 1,
                "price": 19000,
                "room_count": 1,
                "title": "测试房屋3",
                "user_avatar": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS"
            },
            {
                "address": "地址地址",
                "area_name": "东城区",
                "ctime": "2017-11-12",
                "house_id": 5,
                "img_url": "http://oyucyko3w.bkt.clouddn.com/FhxrJOpjswkGN2bUgufuXPdXcV6w",
                "order_count": 0,
                "price": 10000,
                "room_count": 1,
                "title": "我是房屋标题",
                "user_avatar": "http://oyucyko3w.bkt.clouddn.com/FmWZRObXNX6TdC8D688AjmDAoVrS"
            }
        ],
        "total_page": 2
    },
    "errmsg": "请求成功",
    "errno": "0"
}

### 返回字段说明
```

- data

| 返回值字段 | 类型  | 字段说明 |
| ---------- | ----- | -------- |
| total_page | int   | 总页数   |
| houses     | array | 房屋列表 |

- houses

| 返回值字段  | 类型 | 字段说明           |
| ----------- | ---- | ------------------ |
| house_id    | int  | 房屋id             |
| order_count | int  | 订单数据           |
| title       | str  | 标题               |
| ctime       | str  | 创建时间           |
| price       | str  | 价格               |
| area_name   | int  | 城区名             |
| address     | str  | 房屋地址           |
| room_count  | int  | 房间数目           |
| img_urls    | str  | 房屋图片           |
| user_avatar | str  | 该房屋所有者的头像 |





# 4.订单模块

- 添加订单
- 获取订单列表
- 接单和拒单
- 评价订单



## 4.1添加订单



### URL

/api/v1.0/orders

### 是否需要登录

是

### 请求方式

POST

### 请求参数

| 参数名     | 必选 | 类型 | 说明     |
| ---------- | ---- | ---- | -------- |
| house_id   | true | int  | 房屋id   |
| start_date | true | str  | 开始日期 |
| end_date   | true | str  | 结束时间 |

### 返回结果

```
{
    "data": {
        "order_id": 1
    },
    "errno": "0",
    "errmsg": "OK"
}
```

### 返回字段说明

| 返回值字段 | 类型 | 字段说明 |
| ---------- | ---- | -------- |
| order_id   | int  | 订单id   |



##4.2获取订单列表

### URL

/api/v1.0/orders

### 是否需要登录

是

### 请求方式

GET

### 请求参数

| 参数名 | 必选 | 类型 | 说明                                       |
| ------ | ---- | ---- | ------------------------------------------ |
| role   | true | str  | 角色类型：【custom: 房客，landlord：房东】 |

### 返回结果

```
{
    "data": {
        "orders": [
            {
                "amount": 1000,
                "comment": "哎哟不错哟",
                "ctime": "2017-11-14 09:59:35",
                "days": 2,
                "end_date": "2017-11-15",
                "img_url": "http://oyucyko3w.bkt.clouddn.com/FhgvJiGF9Wfjse8ZhAXb_pYObECQ",
                "order_id": 1,
                "start_date": "2017-11-14",
                "status": "COMPLETE",
                "title": "555"
            },
            {
                "amount": 20000,
                "comment": "不约",
                "ctime": "2017-11-14 10:59:12",
                "days": 2,
                "end_date": "2017-11-17",
                "img_url": "http://oyucyko3w.bkt.clouddn.com/FhxrJOpjswkGN2bUgufuXPdXcV6w",
                "order_id": 2,
                "start_date": "2017-11-16",
                "status": "REJECTED",
                "title": "我是房屋标题"
            }
        ]
    },
    "errmsg": "OK",
    "errno": "0"
}
```

### 返回字段说明

| 返回值字段 | 类型  | 字段说明 |
| ---------- | ----- | -------- |
| orders     | array | 订单列表 |

- orders

| 返回值字段 | 类型 | 字段说明             |
| ---------- | ---- | -------------------- |
| amount     | int  | 订单金额，以分为单位 |
| comment    | str  | 订单评论/拒单原因    |
| ctime      | str  | 创建时间             |
| days       | int  | 入住天数             |
| start_date | str  | 入住日期             |
| end_date   | str  | 离开日期             |
| img_url    | str  | 房屋图片地址         |
| order_id   | int  | 订单id               |
| status     | str  | 订单状态             |
| title      | str  | 房屋标题             |



## 4.3接单和拒单



### URL

/api/v1.0/orders

### 是否需要登录

是

### 请求方式

PUT

### 请求参数

| 参数名   | 必选  | 类型 | 说明                                     |
| -------- | ----- | ---- | ---------------------------------------- |
| action   | true  | str  | 操作类型：【accept: 接单，reject：拒单】 |
| order_id | true  | int  | 订单号                                   |
| reason   | false | str  | 拒单时，需要填写拒单原因                 |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK"
}
```





## 4.4评论订单



### URL

/api/v1.0/orders/comment

### 是否需要登录

是

### 请求方式

PUT

### 请求参数

| 参数名   | 必选 | 类型 | 说明     |
| -------- | ---- | ---- | -------- |
| comment  | true | str  | 评论内容 |
| order_id | true | int  | 订单号   |

### 返回结果

```
{
    "errno": "0",
    "errmsg": "OK"
}
```