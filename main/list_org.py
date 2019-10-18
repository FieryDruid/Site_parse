import requests
from lxml import html
import os

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

class SiteData:
    def __init__(self, url):
        self.url = url
        self.get_data()

    def get_data(self):
        request = requests.get(self.url, headers = headers)
        with open('site.html', 'w', encoding='utf-8') as file:
            file.write(request.text)
            file.close()

    def import_html(self):
        with open('site.html', 'r', encoding='utf-8') as file:
            self.html = html.fromstring(file.read())
            file.close()
        os.remove('site.html')

    def data_parse(self):
        self.company_name = self.html.xpath('//div[@class = "c2m"]/p/a/text()')[0]
        self.leader = self.html.xpath('//div[@class = "c2m"]/table/tr/td/a/text()')[0]
        try:
            self.status = self.html.xpath('//div[@class = "c2m"]/table/tr[7]/td/text()')[0]
        except:
            print("Не указана численность персонала")
            self.date = self.html.xpath('//div[@class = "c2m"]/table/tr[5]/td/text()')[0]
            self.status = self.html.xpath('//div[@class = "c2m"]/table/tr[6]/td/text()')[0]
        else:
            self.date = self.html.xpath('//div[@class = "c2m"]/table/tr[6]/td/text()')[0]
        finally:
            self.inn_kpp =  self.html.xpath('//div[@class = "c2m"]/table/tr[2]/td/text()')[0]
            self.ogrn = self.html.xpath('//div[@class = "c2m"]/p[4]/text()')[0][1:]

        print(f'Полное юридическое наименование: {self.company_name}')
        print(f'Руководитель: {self.leader}')
        print(f'Дата регистрации: {self.date}')
        print(f'Статус: {self.status}')
        print(f'ИНН / КПП: {self.inn_kpp}')
        print(f'ОГРН: {self.ogrn}')


new_site = SiteData(input('Введите ссылку на компанию с ресурса list-org.com: '))
new_site.import_html()
new_site.data_parse()