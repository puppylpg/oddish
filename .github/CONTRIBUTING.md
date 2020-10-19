首先，感谢您对本项目做出贡献，您的热忱将会使oddish变得越来越好，让更多的csgo小伙伴受益。

# 我可以做什么
贡献不仅仅代表代码。一切能让oddish变得更好的举措，我们都非常欢迎。

## 提出问题
无论是使用中碰到的问题，还是有一些新奇的想法或建议，欢迎[发起issue](https://github.com/puppylpg/oddish/issues/new)，描述您的观点。
我们将尽快予以答复。

## 贡献代码
无论您是自己有需求，还是在[issue](https://github.com/puppylpg/oddish/issues/)里看到别人的想法建议，如果能将这些直接用鲜活的代码实现出来，
将会是对oddish最直接的增强。不用对自己的代码水平过于担心，大家一起努力，相信一定能将代码写得漂亮整洁，共同提高进步。

可以在[Pull Request](https://github.com/puppylpg/oddish/pulls)里提交贡献。

## 其他
也许你还能想到其他传播、推广、丰富oddish的小点子，欢迎提出。

# 如何贡献代码
## 了解oddish架构
oddish是一个小程序，架构相对简单。这里还有一个额外的参考资料，帮助你更快了解代码里的一些内容：
### wiki
这里有两篇wiki，描述了oddish初期的构建和优化历程：
- https://puppylpg.github.io/2019/12/02/python-crawler-buff/
- https://puppylpg.github.io/2019/12/07/python-crawler-buff-optimaze/

### 数据结构
`Item`类是对csgo饰品的数据结构描述，一些属性解释如下：
- `name`：饰品中文名；
- `price`：buff最低价；
- `steam_predict_price`：预估的steam最低售价；
- `buy_max_price`：buff最高求购价格；
- `average_sold_price_after_tax`：steam该饰品过去一段时间所有成交价格的.25分位点价格；
- `gap`：`average_sold_price_after_tax - price`，`average_sold_price_after_tax`扣税后和buff最低售价的差值；
- `gap_percent`：`gpa`值占`price`的比例，大概可理解为单位资金效率吧；

其他数据结构如有必要会继续补充。

### example
`example`文件夹里有一些buff返回的json样例，不完全整理如下：
- `goods.json`: 某category中的一些（一般是20个）item信息；
- `price_history`: steam交易记录（`$`）；
- `steam_inventory`: 库存；

欢迎补充更多。

## 代码规约
当前代码量并不大，代码也比较简单整洁，维持现有代码的格式就行了。

比如：
- 命名多为下划线分割的单词，不要用驼峰命名法；
- 符号前后都有一个空格，比如等号；
- 一些新加流程或者比较复杂的地方记得打log；

等等。

## 代码合并
合并前请先解决所有code review中提出的问题，并标记每一处review意见为resolved状态。

合并时记得压缩本次代码提交的所有commit，避免一次合并往master里添加多次commit。


再次感谢您的积极参与，我们一起让oddish变得更好。
