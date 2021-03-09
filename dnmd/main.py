import threading

from dnmd_demo import Dnmd
import multiprocessing as mp
from multiprocessing import Pool,Lock
from concurrent.futures import ProcessPoolExecutor
if __name__ == '__main__':
    user_infos = {
        'zk':{'id':'201705021128',
              'psw':'119019',
              'email':''},
        'wsx':{'id':'201705021118',
               'psw':'311610',
               # 'email': '2231733504@qq.com'
               },
        'jsc':{'id':'201705021416',
               'psw':'07181x',
               # 'email': '1838544232@qq.com'
               },
        'xh':{'id':'201705021121',
              'psw':'13001X'
              },
        'jlf':{'id':'201705021113',
               'psw':'090534',
               # 'email': '1341699342'
               }
    }
    # s = Dnmd()
    #
    # for user_info in user_infos:
    #     inner_info = user_infos[user_info]
    #     print(inner_info)
    #     # pool.apply_async(s.login(inner_info.get('id'), inner_info.get('psw')))
    #     # s.login(inner_info.get('id'), inner_info.get('psw'))
    #     s.login(**inner_info)
    #
    threads = []
    for user_info in user_infos:
        inner_info = user_infos[user_info]
        print(inner_info)
        s = Dnmd()
        threads.append(threading.Thread(target=s.login, kwargs=inner_info))
    for t in threads:
        t.start()