# coding:utf-8
""" 处理抓取失败的页面 """

__python_version__ = "3.6"

import os
import threading
import logging
import time
import urllib
from urllib import request
import settings

log_file = "异常访问处理.log"
# 传送日志设置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_file,
                    filemode='a')

console = logging.StreamHandler()  
console.setLevel(logging.DEBUG)  
formatter = logging.Formatter('%(name)s[%(levelname)s]: %(message)s \n')  
console.setFormatter(formatter)  
# 将定义好的console日志handler添加到root logger  
logging.getLogger('').addHandler(console)  

headers = {
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
TIME_OUT = 20


def handle_failure(fail_page_que):
    print("Exception tracker is on line!!!!")
    while threading.active_count()>2:
        # print(threading.active_count())
        time.sleep(2)
        url, key_words, goods_id, page_index = fail_page_que.get()
        save_to = os.path.join(settings.json_dir_path, "%s_%s_%d.json"%(key_words, goods_id, page_index))
        try:
            try:
                req = request.Request(url, None, headers)
                resp = request.urlopen(req, None, TIME_OUT)
                content = resp.read()
                if "anti_Spider" in content.decode("utf-8", "ignore"):
                    logging.info("Fail to request %s for [%s]"%(url, "Anti-spider"))
                    continue
                with open(save_to, "wb") as fw:
                    fw.write(content)
                    print("Exception-process success!")
            except urllib.error.URLError as e:
                logging.info("Fail to request %s for [%s]"%(url, str(e.code)))
        except Exception as e:
            logging.error("Fault to request for %s"%str(e))
    print("Exception tracker handler is off......")

"""
100-199 用于指定客户端应相应的某些动作。 
200-299 用于表示请求成功。 
300-399 用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息。 
400-499 用于指出客户端的错误。 
500-599 用于支持服务器错误。
"""