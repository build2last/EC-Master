# coding:utf-8
# 一些参数设置
from __future__ import unicode_literals
from __future__ import division
import sys,os

# 调试
debug_mode = False

# 中间 json 数据存储地址
json_dir_path = os.path.join(sys.path[0],"reviews_backup") + "\\"

# 网络报文参数
AMAZON_COOKIE = 'x-wl-uid=1nmATGfbKNcKW2bSM4FF/3ZF8NYM4MoKID/g0A0DtxmGAbRYGfUQ6JyXKLWkTSxy4cldtD+iapwI=; session-token="o/yC3aFX2Xwcfan9dgPazp/7nKr9bTj6yDTQPwCH3F8GbgtMIDfbc3hoVg/z2jRj+25kKV7caZADG7X54oYxbjOb82XimoEhw9cKnoRUKKE50bI98yflA3+ibQBJh4b6MCvEOfYiSGOlTicZPYOlev48f529yYmRhh9TvQqV0edyb03VWA924hc80cNnd71ukbnmUfR38hhdAXF9t7bQV3FC/Pe6sFh8Jsc86Y0fZyR3HlHZwb2vVw=="; ubid-acbcn=479-6002062-1093330; session-id-time=2082729601l; session-id=451-7142024-2449903; csm-hit=5JQM7V9FB6AZ3RBZYA0B+s-FFPHCH4GH60R6Y4K9PV6|1490531033755'
TMALL_COOKIE = 'miid=8513969304072353584; thw=cn; hng=CN%7Czh-cn%7CCNY; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; tracknick=%5Cu6606%5Cu4ED1%5Cu98DE%5Cu8D8A; _cc_=UtASsssmfA%3D%3D; tg=0; cna=ksrJD9x0cnACAdOiGi/THDSv; l=AllZdqLhL-SdNLtWgUad5-5O6U8z5k2Y; isg=Ajk51K7TRf8GlhYsdw7L7IYASKVtYi34zTA7dFtutWDf4ll0o5Y9yKcyElHu; _tb_token_=5ahp6FeaNGhA; v=0; cookie2=62239553bb3cc9d0ad557f1c1ae21127; t=03ee49e5fe3560f206e9502c150de389'

# Data base settings:
## Mysql
mysql_url = "localhost"
ms_user = "root"
ms_pa = "liukun"
ms_db = "reviews"

# 商品关键词
keywords = ["笔记本电脑"]

test_table = "nlp_sample"

# if __name__ == "__main__":
# 	print(json_dir_path)
# 	job.do_job()
