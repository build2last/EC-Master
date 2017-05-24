# coding:utf-8
""" 网络访问和页面下载中间件 """

# Todo: 实现自动获取网站 cookie
# ------------------------------
# filename = 'amazon_cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
# cookie = cookielib.MozillaCookieJar(filename)
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
# 模拟登录，并把cookie保存到变量
# result = opener.open(review_url)
# 保存cookie到cookie.txt中
# cookie.save(ignore_discard=True, ignore_expires=True)
# 利用cookie请求访问另一个网址
# result = opener.open(review_url)
# review_page_content = result.read().decode("utf-8")
# -------------------------

__python__ = 3.6

import urllib
import time
import selenium.webdriver.support.ui as ui
from selenium import webdriver
import settings
import pymysql as MySQLdb
from urllib import request


headers = {
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
req_timeout = 40


def create_table_in_mysql():
    create_table_cmd = """CREATE TABLE IF NOT EXISTS url_content (
          id int(20) not null AUTO_INCREMENT,
          url varchar(400) NOT NULL UNIQUE,
          content mediumblob,
          detail text,
          status int DEFAULT 0,
          PRIMARY KEY (id)
        ) ENGINE=InnoDB, DEFAULT CHARSET=utf8;"""
    with MySQLdb.connect(settings.MYSQL_DOMIN, settings.MYSQL_USER, settings.MYSQL_PA, settings.MYSQL_DB, charset="utf8") as cursor:
        cursor.execute(create_table_cmd)
        data = cursor.fetchone()
        print("Database version : %s " % data)


def read_page_from_MySQL(url):
    with MySQLdb.connect(settings.MYSQL_DOMIN, settings.MYSQL_USER, settings.MYSQL_PA, settings.MYSQL_DB, charset="utf8") as cursor:
        cursor.execute('select content from url_content where url=%s', (url,))
        result = cursor.fetchall()
        cursor.close()
    if result:
        if settings.DEBUG:
            print("MySQL found %s"%url)
        return result[0][0]
    else:
        return ""


def get_cookie(website):
    if website == "TMALL":
        return settings.TMALL_COOKIE
    elif website == "AMZ":
        return settings.AMAZON_COOKIE
    elif website == "JD":
        return ""


def url_request(url):
    html_content = ""
    if "jd.com" in url:
        # cookie = get_cookie("JD")
        try:
            req = urllib.request.Request(url, None, headers)
            resp = urllib.request.urlopen(req, None, req_timeout)
            html_content = resp.read()
        except Exception as e:
            print("读取京东页面出错 %s\n"%url + str(e))
            html_content = ""
    elif "tmall.com" in url:# and "PageComments" in url:
        cookie = get_cookie("TMALL")
        try:
            req = urllib.request.Request(url, None, headers)
            if cookie:
                req.add_header('Cookie', cookie)
            resp = urllib.request.urlopen(req, None, req_timeout)
            html_content = resp.read()
            return html_content
        except Exception as e:
            print("读取天猫页面出错 %s\n"%url + str(e))
            html_content = ""
    elif "amazon" in url:
        cookie = get_cookie("AMZ")
        try:
            req = urllib.request.Request(url, None, headers)
            if cookie:
                req.add_header('Cookie', cookie)
            # resp = urllib2.urlopen(req, None, req_timeout)
            resp = urllib.request.urlopen(req, None, req_timeout)
            html_content = resp.read()
            return html_content
        except Exception as e:
            print("读取亚马逊页面出错 %s\n"%url + str(e))
            html_content = ""
    else:
        try:
            req = urllib.request.Request(url, None, headers)
            resp = urllib.request.urlopen(req, None, req_timeout)
            html_content = resp.read()
        except Exception as e:
            print("读取页面出错 %s\n"%url + str(e))
            html_content = ""
    return html_content


def read_page(url, detail= "", use_database=False, turn_on_update=True):
    if turn_on_update and use_database:
        html_content = url_request(url)
        if not html_content:
            print("Fail to request %s"%url)
            return ""
        conn = MySQLdb.connect(settings.MYSQL_DOMIN, settings.MYSQL_USER, settings.MYSQL_PA, settings.MYSQL_DB, charset="utf8")
        cursor = conn.cursor()
        try:
            if cursor.execute('select 1 from url_content where url=%s', (url,)):
                if detail:
                    cursor.execute('update url_content set content=%s, detail=concat(detail, %s) where url=%s',
                     (MySQLdb.Binary(html_content), "+"+detail, url))
                else: 
                    cursor.execute('update url_content set content=%s where url=%s',(MySQLdb.Binary(html_content), url))
                print("Update url_content: %s"%url)
            else:
                if detail:
                    cursor.execute('insert into url_content values(%s, %s, %s, %s)', (url, MySQLdb.Binary(html_content), detail, 0))
                if settings.DEBUG:
                    print("%s inserted"%url)
            conn.commit()
        except Exception as e:
           print(e)
           conn.rollback()
        conn.close()
        return html_content
    elif use_database==False:
        return url_request(url)
    elif turn_on_update==False:
        content = read_page_from_MySQL(url)
        if content:
            return content
        else:
            html_content = url_request(url)
            conn = MySQLdb.connect(settings.MYSQL_DOMIN, settings.MYSQL_USER, settings.MYSQL_PA, settings.MYSQL_DB, charset="utf8")
            cursor = conn.cursor()
            try:
                if detail:
                    cursor.execute('update url_content set content=%s, detail=concat(detail,%s) where url=%s',
                     (MySQLdb.Binary(html_content), "+"+detail, url))
                else: 
                    cursor.execute('update url_content set content=%s where url=%s',(MySQLdb.Binary(html_content), url))
                if settings.DEBUG:
                    print("%s inserted"%url)
                conn.commit()
            except Exception as e:
               print(e)
               conn.rollback()
            conn.close()
            return html_content



def render_js(url):
    """
        返回 unicode 字串
    """
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.disk-cache"] = True
    cap["phantomjs.page.customHeaders.Cookie"] = ""
    driver = webdriver.PhantomJS(executable_path=settings.WEB_DRIVER_PATH, desired_capabilities=cap)
    driver.get(url)
    # 翻到底，详情加载
    js = "var q=document.documentElement.scrollTop=1000"
    driver.execute_script(js)
    wait = ui.WebDriverWait(driver,7)
    wait.until(lambda browser: browser.execute_script("return document.readyState") == "complete")
    content = driver.page_source.encode("utf-8")
    driver.quit()
    return content


# 返回一个初始化过的 PHANTOMJS driver
def PHANTOMJS_driver():
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = True
    cap["phantomjs.page.settings.disk-cache"] = True
    cap["phantomjs.page.customHeaders.Cookie"] = ""
    driver = webdriver.PhantomJS(executable_path=settings.WEB_DRIVER_PATH, desired_capabilities=cap)
    wait = ui.WebDriverWait(driver,5)
    return driver

# def main():
#     print(len(read_page("http://www.w3school.com.cn/sql/sql_update.asp", turn_on_update=False)))
#     read_page("http://www.w3school.com.cn/sql/sql_update.asp", turn_on_update=False)

# if __name__ == '__main__':
#     main()