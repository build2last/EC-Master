# coding:utf-8

import pprint

from lxml import etree



# HTML expected to be UTF-8 file
def get_tree_node(HTML, basic_url="https://www.amazon.cn"):
    nodes_tree = []
    import pprint
    tree = etree.HTML(HTML)
    cate_nodes = tree.xpath('//*[@class="a-row a-spacing-small a-spacing-top-medium"]')
    for node in cate_nodes:
        level1_cate_name = ",".join(node.xpath('./div[1]/span//a/text()'))
        level2_cate_nodes = node.xpath('.//*[@class="a-row a-spacing-small"]')
        for no2 in level2_cate_nodes:
            level2_cate_name = no2.xpath('.//*[@class="nav_a a-link-normal a-color-state"]/text()')[0]
            level3_cates_names = no2.xpath('.//*[@class="nav_a a-link-normal a-color-base"]/text()')
            level3_cates_links = map(lambda x:basic_url+x, node.xpath('.//*[@class="nav_a a-link-normal a-color-base"]/@href'))
            level3_cates_list = list(zip(level3_cates_names, level3_cates_links))
            if level2_cate_nodes:
                second_cate_node = {"level1":level1_cate_name, "level2":level2_cate_name, "level3":level3_cates_list}
                # pprint.pprint(second_cate_node)
                nodes_tree.append(second_cate_node)

    return nodes_tree        

def get_nodes(HTML_path="Category/HomePageParser/AmaHomePage.html"):
    """Get_lv2_nodes"""
    HTML = open(HTML_path, "rb").read()
    return get_tree_node(HTML)

def test():
    # for lv2Node in get_nodes("AmaHomePage.html"):
    #     pprint.pprint(lv2Node)
    print(len(get_nodes()))