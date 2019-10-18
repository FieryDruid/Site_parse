import requests
from lxml import html, etree
from math import ceil
import os

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

class SiteData:
    def __init__(self, count):
        self.url = "https://habr.com/ru/top/yearly/"
        self.data_dict = {}
        self.posts_count = int(count)
        self.page_count = ceil(self.posts_count/20)

        print(self.page_count)
        i = 1
        while i <= self.page_count:
            self.get_data(i)
            self.import_html(i)
            if self.posts_count<20 and self.posts_count > 0:
                self.data_parse(self.posts_count)
                break
            else:
                self.data_parse()
            self.posts_count -= 20
            i += 1


    def get_data(self, i):
        request = requests.get(f'{self.url}page{i}', headers = headers)
        with open(f'site_page{i}.html', 'w', encoding='utf-8') as file:
            file.write(request.text)
            file.close()

    def import_html(self, i):
        with open(f'site_page{i}.html', 'r', encoding='utf-8') as file:
            self.html = html.fromstring(file.read())
            file.close()
        os.remove(f'site_page{i}.html')


    def data_parse(self, posts_count = 20):
        self.title = self.html.xpath('//h2[@class= "post__title"]/a/text()')

        self.data = self.html.xpath('//div[@class="post__text post__text-html js-mediator-article"]')
        self.meta = self.html.xpath('//header[@class= "post__meta"]/span[@class= "post__time"]/text()')

        self.nickname = self.html.xpath('//span[@class= "user-info__nickname user-info__nickname_small"]/text()')
        i = 0
        temp_dict={}

        if posts_count != 20:
            for element in self.title:
                temp_dict[element] = [self.data[i].xpath('./text() |./img/@src | ./a/@href'), self.meta[i],
                                      self.nickname[i]]
                i += 1
                if i == posts_count:
                    break
        else:
            for element in self.title:
                temp_dict[element] = [self.data[i].xpath('./text() |./img/@src | ./a/@href'), self.meta[i],
                                      self.nickname[i]]
                i += 1
        self.data_dict.update(temp_dict)


        print(self.data_dict)


new_site = SiteData(input())
