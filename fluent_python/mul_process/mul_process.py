import multiprocessing as mp
import xlrd
import os
import time
import queue


def start_mult(log_dir, xlsx_file, sheet_index, col_index, dst_file):
    search_str = xlrd.open_workbook(filename=xlsx_file).sheet_by_index(sheet_index).col_values(col_index)
    manage = mp.Manager()
    qu = manage.Queue()
    pool = mp.Pool(processes=mp.cpu_count())
    for fn in os.listdir(log_dir):
        pool.apply_async(func=serach, args=(log_dir + fn, search_str, qu))
    pool.close()
    pool.join()
    while True:
        try:
            search_str.remove(qu.get(block=False))
        except ValueError as e:
            continue
        except queue.Empty as e:
            break
    print(len(search_str))
    # with open(dst_file, mode='w', encoding='utf-8') as f:
    #     for order_list in search_str:
    #         f.write(order_list)
    #         f.write('\n')


def serach(log_file, search_str, qu):
    try:
        print("Searcing file '" + log_file  + "'...")
        with open(log_file, mode='r', encoding='utf-8') as f:
            l = f.read()
            for s_s in search_str:
                if s_s in l:
                    qu.put(s_s, block=False)
    except Exception as e:
        return str(e)
    return None


if __name__ == "__main__":
    print(time.time())
    start_mult(log_dir="F:/logfile/", xlsx_file="F:/order.xlsx", sheet_index=0, col_index=0, dst_file='F:/orders_list.txt')
    print(time.time())