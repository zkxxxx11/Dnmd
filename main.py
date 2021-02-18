import threading

from dnmd_demo import Dnmd
import multiprocessing as mp
from multiprocessing import Pool,Lock
from concurrent.futures import ProcessPoolExecutor
if __name__ == '__main__':
    user_infos = {
        'zk':{'id':'xxxxxxx',
              'psw':'xxxxxxx',
              'email':''},

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