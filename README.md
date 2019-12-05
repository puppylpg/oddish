[toc]

# oddish
![oddish](static/oddish.png)
> [During the daytime, Oddish buries itself in soil to absorb nutrients from the ground using its entire body.](https://www.pokemon.com/us/pokedex/oddish)

走路草，白天沉睡，夜晚潜行，我来过，并将信息镌刻在深深的记忆里。

## Aim
To crawl csgo skin from `buff.163.com`. 
If there is no data available, crawl from the website, then analyse data from local pandas DataFrame to avoid more crawling behavior.

> **First Rule: BE GOOD AND TRY TO FOLLOW A WEBSITE’S CRAWLING POLICIES. Don't crawl the website to often!**

## wiki
https://puppylpg.github.io/python/csgo/2019/12/01/python-crawler-buff.html

## 爬取
### 数据源
当首次爬取时，会从网站爬取数据，保存到本地。之后再次爬取时，默认先检测本地文件，如果有，直接从本地加载。

文件目前以小时为单位保存，同一小时区间内使用同一个文件。所以当在不同小时首次运行时，会再次从网站爬取数据。

可配置是否强制从网站上爬取。

### 认证
buff提供完用户名密码之后还要使用网易易盾验证登录，挺烦的。所以目前简单起见，
每次先使用用户名和密码网页登录buff，然后手工把cookie贴到`config/config.ini`里，使用该cookie运行。

建议使用Chrome登录buff，查看cookie（可自行百度方法），贴到配置里，粘贴后配置示例如下：
```
[BASIC]
cookie = _ga=GA1.2.162602080.1551374933; _ntes_nnid=8ce0cf6bdce55512e73f49cb8a49960e,1552104955025; _ntes_nuid=8ce0cf6bdce55512e73f49cb8a49960e; ...; _gat_gtag_UA_109989484_1=1
```

### 代理
并不能找到国内的质量比较高的合（免）适（费）的代理服务器。所以还是用自己的ip慢慢爬着吧。爬慢点儿，看起来buff也不会下杀手。

csgo总共10000多饰品，每爬一次大概20个，总共下来500多次请求应该就可以了。但是每个饰品都要单独爬一次历史交易价格记录，
所以请求量倍增，建议使用价格过滤排除某价格区间的物品。详见wiki。

## 配置
修改`config/config.ini`中的一些参数，进行自己希望的自定义配置。所有配置的含义见文件中的注释，或者wiki介绍。

### 价格区间设定
价格区间设定在2.0.0版本中是一个非常重要的优化。

之前的价格筛选方式为：爬取所有饰品，按照价格区间进行筛选。优化之后，先使用buff对价格进行筛选，然后爬去筛选后的物品。
这样做之后爬取数据量骤减，效率极大提升。

价格区间配置为`config/config.ini`的`crawl_min_price_item`和`crawl_max_price_item`，有以下限定：
- 最低价不小于0；
- 最高价不低于最低价，且不超过buff限定的最高价，目前为15w；
- 如果所填写条件不满足上述条件，将按上述条件进行处理。

比如区间设定为`5~1`元，则会被系统调整为`5~5`元，即只爬取5元饰品。

#### buff的区间筛选API
不得不说buff的区间筛选API很是清奇，限定价格之后，返回的`page_num`和`page_size`竟然都是错的。也就是说返回的数据并不能告诉我们在这个价格区间内
一共有多少页共计多少饰品。然鹅机智的我发现，如果将page number设定为超出实际页数的值，这两个数据就会变成正确值。

比如，98~99.9的饰品共计3页42件，但是返回值告诉我们一共有720页14388件，而这实际是buff现售物品总数，并不是价格筛选后的件数。
想获取准确值3页42件，只需给page number设定为超出3的值即可，所以我用了`sys.maxsize`，一个巨大无比的值。

> 我是不是应该给buff报个bug：
> - hi, buff，我爬你的网站发现你有bug。
> - buff: 好的，bug奖励两毛，爬虫封ip处理。
> :D

### 类别设定
增设类别限定，可以配置自己**只想**爬取的类别（白名单）或者**不想**爬取（黑名单）的类别。

**白名单优先级高于黑名单优先级。**

所以规则如下：
- 如果黑白名单均未设置，默认爬取所有类别，所有类别参考`config/reference/category.md`；
- 如果设置了白名单，仅爬取白名单类型饰品；
- 如果只设置了黑名单，则爬取除了黑名单之外的所有物品；

比如：
```
category_white_list = ["weapon_ak47", "weapon_m4a1", "weapon_m4a1_silencer"]
category_black_list = ["weapon_m4a1"]
```
则最终会爬取AK、M4A1、M4A4三种物品。

> NOTE: M4A1游戏代号为"weapon_m4a1_silencer"、M4A4游戏代号为"weapon_m4a1"。
> 不要问为什么，我猜是V社员工一开始起名的时候没想好，后来由于兼容性等原因不好改了。那咋办嘛，就这么用着呗。

**类别名称一定不能写错了（建议复制粘贴），否则buff直接返回所有类别的物品……什么鬼设定……**

内部实现上：
- 如果未设定爬取类别，则不分类别直接爬取价格区间内的所有物品；
- 如果设定了爬取类别，依次爬取有效类别内所有符合价格区间的物品；

## 运行方法
1. （可选）自定义配置，cookie一定要配置，方法见上述“认证”部分；
1. 工程根目录下运行：`python -m src`

## 输出结果
- database：爬的数据；
- log: 日志；
- suggestion：分析结果；

如果不关心过程，只查看分析结果即可。

## 依赖
- python: 3.7.3
- pandas: 0.25.3
- numpy: 1.17.4

没使用依赖的特别特殊的功能，所以除了python必须python3，其他依赖不是这个版本应该也没啥问题。

## 数据结构
- `name`：饰品中文名；
- `price`：buff最低价；
- `steam_predict_price`：预估的steam最低售价；
- `buy_max_price`：buff最高求购价格；
- `average_sold_price_after_tax`：steam该饰品过去一段时间所有成交价格的.25分位点价格；
- `gap`：`average_sold_price_after_tax - price`，`average_sold_price_after_tax`扣税后和buff最低售价的差值；
- `gap_percent`：`gpa`值占`price`的比例，大概可理解为单位资金效率吧；

## example
一些buff返回的json样例：
- `goods.json`: 某category中的一些（一般是20个）item信息；
- `price_history`: steam交易记录（`$`）；
- `steam_inventory`: 库存；

## 结论
最终我发现，还是买steam充值卡更实惠 :D 

但是说实话黑产这种东西，还是不碰为好，买完充值卡遭遇steam红信的也不少，所以还是这种方式更安全。
