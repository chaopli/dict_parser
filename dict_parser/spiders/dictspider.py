# -*- coding: utf-8 -*-
import scrapy
import codecs
import os


class DictspiderSpider(scrapy.Spider):
    name = "dictspider"
    allowed_domains = ["www.baus-ebs.org"]
    start_urls = ['http://www.baus-ebs.org/fodict_online/dict_list.asp?dictid=1&offset=0&page_count=50']

    def __init__(self):
        super(DictspiderSpider, self).__init__()
        os.remove('./tdict.txt')

    def parse(self, response):
        words = response.selector.xpath('//tr/td/a/text()').extract()
        with codecs.open('./tdict.txt', 'a', encoding='utf-8') as f:
            for word in words:
                f.write(word)
        next_page = response.selector.xpath(u'//a[text()="下頁"]/@href').extract()
        if next_page:
            yield scrapy.Request('/'.join(response.url.split('/')[:-1])+'/'+next_page[0], self.parse)
