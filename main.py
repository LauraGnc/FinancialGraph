'''This is the bokeh script to generate data from stock market.
Change the variables start and end to change the dates.
Below, the df variable can be modified if you want to see the stock for another
company and from another source.'''


from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file

start = datetime.datetime(2015, 11, 1)
end = datetime.datetime(2016, 3, 10)
df = data.DataReader(name='GOOG', data_source='yahoo', start=start, end=end)

date_increase = df.index[df.Close > df.Open]
date_decrease = df.index[df.Close < df.Open]

def inc_dec(c, o):
    if c > o:
        value = "Increase"
    elif c < o:
        value = "Decrease"
    else:
        value = "Equal"
    return value

df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
df["Middle"] = (df.Open + df.Close) / 2
df["Height"] = abs(df.Close - df.Open)

p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
p.title.text = ". ' . Candlestick . ' ."
p.title.align = "center"
p.title.text_font_size = "24px"

p.grid.grid_line_alpha = 0.5

hours12 = 12*60*60*1000

p.segment(df.index, df.High, df.index, df.Low, color="black")

p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status == "Increase"], hours12,
       df.Height[df.Status == "Increase"], fill_color="pink", line_color="red")

p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], hours12,
       df.Height[df.Status == "Decrease"], fill_color="orange", line_color="red")

output = "CS.html"
show(p)