import multiprocessing as mp
import xlrd
import os
import time


def start_mult(log_dir, xlsx_file, sheet_index, col_index, dst_file):
    search_str = xlrd.open_workbook(filename=xlsx_file).sheet_by_index(sheet_index).col_values(col_index)
    conn1, conn2 = mp.Pipe(duplex=False)
    pool = mp.Pool(processes=mp.cpu_count())
    p2 = mp.Process(target=handle, args=(search_str, dst_file, conn1))
    p2.start()
    for fn in os.listdir(log_dir):
        pool.apply_async(func=serach, args=(log_dir + fn, search_str, conn2))
    pool.close()
    pool.join()


def handle(search_str, dst_file, conn1):
    print("start recv database")
    while True:
        try:
            search_str.remove(conn1.recv())
        except ValueError as e:
            continue
        except EOFError as e:
            break
    print(len(search_str))
    with open(dst_file, mode='w', encoding='utf-8') as f:
        for order_list in search_str:
            f.write(order_list)
            f.write('\n')


def serach(log_file, search_str, conn2):
    try:
        print("Searcing file '" + log_file  + "'...")
        with open(log_file, mode='r', encoding='utf-8') as f:
            l = f.read()
            for s_s in search_str:
                if s_s in l:
                    conn2.send(s_s)
    except Exception as e:
        return str(e)
    return None


if __name__ == "__main__":
    print(time.time())
    start_mult(log_dir="F:/logfile/", xlsx_file="F:/order.xlsx", sheet_index=0, col_index=0, dst_file='F:/orders_list.txt')
    print(time.time())