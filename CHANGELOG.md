# buff csgo skin crawler
## v1.0.0(2019-11-30)
* 功能
    - 完成爬取、简单分析功能；

## v1.1.0(2019-11-30)
* 功能
    - 默认优先使用本地文件加载数据，没数据时再从网站获取；

## v1.2.0(2019-11-30)
* 功能
    - 使用pandas DataFrame的筛选排序功能替换原来使用list的做法；

## v1.3.0(2019-11-30)
* 功能
    - 爬取所有item的steam历史（默认7天）售出价格；
    - 使用steam历史售出价格平均值替代steam最低售价，售价可能虚高，售出价格才是实在的；

## v1.4.0(2019-11-31)
* 功能
    - cookie放入文件；
    - 价格低于`CRAWL_MIN_PRICE_ITEM`或高于`CRAWL_MAX_PRICE_ITEM`就不爬取了，每个item的历史售出价格都要单独爬一次，太耗时了；

* TODO
    - 增加爬取缓存，如果爬取过程太长中断，可以使用   
    ```
    catch exception 生成table持久化文件.unfished和访问过的url持久化文件
    在每次网络访问后，记录访问过的url，访问前，判断url是否访问过
    下次启动时，先检查是否有未完成，有的话恢复，并删除unfished和url used
    
    测试的时候，可以先使用一个category去试试，中间断网
  
    或者专门搞fail item url，fail category url， fail price url，一个个单独分类恢复
    ```
    - 计算steam卖到buff的收益率时，使用buff实际售价取代buff最低售价，要不然也没啥意义；
    - 显示进度，记录每一次价格爬取是总第多少次，好预估结束时间；

## v1.5.0(2019-12-02)
* 功能
    - 爬取的数据、log、建议分别放到database、log、suggestion文件夹中，同时console也会输出所有内容；
    - 实际计算`average_sold_price`价格的时候，用的是该饰品steam历史平均售价的.25分位点，更科学一些。防止一些“好货”带高预期收入；
    - 调整扣税总比例为15%，steam 5%，csgo 10%；
    - 爬取价格的时候增加进度显示，好对总时间有预期；
    - 爬取的时候设置timeout=5s，超时报错返回；
