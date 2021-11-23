# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
import os

from urllib.parse import urlparse
from html.parser import HTMLParser


URL = "https://lenta.ru/news/2021/11/20/surkov/"
URL = "https://lenta.ru/news/2015/12/15/american/"
URL = "https://lenta.ru/articles/2021/11/23/megatoad/"
URL = "https://svtv.org/news/2021-11-23/v-kazani-fsb-zadierzhala-podrostka-kotoryi-iakoby-ghotovil-skulshutingh/"
u = urlparse(URL)
Filename = u.netloc + u.path[0:-1]

Black_List_Tag = {"script"}
White_List_Tag = {"p"}


class MyHtmlParser(HTMLParser):

    to_write = False
    result_string = ""

    def handle_starttag(self, tag, attrs):
        if tag in White_List_Tag:
            self.to_write = True

    def handle_endtag(self, tag):
        if tag in White_List_Tag:
            self.to_write = False

    def handle_data(self, data):
        if self.to_write:
            print("Encountered some data  :", data)
            self.result_string += data


if __name__ == '__main__':
    text_of_page = requests.get(URL).text

parser = MyHtmlParser()
parser.feed(text_of_page)

#parser.result_string

if not os.path.exists(Filename):
    os.makedirs(Filename)
with open(Filename + ".txt", 'w', encoding='utf-8') as f:
    f.write(parser.result_string)
with open(Filename + "RAW.txt", 'w', encoding='utf-8') as f:
    f.write(text_of_page)
