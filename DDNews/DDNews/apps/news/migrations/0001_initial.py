# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-11 08:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('content', models.CharField(max_length=200, verbose_name='评论内容')),
                ('like', models.IntegerField(default=0, verbose_name='点赞数')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否展示')),
            ],
            options={
                'db_table': 'tb_comment',
                'verbose_name': '评论信息表',
                'verbose_name_plural': '评论信息表',
            },
        ),
        migrations.CreateModel(
            name='Comment_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('reason', models.CharField(max_length=200, verbose_name='举报原因')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=256, verbose_name='新闻标题')),
                ('source', models.CharField(max_length=64)),
                ('index_image_url', models.ImageField(null=True, upload_to='', verbose_name='新闻索引图片路径')),
                ('index_image_url_list', models.ImageField(null=True, upload_to='', verbose_name='新闻索引图片路径')),
                ('digest', models.CharField(max_length=256, null=True, verbose_name='新闻简要')),
                ('content', models.TextField(verbose_name='新闻内容')),
                ('clicks', models.IntegerField(default=0, verbose_name='文章点击数')),
                ('status', models.SmallIntegerField(choices=[(0, '审核通过'), (1, '审核中'), (2, '审核不通过')], default=0, verbose_name='文章审核状态')),
                ('reason', models.CharField(max_length=256, verbose_name='审核不通过原因')),
                ('report_time', models.DateTimeField(verbose_name='发布时间')),
                ('digest_label', models.CharField(max_length=256, verbose_name='新闻关键字')),
            ],
            options={
                'db_table': 'tb_news',
                'verbose_name': '新闻表',
                'verbose_name_plural': '新闻表',
            },
        ),
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='新闻分类')),
            ],
            options={
                'db_table': 'tb_news_category',
                'verbose_name': '新闻分类',
                'verbose_name_plural': '新闻分类',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='用户昵称')),
                ('avatar_url', models.CharField(max_length=256, verbose_name='用户头像路径')),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='用户手机号')),
                ('password', models.CharField(db_column='password_hash', max_length=128, verbose_name='用户密码')),
                ('email', models.CharField(max_length=128, null=True, verbose_name='用户邮箱')),
                ('signature', models.CharField(max_length=50, null=True, verbose_name='用户签名')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='用户性别')),
                ('is_active', models.BooleanField(default=False, verbose_name='用户邮箱绑定状态')),
                ('is_admin', models.BooleanField(default=False, verbose_name='是否是管理员')),
            ],
            options={
                'db_table': 'tb_user',
                'verbose_name': '用户user',
                'verbose_name_plural': '用户user',
            },
        ),
        migrations.CreateModel(
            name='User_Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News', verbose_name='新闻id')),
            ],
            options={
                'db_table': 'tb_user_collection',
                'verbose_name': '用户收藏表',
                'verbose_name_plural': '用户收藏表',
            },
        ),
        migrations.CreateModel(
            name='Comment_Relation',
            fields=[
                ('commenter', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='commenter', serialize=False, to='news.Comment', verbose_name='评论信息父id')),
            ],
            options={
                'db_table': 'tb_comment_relation',
                'verbose_name': '评论关系表',
                'verbose_name_plural': '评论关系表',
            },
        ),
        migrations.CreateModel(
            name='User_Fans',
            fields=[
                ('follow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='follows', serialize=False, to='news.User', verbose_name='关注')),
            ],
            options={
                'db_table': 'tb_user_fans',
                'verbose_name': '用户关注表',
                'verbose_name_plural': '用户关注表',
            },
        ),
        migrations.AddField(
            model_name='user_collection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.User', verbose_name='用户id'),
        ),
        migrations.AddField(
            model_name='user',
            name='collect_new',
            field=models.ManyToManyField(related_name='collected_user', through='news.User_Collection', to='news.News'),
        ),
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='news.NewsCategory', verbose_name='新闻分类'),
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='news.User', verbose_name='作者id'),
        ),
        migrations.AddField(
            model_name='comment_report',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Comment', verbose_name='评论id'),
        ),
        migrations.AddField(
            model_name='comment_report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.User', verbose_name='举报用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='new',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News', verbose_name='评论的新闻'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.User', verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='user_fans',
            name='fan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fans', to='news.User', verbose_name='粉丝'),
        ),
        migrations.AddField(
            model_name='comment_relation',
            name='new',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News', verbose_name='评论的新闻'),
        ),
        migrations.AddField(
            model_name='comment_relation',
            name='replier',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='replier', to='news.Comment', verbose_name='回复评论信息id'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_content',
            field=models.ManyToManyField(through='news.Comment_Relation', to='news.Comment'),
        ),
    ]
