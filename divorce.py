from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper
)
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure

from bokeh.sampledata.us_cities import data as cities
from bokeh.sampledata.us_marriages_divorces import data as divorces

palette.reverse()

cities = {
    code: int(city for code, city in cities.items() if city["state"] == "ny")}

city_xs = [city["lons"] for city in cities.values()]
city_ys = [city["lats"] for city in cities.values()]

city_names = [city['name'] for city in cities.values()]
city_rates = [divorces[city_id] for city_id in cities]
color_mapper = LogColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=city_xs,
    y=city_ys,
    name=city_names,
    rate=city_rates,
))

TOOLS = "pan,wheel_zoom,reset,hover,save"

p = figure(
    title="New York Divorce Rates, 2018", tools=TOOLS,
    x_axis_location=None, y_axis_location=None
)
p.grid.grid_line_color = None

p.patches('x', 'y', source=source,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Divorce rate)", "@rate%"),
    ("(Long, Lat)", "($x, $y)"),
]

show(p)