from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import requests
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from GoogleNews import GoogleNews
from newsapi import NewsApiClient
from Currency.models import NewsModel
import datetime as dt

googlenews = GoogleNews()
def changePrice(oldPrice,newPrice):
    if oldPrice!=newPrice:
        return True
    return False

apiKey = "d8e177aeb567448ca15f9415d0635bbe"

@login_required
def converter(request):
    if request.method=="POST":
        crypto = request.POST["crypto"]
        country = request.POST["country"]
        cryptoValue = float(request.POST["cryptoValue"])
        countryValue = float(request.POST["countryValue"])
        if cryptoValue <= 0:
            cryptoValue=1
        if countryValue <= 0:
            countryValue =1
        ansForCrypto = changePrice(cryptoValue,request.session["currencyvalue"])
        ansForCountry = changePrice(countryValue,request.session["countryvalue"])
        request.session["currency"] = crypto 
        request.session["country"] = country
        path =  f"https://api.coingecko.com/api/v3/coins/{crypto}"
        res = requests.get(path).json()
        value = res["market_data"]["current_price"][country]
        btcprice = 0
        conprice = 0
        if ansForCrypto:
            btcprice = cryptoValue
            conprice = cryptoValue * countryValue
        elif ansForCountry:
             btcprice = cryptoValue / countryValue
             conprice = cryptoValue
        else:
            btcprice = cryptoValue
            conprice = value * btcprice 
        request.session["currencyvalue"] = btcprice
        request.session["countryvalue"] =conprice
        return redirect('currency converter')
    if not "currency" in request.session.keys():
        #user visiting this page for first time
        path =  f"https://api.coingecko.com/api/v3/coins/bitcoin"
        res = requests.get(path).json()
        value = res["market_data"]["current_price"]["inr"]
        request.session["currency"] = "bitcoin"
        request.session["currencyvalue"] = 1
        request.session["country"] = "inr"
        request.session["countryvalue"] = value
    else:
        #user visiting the page second time or another time
        value = request.session['currency']
        path =  f"https://api.coingecko.com/api/v3/coins/{value}"
        res = requests.get(path).json()
        country =request.session["country"]
        val = res["market_data"]["current_price"][country]
        #return HttpResponse(res)
        request.session["countryvalue"] = request.session["currencyvalue"] * val
    return render(request,"currency/main.html")

def printSession(request):
    if request.session["country"] == "rbl":
        request.session["country"] = "rub"
    return HttpResponse(request.session["country"])

@login_required
def getNews(request):
    news = NewsApiClient(api_key=apiKey)
    data = news.get_everything(q="crypto currency",language="en",page_size=20)
    context={}
    news = []
    for i in range(15):
        title = data["articles"][i]["title"]
        image = data["articles"][i]["urlToImage"]
        desc = data["articles"][i]["description"]
        media = data["articles"][i]["source"]["name"]
        link = data["articles"][i]["url"]
        date = data["articles"][i]["publishedAt"]
        n1 = NewsModel(title,image,desc,media,link,date)
        news.append(n1)
    context["data"] = news
    return render(request,"Currency/news.html",context)

@login_required
def currencyNews(request,currency):
    news = NewsApiClient(api_key=apiKey)
    data = news.get_everything(q=currency,language="en",page_size=20)
    context={}
    news = []
    for i in range(15):
        title = data["articles"][i]["title"]
        image = data["articles"][i]["urlToImage"]
        desc = data["articles"][i]["description"]
        media = data["articles"][i]["source"]["name"]
        link = data["articles"][i]["url"]
        date = data["articles"][i]["publishedAt"]
        n1 = NewsModel(title,image,desc,media,link,date)
        news.append(n1)
    context["data"] = news
    context["currency"]= currency.title()
    return render(request,"Currency/coinnews.html",context)
    

def demo():
    context={"currency":"s"}
    googlenews = GoogleNews(lang='en')
    googlenews.search("s")
    result = googlenews.page_at(1)
    #return HttpResponse(result)
    result2 =  googlenews.page_at(2)
    news = []
    for i in result:
        title = i["title"]
        image = i["img"]
        desc = i["desc"]
        media = i["media"]
        link = i["link"]
        date = i["date"]
        n1 = NewsModel(title,image,desc,media,link,date)
        news.append(n1)
    for i in result2:
        title = i["title"]
        image = i["img"]
        desc = i["desc"]
        media = i["media"]
        link = i["link"]
        date = i["date"]
        n1 = NewsModel(title,image,desc,media,link,date)
        news.append(n1)
    context["data"] = news
    return render(request,"Currency/coinnews.html",context)