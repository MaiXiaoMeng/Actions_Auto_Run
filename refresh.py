from scripts.tieba_baidu_com import tieba_baidu_com
from scripts.cloud_189_cn import cloud_189_cn
from scripts.www_mikugal_com import www_mikugal_com

if __name__ == '__main__':
    www_mikugal_com().run()
    cloud_189_cn().run()
    tieba_baidu_com().run()
