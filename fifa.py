import pandas as pd
from bokeh.io import show
from bokeh.models import CustomJS, Select, ColumnDataSource, Column
from bokeh.plotting import figure, output_file
from bokeh.layouts import layout, row
from bokeh.io import curdoc, output_notebook

file = r"C:/Users/hzs_J/Desktop/FIS/fifa19_new.xls"
df = pd.read_excel(file)
df = df.dropna(axis=0, subset=['Club'], how='any')
list_club = df.drop_duplicates(subset=['Club'])['Club'].values.tolist()
list_attribute = df.columns.values.tolist()[54:88]

# output_file('data/fifa_team.html')
output_notebook()


def get_figure(df_data):
    name = df_data[df_data['Club'] == select_club.value]['Name']
    attribute = df_data[df_data['Club'] == select_club.value][select_attribute.value].astype(float)
    # new_data = {'name': [name], 'attribute': attribute}
    # source = ColumnDataSource(data=dict(name=[], attribute=[]))
    p = figure(x_range=name, plot_width=1500, plot_height=600)  # x轴是Categorical Data时需指明x_range=？
    p.vbar(x=name, top=attribute, width=0.5, bottom=0)
    p.xaxis.major_label_orientation = 1  # x轴label斜着显示
    # source.stream(new_data)
    return p


# 数据更新函数
def update(attr, old, new):
    layout.children[1] = get_figure(df)  # 将第二子图更新


select_club = Select(title="Club:", value=list_club[0], options=list_club)
select_club.js_on_change("value", CustomJS(code="""console.log('select: value=' + this.value, this.toString())"""))

select_attribute = Select(title="Attribute:", value=list_attribute[0], options=list_attribute)
select_attribute.js_on_change("value", CustomJS(code="""console.log('select: value=' + this.value, this.toString())"""))
select_attribute.on_change("value", update)
select = row(select_club, select_attribute)  # 小部件和图横向排列

layout = Column(select, get_figure(df))  # 小部件和图横向排列
curdoc().add_root(layout)  # 添加layout
curdoc().title = "test--bokeh"  # 标题设置


# bokeh serve --show D:\python_workspace\fifa.py