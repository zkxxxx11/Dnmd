import redis


def get_conn():
    conn = redis.StrictRedis(host='127.0.0.1',
                             port=6379,
                             db=0,
                             password='')
    return conn