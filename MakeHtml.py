from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Pie,Bar
from collections import Counter

CLASSES = ['101', '102', '103', '104', '105', '106', '107', '112', '119', '120']
OLORS = {
    '101': (128, 128, 128),
    '102': (0, 192, 255),
    '103': (202, 36, 204),
    '104': (77, 80, 192),
    '105': (0, 0, 255),
    '106': (0, 255, 255),
    '107': (245, 248, 10),
    '112': (0, 255, 0),
    '119': (0, 0, 0),
    '120': (75, 46, 72)
}
WL = [10,25,40,55,70.85]

class Classes_Pie():
    def __init__(self):
        super(Classes_Pie,self).__init__()
        self.x = []
        self.y = []
    def get_info(self, info):
        c = Counter(info)
        c = c.most_common(5)
        for i in range(len(c)):
            self.x.append(c[i][1])
            self.y.append(c[i][0])

    def bin(self, info):
        self.get_info(info)
        html = (
        Pie()
            .add("", [list(z) for z in zip(self.y, self.x)])
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布",subtitle="饼图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
         )
        return html
class Classes_Bar():
    def __init__(self):
        super(Classes_Bar,self).__init__()
        self.x = []
        self.y = []
    def get_info(self, info):
        c = Counter(info)
        c = c.most_common(5)
        for i in range(len(c)):
            self.x.append(c[i][0])
            self.y.append(c[i][1])
    def bar(self,info):
        self.get_info(info)
        html = (
        Bar()
            .add_xaxis(self.x)
            .add_yaxis("类别",self.y)
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布",subtitle="柱状图"))
        )
        return html
class WL_Bar():
    def __init__(self):
        super(WL_Bar,self).__init__()
        self.x = []
        self.y = []
    def get_info(self,w,h):
        for i in range(len(w)):
            pass

    def bar(self,w,h):
        self.get_info(w,h)
        html = (
        Bar()
        )


