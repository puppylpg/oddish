import urllib.request
import re

if __name__ == '__main__':
    item_regex = re.compile(
        r'''<li>\s+<a href="(.+?)"\s+title="(.+?)">(.*?)￥(.+?)"(.*?)</li>''', re.DOTALL
    )

    steam_link_regex = re.compile(
        r'''参考价格(.*?)href="(.+?)"'''
    )

    q = re.compile(r'''<div class="hero">\s+<span>Reference: .+\( about ￥ (.+?) \)</span>''')

    for i in range(10):
        target = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num=%d' % i
        main_page = urllib.request.urlopen(target)
        main_page_html = main_page.read().decode('utf-8')
        items = item_regex.findall(main_page_html)

        for item_info in items:
            item_relative_addr = item_info[0]
            item_name = item_info[1]
            item_buff_price = float(item_info[3])

            item_full_addr = 'https://buff.163.com/' + item_relative_addr
            item_page = urllib.request.urlopen(item_full_addr)
            item_page_html = item_page.read().decode('utf-8')
            steam_link = steam_link_regex.findall(item_page_html)[0]

            print('%s\t buff最低价：%f steam link: %s' % (item_name, item_buff_price, steam_link))
