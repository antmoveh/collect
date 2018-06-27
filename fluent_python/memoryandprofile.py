


"""
Python中的内存管理涉及一个包含所有Python对象和数据结构的私有堆。
Python内存管理器通过本文档中列出的Python / C API函数根据需要为Python对象和其他内部缓冲区分配堆空间。
不应该试图与C库的函数的Python对象进行操作：malloc()， calloc()，realloc()和free()。这将导致C分配器和Python内存管理器之间的混合调用带来致命后果
PYTHONMALLOC 环境变量可以用来配置Python使用的内存分配器
Python内存管理器具有不同的组件，可处理各种动态存储管理方面的问题，如共享，分割，预分配或缓存。
I / O缓冲区的内存请求由C库分配程序处理。Python内存管理器只涉及作为结果返回的字符串对象的分配。
"""

"""
Python有一个pymalloc分配器，针对小型对象（小于或等于512字节）进行了优化，并具有较短的生命周期
"""

"""
         i/o缓存管道
object --------------->内存API（pymalloc, calloc realloc, free等）--------->内存存储（共享，分割，预分配、缓存等）
"""


# ---------------------------------------------------------------------------------------
# 内存分析工具memory_profiler，可以分析行级、方法级、进程/子进程,某个时间段等内存使用情况
# ----------------------------------------------------------------------------------------

from memory_profiler import profile
@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a
my_func()

"""
也可以 python -m memory_profiler example.py
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
memory_usage((f, (1,), {'n': int(1e6)}))  # 有问题 测试报错

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