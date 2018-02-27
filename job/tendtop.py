
class tank:

    def __new__(cls, *args, **kwargs):
        wens = args[2]
        if wens not in ('W', 'E', 'N', 'S'):
            return None
        return object.__new__(cls)

    def __init__(self, x, y, wens):
        self.x = x
        self.y = y
        self.wens = wens

    def coord(self):
        return self.x, self.y

    def direction(self):
        return self.wens

    def set_coord(self, x, y, wens):
        self.x = x
        self.y = y
        self.wens = wens

    def __repr__(self):
        return '坐标:{}, 方向:{}'.format((self.x, self.y), self.wens)


class interceptor:

    def __init__(self):
        self.tanks = []  # 存储多个坦克实例
        self.tanks_coord = [] # 存储所有坦克的坐标
        self.wens_xy = {'W': -1, 'E': 1, 'N': 1, 'S': -1}
        self.wens_lr = {'WL': 'S', 'WR': 'N','EL': 'N', 'ER': 'S','NL': 'W', 'NR': 'E','SL': 'E', 'SR': 'W'}

    # 接收坦克位置及信号
    def intercept(self):
        while True:
            pace = input("请输入坦克坐标、运行方向及信号（例:11,39,W,MTMPRPM）: ")
            if pace == 'exit':
                break
            if pace == "all":
                self.output(pace)
            pace = pace.upper().split(',')
            if len(pace) < 3:
                continue
            index = self.tank_process(pace)
            self.output(index)

    # 坦克队列
    def tank_process(self, pace):
        x, y, index = 0, 0, -1
        try:
            x, y, wens = int(pace[0]), int(pace[1]), pace[2].upper()
        except ValueError as e:
            print(e)
            return None

        if (x, y) in self.tanks_coord:
            index = self.tanks_coord.index((x, y))
        else:
            t = tank(x, y, wens)
            if not t:
                return None
            self.tanks.append(t)
            self.tanks_coord.append(t.coord())
        if len(pace) == 4:
            x, y, wens = self.interpret_signal(index, pace[3])
            self.tanks[index].set_coord(x, y, wens)
            self.tanks_coord[index] = (x, y)
        return index

    # 计算坦克位置
    def interpret_signal(self, index, signal):
        x, y = 0, 0
        tmp_direction = self.tanks[index].direction()
        for s in signal:
            if s == "L" or s == "R":
                tmp_direction = self.wens_lr[tmp_direction+s]
            if s == "M":
                if tmp_direction in ('W', 'E'):
                    x += self.wens_xy[tmp_direction]
                else:
                    y += self.wens_xy[tmp_direction]
        x += self.tanks_coord[index][0]
        y += self.tanks_coord[index][1]
        return x, y, tmp_direction

    # 销毁坦克
    def destroy_tank(self, x, y):
        index = self.tanks_coord.index((x, y))
        del self.tanks[index]
        del self.tanks_coord[index]

    # 输出方法，测试使用
    def output(self, index):
        if index == "all":
            for t in self.tanks:
                print(t)
        else:
            try:
                print(self.tanks[index])
            except TypeError as e:
                print("未创建坦克")


if __name__ == "__main__":
    signal = 'MTMPRPMTMLMRPRMTPLMMTLMRRMP'
    itr = interceptor()
    itr.intercept()