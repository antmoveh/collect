
from memory_profiler import profile


@profile
def my_func():
    a = [1] *(10 ** 6)
    b = [2] *(2 * 10 ** 7)
    del b
    return a


if __name__ =='__main__':
    my_func()

"""
python -m memory_profiler example.py
"""

"""
图形化展示脚本内存使用情况
mprof run script.py
mprof plot
其他方法
mprof run: running an executable, recording memory usage
mprof plot: plotting one the recorded memory usage (by default, the last one)
mprof list: listing all recorded memory usage files in a user-friendly way.
mprof clean: removing all recorded memory usage files.
mprof rm: removing specific recorded memory usage files
"""

"""
跟踪父进程和子进程的内存使用情况
父子进程汇总: mprof run --include-children script.py
子进程独立: mprof run --multiprocess script.py
"""

"""
断点调试
1.调试函数必须使用@profile修饰
2.python -m memory_profiler --pdb-mmem = 100 my_script.py 
"""

"""
API 返回一段时间内内存使用情况
memory_usage（proc = -1， interval = .1， timeout = None
proc pid 不一定是python程序
"""

from memory_profiler import memory_usage
mem_usage = memory_usage(proc=-1, interval=.2, timeout=1)
print(mem_usage)


import time
def f(a, n=100):
    time.sleep(2)
    b = [a] * n
    time.sleep(1)
    return b
memory_usage((f, (1,), {'n': int(1e6)}))   # 有问题 测试报错


"""
写入文件
fp=open('memory_profiler.log','w+')
@profile(stream=fp)
def my_func():
     a = [1] * (10 ** 6)
     b = [2] * (2 * 10 ** 7)
.    del b
     return a
    
# 写入log
from memory_profiler import LogFile
import sys
sys.stdout = LogFile('memory_profile_log')

sys.stdout = LogFile('memory_profile_log', reportIncrementFlag=False)
"""