# 刻意单词听写

这是一款协助你进行单词听写的软件，它将你要练习的单词列表读出来，然后比对你默写的结果和正确答案。
你写错的单词，会以更强的概率再次出现，直到你掌握了他。反之，你反复写对的单词，会出现得越来越少，让你更能专注练习那些你不太熟悉的。


## 初心
起初这个软件是写给我老婆协助他学英语用的，觉得挺好玩的把他分享出来。

## 特性&使用方法

**v0.1**
* 支持按照时间和单词数设置练习强度
* 在线获取单词发音（需联网）
* 单词发音依赖一个外部包: pip install playsound

目前这版只是在command line帮助你背单词。

第一次启动：

`python learner.py your_db.json your_list.json`

其中your_db.json 是你本地存储单词记录的数据库文件名，内容由软件自动生成，你只需只定一个不存在的文件即可。
your_list.json 是你想听写的单词列表，一个单词一行。

之后启动：

`python learner.py your_db.json`

程序会加载之前存储在your_db.json的背诵记录。


## TODO
后边如果有时间，一些想搞的东西：
* 每次练习强度可以设置，这样可以在强度和范围上取得一个
* 字母粒度识别错的强度，给出针对性提示
* web 化方便对命令行不熟悉的用户使用
* 在线获取示意，有助于背单词
* 基于云的单词表分享功能


