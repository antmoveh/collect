import re

"""
常用方法
re.search() re.compile() re.findall() re.finditer() re.sub() re.match() re.split()
模式
re.M(多行匹配，影响^$) re.I(大小写不敏感)re.S(使.匹配所有信息)
re.L(本地化识别\w\W取决于当前环境) re.A(Unicode匹配，没啥用)
re.DEBUG(调试信号，输出更多编译信息)
re.X(易读的方式编写正则表达式)
"""


# 1、 s1 = "get-element-by-id" 转换为驼峰命名法形式的字符串  getElementById
def underline_to_hump(s):
    def hump(matched):
        return str.upper(matched.group()[1])
    return re.sub("-\w", hump, s)


# 2、判断字符串是否包含数字
def contains_number(s):
    return bool(re.findall("\d", s))


# 3、判断电话号码
def is_phone(s):
    c = re.compile(r"^1[34578]\d{9}$")
    return bool(c.match(s))


# 4、判断是否符合指定格式
# 给定字符串str，检查其是否符合如下格式
# XXX-XXX-XXXX
# 其中X为Number类型
def matches_pattern(s):
    c = re.compile(r"\d{3}-\d{3}-\d{4}$")
    return bool(c.match(s))


# 5、判断是否符合USD格式
# 给定字符串 str，检查其是否符合美元书写格式
# 以 $ 开始
# 整数部分，从个位起，满 3 个数字用 , 分隔
# 如果为小数，则小数部分长度为 2
# 正确的格式如：$1,023,032.03 或者 $2.03，错误的格式如：$3,432,12.12 或者 $34,344.3**
def is_usd(s):
    c = re.compile(r"^\$\d{1,3}(,\d{3})*(\.\d{2})?$")
    return bool(c.match(s))


# 6、实现千位分隔符
def thousand_split(number):
    c = re.compile(r"\d{1,3}(?=(\d{3})*$)")

    def add_comma(matched):
        return matched.group() + ","
    return c.sub(add_comma, number)[:-1]


# 7、获取 url 参数
# 获取 url 中的参数
# 指定参数名称，返回该参数的值 或者 空字符串
# 不指定参数名称，返回全部的参数对象 或者 {}
# 如果存在多个同名参数，则返回数组
def get_url_param(url, param="\w+"):
    c = re.compile(r"({key})=(?P<value>\w+)".format(key=param))
    return dict(c.findall(url))


# 8、验证邮箱
def is_email(email):
    c = re.compile(r"^([\w_\-.])+@([\w_\-])+(\.[\w_\-]+)$")
    return bool(c.match(email))


# 9、验证身份证号码
# 身份证号码可能为15位或18位，15位为全数字，18位中前17位为数字，最后一位为数字或者X
def is_card_no(number):
    c = re.compile(r"(^\d{15}$)|(^\d{18}$)|(^\d{17}(X|x))$")
    return bool(c.match(number))


# 10、匹配汉字
re.compile(r"^[\u4E00-\u9FA5]{0,}")


# 11、去除首尾的'/'
# str = '////ercc//ee//////';
c = re.compile(r"^/*|/*$")
m = c.sub("", "////ercc//ee//////")

# 12、判断日期格式是否符合 '2017-05-11'的形式，简单判断，只判断格式
re.compile(r"^\d{4}-\d{1,2}-\d{1,2}$")


# 13、判断日期格式是否符合 '2017-05-11'的形式，严格判断（比较复杂）
re.compile(r"^(?:(?!0000)[0-9]{4}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[0-9]{2}(?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00)-02-29)$")


# 14、IPv4地址正则
re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")


# 15、十六进制颜色正则
re.compile(r"^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")


# 16、车牌号正则
re.compile(r"^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$")


# 17、匹配HTML标签
s = "<p>dasdsa</p>nice <br> test</br>"
# c = re.compile(r"<[^<>]+>")
# print(c.findall(s))


# 18、密码强度正则，最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符
# 先行断言用法
re.compile(r"^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$")


# 19、URL正则
url = "https://www.api33open.top/user/test/heh/hb?id=27610708&page=1"
x = re.compile(r"^((https?|ftp|file)://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$")
re.compile(r"(?:http|https)://(?:[\w.]+)/(?:\w+/|\w+)+\?(?:\w+=\w+&|\w+=\w+)*", re.I|re.M)

# 20、匹配浮点数
re.compile(r"^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$")


# 21、<OPTION value="待处理">待处理</OPTION>
# 写一个正则表达式,匹配 "<OPTION value="待处理">"
s1 = '<OPTION value="待处理">待处理</OPTION>'
re.compile(r"^<.*?>")
