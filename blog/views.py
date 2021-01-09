from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
import requests, json
from re import search
# Create your views here.
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd
from math import pi
import datetime
from .utils import get_data, convert_to_df


def home(request):
#	context= {
#	'posts': Post.objects.all()
#	}
#	return render(request, 'blog/home.html', context)

 #We use get_data method from utils

    result = get_data('EUR', 'USD', '9PRDFA9QWXCAP88V')  # Add your own APIKEY

    source = convert_to_df(result)

    # These lines are there to color
    # the red and green bars for down and up days

    increasing = source.close > source.open
    decreasing = source.open > source.close
    w = 12 * 60 * 60 * 1000
    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

    title = 'EUR to USD chart'

    p = figure(x_axis_type="datetime", tools=TOOLS,
               plot_width=700, plot_height=500, title=title)
    p.xaxis.major_label_orientation = pi / 4

    p.grid.grid_line_alpha = 0.3

    p.segment(source.date, source.high, source.date, source.low, color="black")

    p.vbar(source.date[increasing], w, source.open[increasing], source.close[increasing],
           fill_color="#D5E1DD", line_color="black"
           )
    p.vbar(source.date[decreasing], w, source.open[decreasing], source.close[decreasing],
           fill_color="#F2583E", line_color="black"
           )

    script, div = components(p)

    return render(request, 'blog/home.html', {'script': script, 'div': div})




def about(request):
    return render(request, 'blog/about.html',  {'title': 'About'})


def market(request):
    api_request = requests.get(
    	" https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_7b2bd309b9284f9488c22c6b82727561&symbols=aapl ")
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error, data not loading"

    return render(request, 'blog/market.html', {'api': api})


def news(request):
    api_request = requests.get(
    	" https://newsapi.org/v2/everything?q=bitcoin&apiKey=48fb97dc883e4aa381fc20051e5a63f3 ")
    try:
        api_news = json.loads(api_request.content)
    except Exception as e:
        api_news = "Error, data not loading"

    data = api_request.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }

    # seprating the necessary data
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "publishedat": i["publishedAt"]
        })

    return render(request, 'blog/news.html', context=context)
