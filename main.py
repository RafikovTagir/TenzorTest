# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
import os
import textwrap
import sys

from urllib.parse import urlparse
from html.parser import HTMLParser


URL = "https://lenta.ru/news/2021/11/20/surkov/"
URL = "https://lenta.ru/news/2015/12/15/american/"
URL = "https://svtv.org/news/2021-11-23/v-kazani-fsb-zadierzhala-podrostka-kotoryi-iakoby-ghotovil-skulshutingh/"
URL = "https://www.vesti.ru/hitech/article/2644748"
URL = "https://www.gazeta.ru/sport/2021/11/26/a_14247133.shtml"
URL = "https://www.gazeta.ru/politics/news/2021/11/26/n_16921087.shtml"
URL = "https://www.gazeta.ru/auto/2019/06/11_a_12407929.shtml"
URL = "https://lenta.ru/articles/2021/11/23/megatoad/"
URL = "https://svtv.org/news/2021-11-28/chtoby-nie-obidiet-ghlavu-kitaia-voz-propustila-ghriechieskuiu-bukvu-pri-vyborie-nazvaniia-novogho-shtamma/"
URL = "https://expert.ru/2021/11/28/umer-aleksandr-gradskiy/"
URL = "https://expert.ru/ural/2021/47/apokalipsisa-ne-sluchilos/"
URL = "https://news.rambler.ru/world/47660957-smi-bayden-ne-hochet-vvodit-sanktsii-protiv-severnogo-potoka-2/"
URL = "https://regnum.ru/news/economy/3433510.html"
URL = "https://vz.ru/news/2021/11/28/1131397.html"
URL = "https://vz.ru/news/2021/11/28/1131399.html"
URL = "https://ria.ru/20211128/obschestvo-1761102268.html"
URL = "https://zona.media/article/2021/11/26/nft"

if URL[-1] == "/":
    URL = URL[0:-1]
u = urlparse(URL)
Filename = u.netloc + u.path

Black_List_Tag = {"script"}
White_List_Tag = {"p", "title", "h1"}


def is_inside_footer(tag, attrs):
    if tag == "div":
        for name, value in attrs:
            if name == "class":
                if value.find("footer") > 0:
                    return True
    return False


class MyHtmlParser(HTMLParser):

    _inside_white_list_tag = False
    _inside_footer = False
    _result_string = ""
    _a_tag_encountered = False
    _a_tag_href = ""
    _hyperlink_needed = False
    _current_paragraph = ""
    _list_of_paragraph = []
    _massive_for_counters_of_tags = {}

    def list_of_paragraph_getter(self):
        return self._list_of_paragraph

    def handle_starttag(self, tag, attrs):
        if is_inside_footer(tag, attrs):
            self._inside_footer = True
        else:
            if tag in White_List_Tag:
                self._inside_white_list_tag = True
            if self._inside_white_list_tag:
                if tag == "a":
                    for name, value in attrs:
                        if name == "href":
                            self._a_tag_href = f" [{value}]"

    def handle_endtag(self, tag):
        if self._inside_white_list_tag:
            if tag == "a":
                self._hyperlink_needed = True
            if tag in White_List_Tag:
                self._list_of_paragraph.append(self._current_paragraph)
                self._current_paragraph = ""
                self._inside_white_list_tag = False

    def handle_data(self, data):
        if not self._inside_footer:                     #По хорошему надо проверять не закончился ли футер, но с чего бы вдруг после футера будет идти хоть что-то важное?
            if self._inside_white_list_tag:
                if self._hyperlink_needed:
                    self._current_paragraph += self._a_tag_href
                    self._hyperlink_needed = False
                self._current_paragraph += data
                print("Encountered some data  :", data)

if __name__ == '__main__':
    text_of_page = requests.get(URL).text

parser = MyHtmlParser()
parser.feed(text_of_page)

output_string = ""
formatted_string = ""

for paragraph in parser.list_of_paragraph_getter():
    output_string += textwrap.fill(paragraph, 80, replace_whitespace=False) + "\n\n"


if not os.path.exists(Filename):
    os.makedirs(Filename)
with open(Filename + ".txt", 'w', encoding='utf-8') as f:
    f.write(output_string)
with open(Filename + "RAW.txt", 'w', encoding='utf-8') as f:
    f.write(text_of_page)
