# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bmw import settings


class BmwPipeline(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")  # 项目根目录
        if not os.path.exists(self.path):  # 判断images文件夹是否存在
            os.mkdir(self.path)  # 创建images文件夹

    # 自己实现下载图片（效率不高，可使用下面的scrapy提供的方法ImagesPipeline）
    def process_item(self, item, spider):
        category = item["category"]
        urls = item["urls"]

        category_path = os.path.join(self.path, category)  # 图片的分类目录
        if not os.path.exists(category_path):
            os.mkdir(category_path)  # 创建分类目录

        for url in urls:
            image_name = url.split("_")[-1]  # 图片名
            request.urlretrieve(url, os.path.join(category_path, image_name))  # 下载图片

        return item


# 使用scrapy提供的图片下载，重写ImagesPipeline的file_path和get_media_requests方法，将图片按自己指定的分类下载
class BMWImagesPipeline(ImagesPipeline):
    # 在发送下载请求之前调用，这个方法就是发送下载请求的
    def get_media_requests(self, item, info):
        request_objs = super(BMWImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    # 在图片在将要被存储的时候调用，获取这个图片存储的路径
    def file_path(self, request, response=None, info=None):
        path = super(BMWImagesPipeline, self).file_path(request, response, info)
        category = request.item.get("category")
        images_store = settings.IMAGES_STORE  # images文件夹路径
        category_path = os.path.join(images_store, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)  # 创建图片分类的文件夹

        image_name = path.replace("full/", "")  # 图片名字
        image_path = os.path.join(category_path, image_name)  # 图片路径
        return image_path


