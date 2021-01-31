from dnmd_demo import Dnmd
import multiprocessing as mp
from multiprocessing import Pool,Lock
from concurrent.futures import ProcessPoolExecutor
if __name__ == '__main__':
    user_infos = {
        'zk':{'id':'xxxxxxxxxxxxxxxx',
              'psw':'xxxxxxxxxxx'},

    }
    work_count = 3
    # with ProcessPoolExecutor(work_count) as pool:
    #     for i, j in enumerate(user_infos):
    #         inner_info = user_infos[j]
    #         print(i, user_infos[j])
    #         pool.submit(s.login(inner_info.get('id'), inner_info.get('psw')))  # 执行
    pool = Pool(1)
    s = Dnmd()
    for user_info in user_infos:
        inner_info = user_infos[user_info]
        print(inner_info)
        pool.apply_async(s.login(inner_info.get('id'), inner_info.get('psw')))
    # 31407
    # s.login(id, psw)