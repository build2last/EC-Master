# coding:utf-8

from django.db import models


class Goods(models.Model):
    item_id = models.CharField(max_length=100, null=False, primary_key=True)
    title = models.CharField(max_length=200, null=False)
    platform = models.CharField(max_length=50, null=False)
    category = models.TextField(null=True, default = ' ')
    detail = models.TextField(null=True, default = ' ')

class Comment(models.Model):
    """11 elements"""
    class Meta:
        ordering=['-date']
        verbose_name="商品评论"
    rev_id = models.CharField(max_length=150, null=False, unique=True)
    item_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    content = models.TextField(null=True, default =' ')
    author = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(null=True)
    rating = models.FloatField(null=True)							# 评论满意度打分，一分制
    platform = models.CharField(max_length=50, null=True)
    key_words = models.CharField(max_length=100, null=True)


