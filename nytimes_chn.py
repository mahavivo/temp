#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

home_url = 'https://cn.nytimes.com'

def html_downloader(url):
    res = requests.get(url).text
    return res

def html_parser(html):
    articles = []
    soup = BeautifulSoup(html, 'lxml')
    article_list = soup.find_all(class_="regularSummaryHeadline")
    for article in article_list:
        article_link = article.find('a')['href']
        real_link = home_url + article_link
        articles.append(real_link)
    
    page_next = soup.find(class_="pagination").find(class_="next").find('a')
    if page_next:
        page_next = home_url + page_next['href']
        return articles, page_next
    else:
        return articles, None

def make_article(url):
    article = {}

    html = html_downloader(url)
    soup = BeautifulSoup(html, 'lxml')

    header_chn = soup.find(class_="article-header").find("header").find('h1').get_text()
    article['header_chn'] = header_chn
    header_eng = soup.find(class_="article-header").find("header").find(class_="en-title").get_text()
    article['header_eng'] = header_eng
    author = soup.find(class_="byline-box").find('address').get_text()
    article['author'] = author
    pub_date = soup.find(class_="byline-box").find('time').get_text()
    article['pub_date'] = pub_date
    author_info = soup.find(class_="author-info").get_text()
    article['author_info'] = author_info

    content = []
    para_list = soup.find_all(class_="article-paragraph")
    for para in para_list:
        paragraph = para.get_text()
        content.append(paragraph)

    article['content'] = '\n'.join(content)

    return article

def save_article(codict):
    file_name = codict['header_chn']
    file_name = re.sub(r'[\\/:*?"<>|\r\n]+', '_', file_name)
    whole_content = codict['header_chn'] + '\n' + codict['header_eng'] + '\n' + codict['author'] + '\n' + \
                    codict['pub_date'] + '\n' + codict['content'] + '\n' + codict['author_info']

    with open('%s.txt' % file_name, 'w', encoding='utf-8') as f:
        f.write(whole_content)


def main():
    url = home_url + '/books/1/'
    while url:
        html = html_downloader(url)
        links, url = html_parser(html)
        for link in links:
            link = link + 'dual/'
            content = make_article(link)
            save_article(content)


if __name__ == '__main__':
    main()
