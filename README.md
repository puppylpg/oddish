[toc]

# buff csgo skin crawler
To crawl csgo skin from `buff.163.com`. 
If there is no data available, crawl from the website, then analyse data from local pandas DataFrame to avoid more crawling behavior.

> **First Rule: BE GOOD AND TRY TO FOLLOW A WEBSITE’S CRAWLING POLICIES. Don't crawl the website to often!**

## 爬取
### 数据源
当首次爬取时，会从网站爬取数据，保存到本地。之后再次爬取时，默认先检测本地文件，如果有，直接从本地加载。

文件目前以小时为单位保存，同一小时区间内使用同一个文件。所以当在不同小时首次运行时，会再次从网站爬取数据。

可配置是否强制从网站上爬取。

### 认证
buff提供完用户名密码之后还要使用网易易盾验证登录，挺烦的。所以目前简单起见，
每次先网页登录，然后手工把cookie贴到程序里，使用该cookie运行。

### 代理
并不能找到国内的质量比较高的合（免）适（费）的代理服务器。所以还是用自己的ip慢慢爬着吧。爬慢点儿，看起来buff也不会下杀手。

csgo总共10000多饰品，每爬一次大概20个，总共下来500多次请求应该就可以了。平均每次请求延迟1-2s，算下来总时间应该在20min以内。

> TIME USED: 0:18:40.363070.

## 数据结构
- `name`：饰品中文名；
- `price`：buff最低价；
- `steam_predict_price`：预估的steam最低售价；
- `buy_max_price`：buff最高求购价格；
- `gap`：当前是`steam_predict_price - price`，需要替换为steam求购价格；

## 使用方法
工程根目录下：`python -m src`

## 依赖
- python: 3.7.3
- pandas: 0.25.3

## 结论
最终我发现，还是买steam充值卡更实惠 :D
