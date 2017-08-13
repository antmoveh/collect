import math
from pyecharts import Polar

data = []
for i in range(5):
    for j in range(101):
        theta = j / 100 * 360
        alpha = i * 360 + theta
        r = math.pow(math.e, 0.003 * alpha)
        data.append([r, theta])
polar = Polar("极坐标系示例")
polar.add("", data, symbol_size=0, symbol='circle', start_angle=-25, is_radiusaxis_show=False,
          area_color="#f3c5b3", area_opacity=0.5, is_angleaxis_show=False)
polar.show_config()
polar.render()