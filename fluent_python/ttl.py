import time
from functools import wraps
from typing import Dict, Tuple


def impose(func):
    """同一个手机号一定时间内访问次数统计， key:(count, time)"""
    visit_times: Dict[str, Tuple[int, int]] = {"last_clean": (0, 0)}

    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = count = 1
        print(visit_times)
        key = args[0]
        _last = int(time.time())
        if key in visit_times:
            count = visit_times[key][0]
            last_time = visit_times[key][1]
            if (_last - last_time) < 5 and count > 10:
                """对于一定时间内访问次数过多的key,可做进一步处理"""
                if (_last - visit_times["last_clean"][1]) > 3600:
                    """清理过多的key,防止占用太多内存"""
                    for k in list(visit_times):
                        if (_last - visit_times[k][1]) > 3600:
                            del visit_times[k]
                    visit_times["last_clean"] = (0, _last)
            else:
                resp = func(*args, **kwargs)
            count += 1 if count < 20 else 0  # 限制统计最大次数，防止值过大引起异常
        else:
            resp = func(*args, **kwargs)
        visit_times[key] = (count, _last)
        return resp
    return wrapper


@impose
def test(phone):
    return phone


for i in range(30):
    time.sleep(1)
    print(test("2333333"))