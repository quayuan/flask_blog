import signal
import time
from functools import wraps


def timer(func):
    """测量函数执行时间的装饰器"""

    @wraps(func)
    def inner_func(*args, **kwargs):
        t0 = time.time()
        result_ = func(*args, **kwargs)
        t1 = time.time()
        print("Time running %s: %s seconds" % (func.__name__, str(t1 - t0)))
        return result_

    return inner_func


def after_timeout():
    print(f'\033[1;31m Error : Function run timeout ! \033[0m \n')


def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                print('start alarm signal.')
                r = func(*args, **kwargs)
                print('close alarm signal.')
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                print(f'Function run timeout ：{func.__name__}')
                callback()

        return to_do

    return wrap
