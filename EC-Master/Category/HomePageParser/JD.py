# coding:utf-8
# from __future__ import unicode_literals
from __future__ import division
import pprint
from lxml import etree


# HTML expected to be UTF-8 file
def get_tree_node(HTML, basic_url):
    nodes_tree = []
    tree = etree.HTML(HTML)
    cate_nodes = tree.xpath('//*[@class="a-row a-spacing-small a-spacing-top-medium"]')
    level1_items = []
    level1_nodes = tree.xpath('//*[@class="cate_menu_item"]')
    for node in level1_nodes:
        level1_items.append(",".join(node.xpath('.//a[@class="cate_menu_lk"]/text()')))
    level2_roots = tree.xpath('//*[@class="cate_part_col1"]')
    reserve_level2_names = tree.xpath('//*[@class="cate_detail_tit_txt"]/text()')
    count = 0
    for i in range(len(level2_roots)):
        for l2_node in level2_roots[i].xpath('./div[@class="cate_detail"]/dl'):
            level2_cate_name = l2_node.xpath('.//a[@class="cate_detail_tit_lk"]/text()')
            if level2_cate_name:
                level2_cate_name = level2_cate_name[0]
            else:
                level2_cate_name = reserve_level2_names[count]
                count += 1
            level3_names = l2_node.xpath('.//a[@class="cate_detail_con_lk"]/text()')
            level3_links = map(lambda x:x if x.startswith("https://") else basic_url+x, l2_node.xpath('.//a[@class="cate_detail_con_lk"]/@href'))
            second_cate_node = {"level1":level1_items[i], "level2":level2_cate_name, "level3":list(zip(level3_names,level3_links))}
            nodes_tree.append(second_cate_node)
    return nodes_tree  


def get_nodes(HTML_path="Category/HomePageParser/JDHomePage.html"):
    """get_lv2_nodes"""
    HTML = open(HTML_path, "rb").read()
    return get_tree_node(HTML=HTML, basic_url="https:")

def test():
    for lv2Node in get_nodes("Category/HomePageParser/JDHomePage.html"):
        pprint.pprint(lv2Node)
