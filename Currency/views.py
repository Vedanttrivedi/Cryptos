from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import requests
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from GoogleNews import GoogleNews

from Currency.models import NewsModel
googlenews = GoogleNews()
def changePrice(oldPrice,newPrice):
    if oldPrice!=newPrice:
        return True
    return False

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


def getNews(request):
    return render(request,"Currency/news.html")

def currencyNews(request,currency):
    context = {"currency":currency}
    '''url = f"https://www.google.com/search?q={currency}+news&sxsrf=AOaemvKr6Q3iI_tmk07JEuvNU98R69Y-rg:1642914161562&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiF5vuXjMf1AhVVc3AKHVXECF0Q_AUoAXoECAEQAw&biw=1455&bih=717&dpr=1.1"
    path = requests.get(url)
    soup  = BeautifulSoup(path.text,"lxml")
    context["newscode"] = soup'''
    googlenews = GoogleNews(lang='en')
    googlenews.search('Bitcoin')
    result = googlenews.page_at(1)
    
    #result2 =  googlenews.page_at(2)
    news = []
    for i in result:
        title = i["title"]
        image = i["img"]
        desc = i["desc"]
        media = i["media"]
        link = i["link"]
        n1 = NewsModel(title,image,desc,media,link)
        news.append(n1)
    context["data"] = news
    return render(request,"Currency/coinnews.html",context)