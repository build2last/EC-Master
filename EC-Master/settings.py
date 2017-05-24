# coding:utf-8

""" 一些参数设置 """

from __future__ import unicode_literals
from __future__ import division
import sys, os


WEB_DRIVER_PATH = 'WebCrawler\phantomjs.exe'

# 调试
DEBUG = False
# 中间 json 数据存储地址
json_dir_path = os.path.join(sys.path[0], "reviews_backup")

# 网络报文参数
AMAZON_COOKIE = r'x-wl-uid=1EVtCHAT9bT4YbLX5MmEuiBxIO+oKd1GgPVBgL3elowIPa8GBD6c1G5nJF3vAlftg+Bm0iTT2kMs=; session-token=nQIXd5IGW/5ASFZ94dN4uy5o1BqfHbGOFdPNj2gCwOeLegRjC7TRUkD58+i645NKkmRKXTsvSd37aBPBc+n8BHbUCyRTDbfilr1J0Ygo9JmcH7AWy8Tth9S0Dkr9dQVrYdh6yGd8Pgsn6QObNnLqcI+PT8X3y18g5tOfkGOSfg5QavfPWWzmrNR3/pqtYjmmcRNyHt5RpHOREEUVZ7i//j9wfWAT0CeNUzon/NbU0K8y38Kj4GVaeg==; ubid-acbcn=457-6558609-3247136; session-id-time=2082729601l; session-id=462-7594794-6582925; csm-hit=VSX8GKX6Y2ZRXTNZV5JE+s-FYV80718RQX2M065EV6A|1494149715446'
TMALL_COOKIE = r'tk_trace=1; cookie2=1c782755a8626053217e1e93595565fa; t=4edaf655cb0d6e3b37841bb30c0cd95e; _tb_token_=OGB7zk7y6ZBZ; tt=tmall-main; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; cna=0giCETjUSnMCAdvmVOYN/wTK; pnm_cku822=172UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FQHRIcUpyS3JNcCY%3D%7CU2xMHDJ7G2AHYg8hAS8XLQMjDVEwVjpdI1l3IXc%3D%7CVGhXd1llXGhXY19mXWVcZVpnUG1PdE52Sn9Ce0J3Sn5BfkZ7TmA2%7CVWldfS0TMw8zCTAQLBU1G0YiRi9ENB8%2FBiYaP2lMYjRi%7CVmhIGCUFOBgkGiMXNw86ATUVKRcsFzcNNgMjHyEaIQE7BDFnMQ%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1349*5869-client%3A1349*638-offset%3A1349*5869-screen%3A1366*768; cq=ccp%3D1; l=Aigok8UbcolT3KQLmYv871LWeBwzR4xE; isg=AoaGbd8JIm3YYPYJsbj8xNUc13zQ6cqhqG_1x3CmZKmbcyWN2HXtsYlDPRhF'

# Data base settings:
## Mysql

MYSQL_DOMIN = "localhost"
MYSQL_USER = "root"
MYSQL_PA = "liukun"
MYSQL_DB = "ec"


# 商品关键词
keywords = ["衬衫"]