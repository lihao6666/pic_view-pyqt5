from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Line,Scatter,Grid, Page
from collections import Counter
from pyecharts.globals import CurrentConfig

CurrentConfig.ONLINE_HOST = "C:\\Users\\lh\\Desktop\\图片分类查询系统\\js\\"


CLASSES = ['101', '102', '103', '104',
           '105', '106', '107', '112', '119', '120']
COLORS = {
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

WIDTH_AND_HEIGHT_CLASSES = ["A","B","C","D","E"]
WIDTH_AND_HEIGHT_RATE = [0.5,1,2,2.5]

# 卫星区域像素个数比例饼状图
class Pixel_Bar_Pie():
    def __init__(self):
        super(Pixel_Bar_Pie, self).__init__()
        self.x = []
        self.y = []

    def make_bar_pie(self,infoX,infoY):
        pie = (
            Pie(init_opts=opts.InitOpts(width="1000px", height="800px"))
            .add("", [list(z) for z in zip(infoX, infoY)])
            .set_global_opts(title_opts=opts.TitleOpts(title="像素分布", subtitle="饼图"))
            # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )

        bar = (
            Bar(init_opts=opts.InitOpts(width="1000px", height="800px"))
            .add_xaxis(infoX)
            .add_yaxis("像素数量",infoY)
            .set_global_opts(title_opts=opts.TitleOpts(title="像素分布", subtitle="柱状图"))
        )
        page = Page()#这里可以添加js_host
        page.add(pie, bar)

        return page



# 类别折线和直方图

class Classes_Bar_Line():
    def __init__(self):
        super(Classes_Bar_Line, self).__init__()
        self.x = []
        self.y = []

    def get_info(self, info):
        c = Counter(info)
        c = c.most_common(5)
        for i in range(len(c)):
            self.x.append(c[i][1])
            self.y.append(c[i][0])

    def make_bar_line(self, info):
        self.get_info(info)

        line = (
            Line(init_opts=opts.InitOpts(width="400px", height="400px"))
            .add_xaxis(self.y)
            .add_yaxis("数量", self.x)
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布", subtitle="折线图"))
        )

        bar = (
            Bar(init_opts=opts.InitOpts(width="400px", height="400px"))
            .add_xaxis(self.y)
            .add_yaxis("数量", self.x)
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布", subtitle="柱状图", pos_top="48%"), legend_opts=opts.LegendOpts(pos_top="48%"))
        )

        grid = (
            Grid()
            .add(line, grid_opts=opts.GridOpts(pos_bottom="60%"))
            .add(bar, grid_opts=opts.GridOpts(pos_top="60%"))
        )
        return grid
# 类别饼图和直方图


class Classes_Bar_Pie():
    def __init__(self):
        super(Classes_Bar_Pie, self).__init__()
        self.x = []
        self.y = []

    def get_info(self, info):
        c = Counter(info)
        c = c.most_common(5)
        for i in range(len(c)):
            self.x.append(c[i][1])
            self.y.append(c[i][0])

    def make_bar_pie(self, info):
        self.get_info(info)

        pie = (
            Pie(init_opts=opts.InitOpts(width="620px", height="420px"))
            .add("", [list(z) for z in zip(self.y, self.x)])
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布", subtitle="饼图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )

        bar = (
            Bar(init_opts=opts.InitOpts(width="620px", height="420px"))
            .add_xaxis(self.y)
            .add_yaxis("数量", self.x)
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布", subtitle="柱状图"))
        )
        page = Page()#这里可以添加js_host
        page.add(pie, bar)

        return page
# 形态分布组合图表


class WH_AREA_Compose():
    def __init__(self):
        super(WH_AREA_Compose, self).__init__()
        self.WIDTHX = [
            '<20',
            '20-35',
            '35-50',
            '50-65',
            '65-80',
            '>=80'
        ]
        self.WIDTHY = [0, 0, 0, 0, 0, 0]
        self.HEIGHTX = [
            '<20',
            '20-35',
            '35-50',
            '50-65',
            '65-80',
            '>=80'
        ]
        self.HEIGHTY = [0, 0, 0, 0, 0, 0]
        self.AREAX = [
            '<400',
            '400-2400',
            '2400-4400',
            '4400-6400',
            '>=6400'
        ]
        self.AREAY = [0, 0, 0, 0, 0]
        self.AREAS = []

    def get_info(self, width, height):
        for wid in width:
            if wid >= 80:
                self.WIDTHY[5] += 1
            else:
                self.WIDTHY[((wid-20) // 15)+1] += 1
        for hgt in height:
            if hgt >= 80:
                self.HEIGHTY[5] += 1
            else:
                self.HEIGHTY[((hgt-20) // 15)+1] += 1
        for i in range(len(width)):
            self.AREAS.append(width[i]*height[i])
            if width[i]*height[i] >= 6400:
                self.AREAY[4] += 1
            else:
                self.AREAY[(width[i]*height[i]-400) // 2000+1] += 1
    def make_wh_bar(self):
        bar = (
        Bar(init_opts=opts.InitOpts(width="620px", height="420px"))
            .add_xaxis(self.WIDTHX)
            .add_yaxis("长", self.HEIGHTY)
            .add_yaxis("宽", self.WIDTHY)
            .set_global_opts(title_opts=opts.TitleOpts(title="长宽分布", subtitle="柱状图"))
        )
        return bar
    def make_area_bar(self):
        bar = (
        Bar(init_opts=opts.InitOpts(width="620px", height="420px"))
            .add_xaxis(self.AREAX)
            .add_yaxis("面积", self.AREAY)
            .set_global_opts(title_opts=opts.TitleOpts(title="面积分布", subtitle="柱状图"))
        )
        return bar
    def make_area_scatter(self):
        
        scatter = (
        Scatter(init_opts=opts.InitOpts(width="620px", height="420px"))
            .add_xaxis(range(len(self.AREAS)))
            .add_yaxis("面积",self.AREAS)
            .set_global_opts(title_opts=opts.TitleOpts(title="面积分布",subtitle = "散点图"),visualmap_opts=opts.VisualMapOpts(type_="size", max_=10000, min_=200))
        )
        return scatter
    
    def make_compose(self,width,height):
        self.get_info(width,height)
        page = Page(layout = Page.SimplePageLayout)
        page.add(self.make_wh_bar(),self.make_area_bar(),self.make_area_scatter())
        return page


# 长宽比可视化饼图和直方图

class WH_Bi_Bar_Pie():
    def __init__(self):
        super(WH_Bi_Bar_Pie, self).__init__()
        self.x = []
        for i in range(len(WIDTH_AND_HEIGHT_CLASSES)):
            if i<1:
                self.x.append(WIDTH_AND_HEIGHT_CLASSES[i]+": <"+str(WIDTH_AND_HEIGHT_RATE[i]))
            elif 1<=i<len(WIDTH_AND_HEIGHT_CLASSES)-1:
                self.x.append(WIDTH_AND_HEIGHT_CLASSES[i]+": "+str(WIDTH_AND_HEIGHT_RATE[i-1])+"-"+str(WIDTH_AND_HEIGHT_RATE[i]))
            else:
                self.x.append(WIDTH_AND_HEIGHT_CLASSES[i]+": >"+str(WIDTH_AND_HEIGHT_RATE[i-1]))

        print(self.x)
                
    def make_bar_pie(self,list2,list1):

        pie = (
            Pie(init_opts=opts.InitOpts(width="620px", height="420px"))
            .add("", [list(z) for z in zip(WIDTH_AND_HEIGHT_CLASSES, list1)])
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布", subtitle="饼图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )

        bar = (
            Bar(init_opts=opts.InitOpts(width="620px", height="420px"))
            .add_xaxis(self.x)
            .add_yaxis("数量", list1)
            .set_global_opts(title_opts=opts.TitleOpts(title="类别分布", subtitle="柱状图"))
        )
        page = Page()#这里可以添加js_host
        page.add(pie, bar)

        return page


# class Classes_Pie():
#     def __init__(self):
#         super(Classes_Pie,self).__init__()
#         self.x = []
#         self.y = []
#     def get_info(self, info):
#         c = Counter(info)
#         c = c.most_common(5)
#         for i in range(len(c)):
#             self.x.append(c[i][1])
#             self.y.append(c[i][0])

#     def bin(self, info):
#         self.get_info(info)
#         html = (
#         Pie(init_opts=opts.InitOpts(width="620px", height="420px"))
#             .add("", [list(z) for z in zip(self.y, self.x)])
#             .set_global_opts(title_opts=opts.TitleOpts(title="类别分布",subtitle="饼图"))
#             .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#          )
#         return html
# class Classes_Bar():
#     def __init__(self):
#         super(Classes_Bar,self).__init__()
#         self.x = []
#         self.y = []
#     def get_info(self, info):
#         c = Counter(info)
#         c = c.most_common(5)
#         for i in range(len(c)):
#             self.x.append(c[i][0])
#             self.y.append(c[i][1])
#     def bar(self,info):
#         self.get_info(info)
#         html = (
#         Bar(init_opts=opts.InitOpts(width="620px", height="420px"))
#             .add_xaxis(self.x)
#             .add_yaxis("类别",self.y)
#             .set_global_opts(title_opts=opts.TitleOpts(title="类别分布",subtitle="柱状图"))
#         )
#         return html
# class WL_Bar():
#     def __init__(self):
#         super(WL_Bar,self).__init__()
#         self.x = []
#         self.y = []
#     def get_info(self,w,h):
#         for i in range(len(w)):
#             pass

#     def bar(self,w,h):
#         self.get_info(w,h)
#         html = (
#         Bar()
#         )
