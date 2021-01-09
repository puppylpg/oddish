
[![oddish](https://img.shields.io/badge/pokemon-oddish-green)](https://www.pokemon.com/us/pokedex/oddish)
[![junior](https://img.shields.io/badge/wiki-junior-green)](https://puppylpg.github.io/2019/12/02/python-crawler-buff/)
[![optimized](https://img.shields.io/badge/wiki-optimized-green)](https://puppylpg.github.io/2019/12/07/python-crawler-buff-optimaze/)
[![puppylpg](https://img.shields.io/badge/author-puppylpg-green)](https://puppylpg.github.io/)

# oddish
![oddish](static/oddish.png)
> [During the daytime, Oddish buries itself in soil to absorb nutrients from the ground using its entire body.](https://www.pokemon.com/us/pokedex/oddish)

走路草，白天沉睡，夜晚潜行，我来过，并将信息镌刻在深深的记忆里。

# Aim
To crawl csgo skin from `buff.163.com`. 
If there is no data available, crawl from the website, then analyse data from local pandas DataFrame to avoid more crawling behavior.

> **First Rule: BE GOOD AND TRY TO FOLLOW A WEBSITE’S CRAWLING POLICIES. Don't crawl the website with a high frequency!**

# 免责声明
1. 滥用爬虫有被封号的风险；
1. 禁止恶意大量爬取buff数据，否则由此造成的责任自负；
1. 禁止将该爬虫或爬虫获取到的数据用作商业用途，否则由此造成的责任自负；
1. 该爬虫为兴趣使然，不收取任何费用，也没有任何恶意代码。如果还是出了问题，我们可以协商改进代码，但由此造成的后果（比如账号被封），我们也无能为力；

# 如何防止账号被封禁
该爬虫只是为了买个性价比最高的饰品卖到steam里换个买游戏钱，所以本质上不会被经常使用，也不需要爬取太多数据。

总体原则是“缓慢”地获取“少量”数据。这里有一些建议，通过修改配置`config.ini`，能帮助你更合理地使用oddish：

1. 缓慢：尽量调大配置里的`frequency_interval_low`和`frequency_interval_high`，爬取时间间隔越长，爬得越慢，越安全；
1. 少量：
    1. 尽量使用配置里的`category_white_list`限定爬取饰品的类别，类别越少，要爬的数据量越小；
    1. 尽量使用配置里的`category_black_list`限定爬取饰品的类别，类别越多，要爬的数据量越小；
    1. 尽量使用配置里的`crawl_min_price_item`和`crawl_max_price_item`缩小要爬去饰品的价格区间，区间越小，要爬的数据量越小；
    1. 不要经常使用。就我本人来讲，一月能用一次就不错了……csgo出个大行动，或者有新游戏发行，才有使用oddish的场景。天天爬，一天爬很多次的同学，有那么多游戏要买吗……

- 如果你对该爬虫的代码实现感兴趣，欢迎学习交流；
- 如果你想买个饰品卖到steam换个游戏钱，欢迎使用；
- 如果你想倒（往steam里有毛好倒的？倒完卖余额吗？？？），gun (ノ｀Д)ノ

# 我要如何使用
## 视频教程
最直白的方式，就是再跟着视频一步步来：[oddish纯小白使用教程](https://www.bilibili.com/video/BV1ET4y1w7e1/)

## v4.0.0异步爬取
从v4.0.0版本开始，从steam获取数据时，换成了python aio（async io），速度极大提升，基本上一分钟以内就能搞定了。
相应的，要装的aio相关依赖也多了一些。

**如果实在搞不定，建议下载v4.0.0之前的版本。用起来稍微简单点儿，缺点就是非常慢。和v4.0.0相比，二者大概就是一分钟和一小时的差距吧。**

但个人还是建议先尝试一下v4.0.0+版本，毕竟速度快了不是一星半点儿。

## wiki
这里还有两篇文章介绍了oddish初期构建和优化思路，如果你想看的话：
- https://puppylpg.github.io/2019/12/02/python-crawler-buff/
- https://puppylpg.github.io/2019/12/07/python-crawler-buff-optimaze/

## 启动前必看
### 警告
**警告：由于现在buff有反爬机制，爬的过频繁会账号冷却。目前程序配置的是4-8s爬取一次。可自行在配置文件`config.ini`里配置间隔时间，但为了您的账号安全，程序无论如何都不会以小于4s的间隔爬数据。**

如果还不放心，建议时间间隔再调大一些。当然，调的越大，爬得越慢。所以建议同时使用配置里的黑白名单缩小饰品爬取范围，
减少没必要的爬取。

### 数据源
当首次爬取某url时，会从网站爬取数据，保存到本地。之后再次爬取时，默认先检测本地文件，如果有，直接从本地加载。

url对应内容的缓存时间可在配置里自行设置，可配置是否强制从网站上爬取。

总体来讲，缓存时间设置的越长，信息越不是最新的，失效可能性越大。反之，越能获取最新信息，但爬取的工作量越大，需要时间更久。

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

### 爬取steam商店所需的代理
并不能找到国内的质量比较高的合（免）适（费）的代理服务器。如果不能裸访问steam商店，需要本地开启代理（或者vpn），
同时需要在`config/config.ini`中提供一个`socks`代理配置（即ss或v2ray的本地端口），以科学爬取社区市场数据。

如果不需要代理即可直连steam商店，将配置文件中的 `proxy` 留空即可。

你也可以使用网易UU加速器，只需使用模式一、二或三加速Steam社区/商店，并将配置文件中的`proxy`留空。

# 启动命令
1. （可选）自定义配置，cookie一定要配置，方法见上述“认证”部分；
1. 工程根目录下运行：`python -m src`

## 输出结果
~~- database：爬的数据；~~
- log: 日志；
- suggestion：分析结果；

如果不关心过程，只查看分析结果即可。

## 依赖
如果只会使用Anaconda人肉安装，就安装以下依赖：
- python: 3.8.5
- pandas: 1.1.0
- numpy: 1.19.1
- requests: 2.24.0
- aiohttp: 3.7.3
- aiofiles: 0.6.0
- aiohttp-socks: 0.5.5（使用pip）

由于aiohttp-socks没有移植到Anaconda，所以只能使用pip安装。点击Anaconda界面首页的'CMD.exe Promt'下面的Launch按钮，
会打开一个命令行，输入`pip install aiosocks`即可安装。

如果懂pip，直接用以下命令安装：
> pip install -r requirements.txt

# 按照需求自定义配置
修改`config/config.ini`中的一些参数，进行自己希望的自定义配置。所有配置的含义见文件中的注释，或者wiki介绍。

## 价格区间设定
价格区间设定在2.0.0版本中是一个非常重要的优化。

之前的价格筛选方式为：爬取所有饰品，按照价格区间进行筛选。优化之后，先使用buff对价格进行筛选，然后爬去筛选后的物品。
这样做之后爬取数据量骤减，效率极大提升。

价格区间配置为`config/config.ini`的`crawl_min_price_item`和`crawl_max_price_item`，有以下限定：
- 最低价不小于0；
- 最高价不低于最低价，且不超过buff限定的最高价，目前为15w；
- 如果所填写条件不满足上述条件，将按上述条件进行处理。

比如区间设定为`5~1`元，则会被系统调整为`5~5`元，即只爬取5元饰品。

> 但是不得不说buff的区间筛选API很是清奇，限定价格之后，返回的`page_num`和`page_size`竟然都是错的。也就是说返回的数据并不能告诉我们在这个价格区间内
一共有多少页共计多少饰品。然鹅机智的我发现，如果将page number设定为超出实际页数的值，这两个数据就会变成正确值。比如，价格在98~99.9的饰品共计3页42件，但是返回值告诉我们一共有720页14388件，而这实际是buff现售物品总数，并不是价格筛选后的件数。
想获取准确值3页42件，只需给page number设定为超出3的值即可，所以我用了`sys.maxsize`，一个巨大无比的值。

> 只有trick能击败trick，然后让代码变得更加tricky :D

## 类别设定
增设类别限定，可以配置自己**只想**爬取的类别（白名单）或者**不想**爬取（黑名单）的类别。

**白名单优先级高于黑名单优先级。**

高级技巧（小白慎入）：**黑白名单均支持通配符匹配，如 weapon_knife\* 等，更多用法请搜索 "Shell 通配符"**。

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

# 结论
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

想要对oddish做出力所能及的贡献？请参考[CONTRIBUTING.md](.github/CONTRIBUTING.md)。
