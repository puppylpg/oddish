#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import requests
from bs4 import BeautifulSoup


class KuaiDaiLiHidden(object):
    def __init__(self):
        self.session = requests.session()
        self.proxies = None
        self.timeout = 10
        self.time_interval = 2
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36",
        }

    def get_status(self, url):
        """
        获取状态
        :param url: 访问地址
        :return: 返回response或False
        """
        response = self.session.get(
            url=url,
            headers=self.headers,
            proxies=self.proxies,
            timeout=self.timeout,
            # verify=False,
            # allow_redirects=False
        )
        if response.status_code == 200:
            return response
        else:
            print("ERROR: 网络连接失败！ status: %s url: %s" % (response.status_code, url))
            return False

    def get_last_page(self, url):
        """
        获取最后一页page
        :param url: 第一页的url
        :return: 返回int(last_page)或None
        """
        response = self.get_status(url)
        if not response:
            return None
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        lis = soup.select("#listnav > ul > li")

        if lis[-1].text == "页":
            last_page = lis[-2].find("a").text

            return int(last_page)
        return None

    def get_index(self, url):
        """
        访问首页，建立连接
        :param url:
        :return:
        """
        response = self.get_status(url)
        if response:
            # response.encoding = "utf-8"
            # html = response.text
            # print(html)
            print("首页,建立连接...")
            return True
        else:
            print("ERROR: 首页访问失败！")
            return False

    def parse_html(self, url):
        response = self.get_status(url)
        if not response:
            return None
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find(id="list").find("tbody").find_all("tr")
        ip_port_list = []
        for item in items:
            ip = item.find(attrs={"data-title": "IP"}).text
            port = item.find(attrs={"data-title": "PORT"}).text
            ip_port = ip + ":" + port + "\n"
            ip_port_list.append(ip_port)

        return ip_port_list

    @staticmethod
    def write_to_text(path, content):
        path = os.path.abspath(path)
        with open(path, 'a+', encoding='utf-8') as f:
            f.writelines(content)

    def next_page(self, last_page):
        for i in range(1, last_page + 1):
            time.sleep(self.time_interval)
            url = "https://www.kuaidaili.com/free/inha/{i}".format(i=i)
            print(url)
            ip_port_list = self.parse_html(url)
            path = os.path.join(os.getcwd(), "IP.txt")
            self.write_to_text(path, ip_port_list)

    def main(self):
        url = "https://www.kuaidaili.com"
        if not self.get_index(url):
            return None

        time.sleep(self.time_interval)

        url = "https://www.kuaidaili.com/free/inha/1"
        # last_page = self.get_last_page(url)
        last_page = 3
        if not last_page:
            return None

        self.next_page(last_page)


if __name__ == '__main__':
    kuai_dai_li = KuaiDaiLiHidden()
    kuai_dai_li.main()
