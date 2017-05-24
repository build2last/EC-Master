# coding:utf-8
import re
import datetime
import dataItem
from lxml import etree

# HTML expected to be UTF-8 file
def get_tree_node(HTML):
    import pprint

# Macbook air
# https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.58.zk2EnQ&id=530683052432&skuId=3191942273827&areaId=320100&standard=1&user_id=1669409267&cat_id=50024399&is_b=1&rn=c79258b5818e50ee33cbc36e24b15d83
# https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.zk2EnQ&id=530945296812&skuId=3163301283248&areaId=320100&standard=1&user_id=2616970884&cat_id=50024399&is_b=1&rn=c79258b5818e50ee33cbc36e24b15d83


def extract_goods_from_tmall_page(HTML):
    """ return: (商品名称，价格，商品id-店铺id元组)"""
    HTML = HTML.decode("utf-8","ignore")
    tree = etree.HTML(HTML)
    goods_warp = tree.xpath('//div[@class="product-iWrap"]')
    goods_list = []
    for g in goods_warp:
        goods_name = g.xpath('./div[@class="productTitle productTitle-spu"]/a[1]/text()')
        price = g.xpath('./p[@class="productPrice"]/em/text()')
        url = g.xpath('.//a[1]/@href')[0]
        pattern = re.compile('id=(?P<id>.*?)&.*?user_id=(?P<user_id>.*?)&', re.S) #r'<a href="//detail.tmall.com/item.htm?id=(?P<id>.*?)&.*?user_id=(?P<user_id>.*?)&
        goods_seller_tuple = re.findall(pattern, url)
        if goods_name:
            goods_list.append((goods_name[0], price[0], goods_seller_tuple[0]))
    return goods_list


def extract_goods_from_jd_page(HTML):
    """ return: (商品名称，价格，商品id-店铺id元组)"""
    HTML = HTML.decode("utf-8","ignore")
    tree = etree.HTML(HTML)
    goods_warp = tree.xpath('//div[@class="gl-i-wrap j-sku-item"]')
    goods_list = []
    for g in goods_warp:
        goods_name = g.xpath('./div[@class="p-name"]/a[1]/em/text()')
        price = g.xpath('.//*[@class="J_price"]/i/text()')
        url = g.xpath('./div[@class="p-name"]/a[1]/@href')
        if goods_name:
            goods_list.append((goods_name[0], price[0], goods_seller_tuple[0]))
    return goods_list


def get_nodes(HTML_path):
    HTML = open(HTML_path, "rb").read()
    for item in extract_goods_from_tmall_page(HTML):
        item_id = "TMALL_" + "-".join((item[2][1],item[2][0]))
        title = item[0]
        platform = "TMALL"
        category = "TMALL~手机,数码,电脑办公~电脑整机~笔记本"
        detail = "{update: %s, price: %s}"%(str(datetime.datetime.today()), item[1]) 
        dataItem.Good(item_id=item_id, title=title, platform=platform, category=category, detail=detail).save_to_db()


def test():
    import pprint
    path = "html.txt"
    get_nodes(path)
    # HTML = open(path, "rb").read()
    # extract_goods_from_tmall_page(HTML)
    # for node in get_nodes(path):
    #     pprint.pprint(node)


def main():
    import os
    print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "review_backup"))


if __name__ == '__main__':
    test()