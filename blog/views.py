from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json
from re import search
# Create your views here.


def home(request):
#	context= {
#   'posts': Post.objects.all()
#	}
#	return render(request, 'blog/home.html', context)

 

	if request.method == 'POST':
		ticker = request.POST['ticker']
		# pass in url that calls the api
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" +
								   ticker + "/quote?token=pk_7b2bd309b9284f9488c22c6b82727561&symbols=" + ticker)

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'blog/home.html', {'api': api,
			'error': "Could not access the api"})

	else:
	
		return render(request, 'blog/home.html', {'ticker': "Enter a Ticker Symbol Above..."})


def add_stock(request):

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added to your portfolio!"))
			return redirect('blog-add_stock')

	else:
		ticker = Stock.objects.all()
		# save ticker info from api output into python list ('output list')
		output = []
		# modify to pull multiple stock tickers at the same time
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(
				ticker_item) + "/quote?token=pk_7b2bd309b9284f9488c22c6b82727561")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'blog/add_stock.html', {'ticker': ticker, 'output':  output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)  # call database by primary key for id #
	item.delete()
	messages.success(request, ("Stock Has Been Deleted From Portfolio!"))
	return redirect(add_stock)


def about(request):
	if request.method == 'POST':
		ticker = request.POST['ticker']
		# pass in url that calls the api
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" +
                             ticker + "/quote?token=pk_7b2bd309b9284f9488c22c6b82727561&symbols=" + ticker)

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'blog/about.html', {'api': api,
                                            'error': "Could not access the api"})

	else:

		return render(request, 'blog/about.html', {'ticker': "Enter a Ticker Symbol Above..."})


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
