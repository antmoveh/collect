import xlrd, os, threading, queue


def walk_files(log_file, orders_list, order_queue):
    try:
        print("Searcing file '" + log_file  + "'...")
        fp = open(log_file, mode='r', encoding='utf-8')
        for line in fp.readlines():
            for order_list in orders_list:
                if line.find(order_list) > -1:
                    order_queue.put(order_list)
                    orders_list.remove(order_list)
                    break
        fp.close()
    except Exception as e:
        return str(e)
    else:
        if fp != None:
            fp.close()
    return None


def search_order(order, log_file):
    wookbook = xlrd.open_workbook(filename=order)
    sheet1 = wookbook.sheet_by_index(0)
    orders_list = sheet1.col_values(0)
    filename = os.listdir(log_file)
    order_queue = queue.Queue()
    ths = []
    for fn in filename:
#        walk_files(log_file + fn, orders_list, order_queue)
        t = threading.Thread(target=walk_files, args=(log_file + fn, orders_list, order_queue))
        ths.append(t)
    for t in ths:
        print("11")
        t.start()
    for t in ths:
        t.join()
    while True:
        try:
            orders_list.remove(order_queue.get(block=False))
        except ValueError as e:
            continue
        except queue.Empty as e:
            break
    print(len(orders_list))


if __name__ == "__main__":
    import time
    order = "F:/order.xlsx"
    log_file = "F:/logfile/"
    print(time.time())
    search_order(order, log_file)
    print(time.time())