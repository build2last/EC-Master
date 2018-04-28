EC-Master 电商爬虫与观点挖掘
====

**`Windows 10`**

[![](https://img.shields.io/badge/python-3.4-green.svg)](https://www.python.org/download/releases/3.4.0/) [![](https://img.shields.io/badge/python-3.5-green.svg)](https://www.python.org/downloads/release/python-352/)
[![](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/) 
[![](http://www.gnu.org/graphics/gplv3-88x31.png)](https://github.com/build2last/EC-Master/blob/master/Licence)

Copyright 2017 Liu Kun, NUST-CS2013

a Python3 project

通过对电商数据的抓取，了解和掌握相关的网络爬虫技术及反爬虫技术，通过对爬取到数据的分析，了解和掌握细粒度情感分析、观点挖掘等相关机器学习算法，通过对所有资源的整合形成一个较为完整的基于电商评论抓取的观点挖掘展示系统。

## 环境依赖
1. Python 3
2. MySql
3. phantomJS

## 部署步骤
1. 建立 MySql 数据库
> CREATE DATABASE ec DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

2. 修改 settings.py 中参数

3. 用某种手段将电商网站首页 HTML 内容放到 Category/HomePageParser 目录下并重命名
> 比如在浏览器查看网页源代码

4. 凭借 django 的ORM在数据库中建立表格: 执行命令
> python manage.py makemigrations
python manage.py migrate

5. 运行爬虫程序:  StartCrawler.py

6. 解析页面数据并将结构化数据导入数据库：DataParser/jsonToDataBase.py

## 模块说明
* Category：对网站首页进行解析，提供接口供其他模块按条件获取商品目录；
* DataParser：将原始页面解析，对数据进行清洗和结构化并导入数据库；
* WebCrawler：电商爬虫程序，获取原始页面和商品信息；
* djangoApp：网站App，数据库ORM；
* NLP： 一些对评论进行处理和分析的脚本程序；
* test_extract_html：用于对页面解析进行初期调试；
* review_backup：存储原始页面内容文件，可能会在后面的版本中删除。

## 测试
* test.py 对一些模块的接口进行测试
* djangoApp + ReviewMining 结合 d3.js 前端框架，提供一些对于评论中观点的可视化分析

## 版本摘要
* 2017-05-24 [init] 建立v1.0 并开源在 Github 
