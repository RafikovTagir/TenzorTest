# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
import os
import textwrap

from urllib.parse import urlparse
from html.parser import HTMLParser


URL = "https://lenta.ru/news/2021/11/20/surkov/"
URL = "https://lenta.ru/news/2015/12/15/american/"
URL = "https://svtv.org/news/2021-11-23/v-kazani-fsb-zadierzhala-podrostka-kotoryi-iakoby-ghotovil-skulshutingh/"
URL = "https://lenta.ru/articles/2021/11/23/megatoad/"
URL = "https://www.vesti.ru/hitech/article/2644748"
URL = "https://www.gazeta.ru/sport/2021/11/26/a_14247133.shtml"
URL = "https://www.gazeta.ru/politics/news/2021/11/26/n_16921087.shtml"

if URL[-1] == "/":
    URL = URL[0:-1]
u = urlparse(URL)
Filename = u.netloc + u.path

Black_List_Tag = {"script"}
White_List_Tag = {"p", "title"}


def is_inside_footer(tag, attrs):
    if tag == "div":
        for name, value in attrs:
            if name == "class":
                if value.find("footer") > 0:
                    return True
    return False


class MyHtmlParser(HTMLParser):

    to_write = False
    inside_white_list_tag = False
    _inside_footer = False
    result_string = ""
    #p_tag_encountered = False
    a_tag_encountered = False
    a_tag_href = ""
    paragraph_needed = False
    hyperlink_needed = False
    _current_paragraph = ""
    _list_of_paragraph = []

    def list_of_paragraph_getter(self):
        return self._list_of_paragraph

    def is_inside_white_list_tag(self, current_tag=""):
        if current_tag in White_List_Tag:
            self.to_write = True
        if self.to_write:
            return True
        else:
            return False

    def handle_starttag(self, tag, attrs):
        if is_inside_footer(tag, attrs):
            self._inside_footer = True
        else:
            if tag in White_List_Tag:
                self.inside_white_list_tag = True
            if self.inside_white_list_tag:
                if tag == "p":
                    self.paragraph_needed = True
                if tag == "a":
                    self.a_tag_encountered = True
                    for name, value in attrs:
                        if name == "href":
                            self.a_tag_href = f" [{value}]"

    def handle_endtag(self, tag):
        if self.inside_white_list_tag:
            if tag == "a" and self.a_tag_encountered:
                self.a_tag_encountered == False
                self.hyperlink_needed = True
            if tag == "p":
                self._list_of_paragraph.append(self._current_paragraph)
                self._current_paragraph = ""
            if tag in White_List_Tag:
                self.inside_white_list_tag = False

    def handle_data(self, data):
        if not self._inside_footer:                     #По хорошему надо проверять не закончился ли футер, но с чего бы вдруг после футера будет идти хоть что-то важное?
            if self.inside_white_list_tag:
                if self.paragraph_needed:
                    self._current_paragraph += "\n\n"
                    self.paragraph_needed = False
                if self.hyperlink_needed:
                    self._current_paragraph += self.a_tag_href
                    self.hyperlink_needed = False
                print("Encountered some data  :", data)
                self._current_paragraph += data


if __name__ == '__main__':
    text_of_page = requests.get(URL).text

parser = MyHtmlParser()
parser.feed(text_of_page)

output_string = ""
formatted_string = ""

for paragraph in parser.list_of_paragraph_getter():
    output_string += textwrap.fill(paragraph, 80, replace_whitespace= False)


if not os.path.exists(Filename):
    os.makedirs(Filename)
with open(Filename + ".txt", 'w', encoding='utf-8') as f:
    f.write(output_string)
with open(Filename + "RAW.txt", 'w', encoding='utf-8') as f:
    f.write(text_of_page)
