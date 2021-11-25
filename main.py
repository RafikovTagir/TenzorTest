# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
import os

from urllib.parse import urlparse
from html.parser import HTMLParser


URL = "https://lenta.ru/news/2021/11/20/surkov/"
URL = "https://lenta.ru/news/2015/12/15/american/"
URL = "https://svtv.org/news/2021-11-23/v-kazani-fsb-zadierzhala-podrostka-kotoryi-iakoby-ghotovil-skulshutingh/"
URL = "https://lenta.ru/articles/2021/11/23/megatoad/"


u = urlparse(URL)
Filename = u.netloc + u.path[0:-1]

Black_List_Tag = {"script"}
White_List_Tag = {"p", "title"}


class MyHtmlParser(HTMLParser):

    to_write = False
    inside_white_list_tag = False
    result_string = ""
    #p_tag_encountered = False
    a_tag_encountered = False
    a_tag_href = ""
    paragraph_needed = False
    hyperlink_needed = False

    def is_inside_white_list_tag(self, current_tag=""):
        if current_tag in White_List_Tag:
            self.to_write = True
        if self.to_write:
            return True
        else:
            return False

    def handle_starttag(self, tag, attrs):
        if tag in White_List_Tag:
            self.inside_white_list_tag = True
        if self.inside_white_list_tag:
            if tag == "p":
                self.paragraph_needed = True
            if tag == "a":
                self.a_tag_encountered = True
                for name, value in attrs:
                    if name == "href":
                        self.a_tag_href = " [" + value + "]"


    def handle_endtag(self, tag):
        if self.inside_white_list_tag:
            if tag == "a" and self.a_tag_encountered:
                self.a_tag_encountered == False
                self.hyperlink_needed = True
            if tag in White_List_Tag:
                self.inside_white_list_tag = False

    def handle_data(self, data):
        if self.inside_white_list_tag:
            if self.paragraph_needed:
                self.result_string += "\n\n"
                self.paragraph_needed = False
            if self.hyperlink_needed:
                self.result_string += self.a_tag_href
                self.hyperlink_needed = False
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
