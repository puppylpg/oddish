[toc]

[![oddish](https://img.shields.io/badge/pokemon-oddish-green)](https://www.pokemon.com/us/pokedex/oddish)
[![junior](https://img.shields.io/badge/wiki-junior-green)](https://puppylpg.github.io/python/csgo/2019/12/02/python-crawler-buff.html)
[![optimized](https://img.shields.io/badge/wiki-optimized-green)](https://puppylpg.github.io/python/csgo/2019/12/07/python-crawler-buff-optimaze.html)
[![puppylpg](https://img.shields.io/badge/author-puppylpg-green)](https://puppylpg.github.io/)

# oddish
![oddish](static/oddish.png)
> [During the daytime, Oddish buries itself in soil to absorb nutrients from the ground using its entire body.](https://www.pokemon.com/us/pokedex/oddish)

走路草，白天沉睡，夜晚潜行，我来过，并将信息镌刻在深深的记忆里。

## Aim
To crawl csgo skin from `buff.163.com`. 
If there is no data available, crawl from the website, then analyse data from local pandas DataFrame to avoid more crawling behavior.

> **First Rule: BE GOOD AND TRY TO FOLLOW A WEBSITE’S CRAWLING POLICIES. Don't crawl the website to often!**

## wiki
- https://puppylpg.github.io/python/csgo/2019/12/01/python-crawler-buff.html;
- https://puppylpg.github.io/python/csgo/2019/12/07/python-crawler-buff-optimaze.html;

## 爬取

### ALERT
**警告：由于现在buff有反爬机制，爬的过频繁会账号冷却。目前程序配置的是2-4s爬取一次。可自行在配置文件`config.ini`里配置间隔时间，但为了您的账号安全，程序无论如何都不会以小于2s的间隔爬数据。**

如果还不放心，建议时间间隔再调大一些。当然，调的越大，爬得越慢。所以建议同时使用配置里的黑白名单缩小饰品爬取范围，
减少没必要的爬取。

### 数据源
当首次爬取时，会从网站爬取数据，保存到本地。之后再次爬取时，默认先检测本地文件，如果有，直接从本地加载。

文件目前以小时为单位保存，同一小时区间内使用同一个文件。所以当在不同小时首次运行时，会再次从网站爬取数据。

可配置是否强制从网站上爬取。

### 认证
buff提供完用户名密码之后还要使用网易易盾验证登录，挺烦的。所以目前简单起见，
每次先使用用户名和密码网页登录buff，然后手工把cookie贴到`config/config.ini`里，使用该cookie运行。

同时也需通过这个方法提供steam的cookie以爬取steam历史价格。

建议使用Chrome登录buff，查看cookie（可自行百度方法），贴到配置里，粘贴后配置示例如下：
```
[BASIC]
buff_cookie =  _ntes_nnid=b14d347a6d72cfffffffffa5cdbb99a7,1571493626117; _ntes_nuid=b14d347a6d72c258095b57a5cdbb99a7; ...
steam_cookie = timezoneOffset=28800,0; steamMachineAuth76561198093333055=649A9B56941EC90A07EEEEEE0A907688C5D6042; ...
```

### 代理
并不能找到国内的质量比较高的合（免）适（费）的代理服务器。所以还是用自己的ip慢慢爬着吧。csgo总共10000多饰品，每爬一次大概20个，总共下来500多次请求应该就可以了。但是每个饰品都要单独爬一次历史交易价格记录，
所以请求量倍增，建议使用价格过滤排除某价格区间的物品。~~爬慢点儿，看起来buff也不会下杀手。~~

同时需要在`config/config.ini`中提供一个`socks`代理（即ss或v2ray的本地端口），以科学爬取社区市场数据。

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

**黑白名单均支持通配符匹配，如 weapon_knife\* 等，更多用法请搜索 "Shell 通配符"**

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

### 汇率设定
当steam账户所在区非国区时爬取到的steam市场价格单位非人民币，此时可以修改`config/config.ini`中的`exchange_rate`以解决汇率换算问题

比如：steam账户为俄区，当前1俄罗斯卢布=0.08732人民币
```
exchange_rate = 0.08732
```

## 运行方法
1. （可选）自定义配置，cookie一定要配置，方法见上述“认证”部分；
1. 工程根目录下运行：`python -m src`

## 输出结果
- database：爬的数据；
- log: 日志；
- suggestion：分析结果；

如果不关心过程，只查看分析结果即可。

## 依赖
- python: 3.8.5
- pandas: 1.1.0
- numpy: 1.19.1
- requests: 2.24.0

注意python为python3，requests为socks版本，其他依赖无特殊要求。

### socks版本requests的安装方法
```
pip install requests[socks]
pip install requests[security]
```

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
最终我发现，这种方法未必比充值卡更优惠，但绝对更安全、快速。再也不用：
- 苦等卖家发货；
- 大半夜和客服聊天；
- 忍受充值卡随意涨价的无奈；
- 担心账户被红信；

额外好处是，充值卡只能买固定面值的，这种却可以根据需要的余额数，买任意价位的饰品转余额。

而且程序给出的收益是使用steam售价的.25分位点的价格计算的，偏保守，所以实际收益一般会更多。

一个示例：
- 想趁打折买只狼&黑魂III；
- 跑了一下100-200的饰品，程序给出的最高建议是：AK-47 | 皇后 (破损不堪): 213.81325(steam .25 percentile sold price after tax) - 159.0(buff) = 54.81325000000001(beyond 34.47%). Sold 159 items in 7 days.
- 所以buff收了最便宜的皇后AK破损不堪，花了159。steam挂270，很快就卖掉了，到手余额：AK-47 | The Empress  234.80 CNY；
- 比例：159/234.79=0.677（想了想，充值卡也不过如此）；
- 加上原来就有的40+余额，买了DARK SOULS III Deluxe Edition和Sekiro: Shadows Die Twice；
- 玩了一下，卒，卒，卒……卒无限循环，退款……

# Last but not least
- 喜欢：欢迎star；
- 有问题：欢迎提出[issue](https://github.com/puppylpg/oddish/issues)；
- 程序爱好者：欢迎fork，或者提出merge request；
- 土豪：欢迎点一下工程上的sponsor，赞助一波；
