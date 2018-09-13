#encoding: utf-8

import requests
from lxml import etree
import sqlite3
# 可以扩展为存储mysql

conn = sqlite3.connect('movie_site.db')
cursor = conn.cursor()

headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

proxies = {
    'http': ''
}

def parse_detail(detail_url):
    # response = requests.get(detail_url,headers=headers,proxies=proxies)
    # 可根据实际情况添加代理
    response = requests.get(detail_url,headers=headers)
    html = response.content.decode("gbk")
    parser = etree.HTML(html)
    movie = {}
    movie['title'] = parser.xpath("//font[@color='#07519a']/text()")[0]
    # xpath永远返回的是一个列表，所以想要获取这个zoom元素，
    # 应该要通过列表下标操作取出这个元素
    zoom = parser.xpath("//div[@id='Zoom']")[0]
    imgs = zoom.xpath(".//img/@src")
    movie['cover'] = imgs[0]
    movie['screenshoot'] = imgs[1]
    infos = zoom.xpath(".//text()")
    for info in infos:
        if info.startswith("◎年　　代"):
            info = info.replace("◎年　　代","").strip()
            movie['year'] = info
        elif info.startswith("◎产　　地"):
            info = info.replace("◎产　　地","").strip()
            movie['country'] = info
        elif info.startswith("◎类　　别"):
            info = info.replace("◎类　　别",'').strip()
            movie['category'] = info
        elif info.startswith("◎片　　长"):
            info = info.replace("◎片　　长",'').strip()
            movie['duration'] = info
        elif info.startswith("◎导　　演"):
            info = info.replace("◎导　　演",'').strip()
            movie['director'] = info

    sql = "insert into movie(id,title,cover,screenshoot,year,country,category,duration,director) values(null,'{title}','{cover}','{screenshoot}','{year}','{country}','{category}','{duration}','{director}')".format(
        title=movie['title'],
        cover = movie['cover'],
        screenshoot = movie['screenshoot'],
        year = movie['year'],
        country = movie['country'],
        category = movie['category'],
        duration = movie.get('duration') or '',
        director = movie['director']
    )
    cursor.execute(sql)
    conn.commit()




def parse_list():
    # 1. 请求数据
    url = 'http://www.dytt8.net/html/gndy/dyzz/index.html'
    response = requests.get(url,headers=headers,proxies=proxies)
    html = response.content.decode("gbk")

    # 2. 解析数据
    DOMAIN = 'http://www.dytt8.net'
    parser = etree.HTML(html)
    hrefs = parser.xpath("//a[@class='ulink']/@href")
    for href in hrefs:
        detail_url = DOMAIN+href
        parse_detail(detail_url)
        # break


if __name__ == '__main__':
    parse_list()

