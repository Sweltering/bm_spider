# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    rules = (
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65.+"), callback="parse_page", follow=True),
    )

    def parse_page(self, response):
        category = response.xpath("//div[@class='uibox']/div/text()").get()  # 分类标题
        srcs = response.xpath("//div[contains(@class, 'uibox-con')]/ul/li//img/@src").getall()  # 图片地址
        # srcs = list(map(lambda x: x.replace("t_", ""), srcs))  # 高清图的地址内没有t_
        # srcs = list(map(lambda x: response.urljoin(x), srcs))  # 补齐url(加上https)
        srcs = list(map(lambda x: response.urljoin(x.replace("t_", "")), srcs))
        yield BmwItem(category=category, image_urls = srcs)



    # 没有使用CrawlSpider规则解析参数
    # def parse(self, response):
    #     uiboxs = response.xpath("//div[@class='uibox']")[1:]  # 汽车图片的类别标签
    #     for uibox in uiboxs:
    #         category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()  # 图片类别
    #         urls = uibox.xpath(".//ul/li/a/img/@src").getall()  # 所有的图片链接
    #         # for url in urls:
    #         #     url = response.urljoin(url)  # 拼接成完成的url（前面加上了https）
    #         #     print(url)
    #         urls = list(map(lambda url: response.urljoin(url), urls))
    #         item = BmwItem(category=category, image_urls=urls)
    #         yield item
