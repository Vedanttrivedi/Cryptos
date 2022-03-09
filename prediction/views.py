from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests
# Create your views here.

def home(request):
    path=f"https://api.coingecko.com/api/v3/coins/bitcoin"
    res = requests.get(path).json()
    about = res["description"]["en"]
    hash_alog = res["hashing_algorithm"]
    image = res["image"]["large"]
    market_rank = res["market_cap_rank"]
    current_price = res["market_data"]["current_price"]["usd"]
    high_price = res["market_data"]["high_24h"]["usd"]
    low_price = res["market_data"]["low_24h"]["usd"]
    path=f"https://api.coingecko.com/api/v3/coins/litecoin"
    res = requests.get(path).json()
    ltc_price= res["market_data"]["current_price"]["usd"]
    path=f"https://api.coingecko.com/api/v3/coins/ethereum"
    res = requests.get(path).json()
    eth_price= res["market_data"]["current_price"]["usd"]
    context = {}
    context["name"] = "bitcoin"
    context["about"] = about[:250]
    context["image"] = image
    context["hash_algo"] = hash_alog
    context["market_rank"] = market_rank
    context["high_price"] = high_price
    context["low_price"] = low_price
    context["current_price"] = current_price
    context["predict_price"] = 000000
    context["eth"] = eth_price
    context["ltc"] = ltc_price
    return render(request,"user/base.html",context)

@login_required
def oneCoin(request,coin):
    path=f"https://api.coingecko.com/api/v3/coins/{coin}"
    res = requests.get(path).json()
    about = res["description"]["en"]
    hash_alog = res["hashing_algorithm"]
    image = res["image"]["large"]
    market_rank = res["market_cap_rank"]
    current_price = res["market_data"]["current_price"]["usd"]
    high_price = res["market_data"]["high_24h"]["usd"]
    low_price = res["market_data"]["low_24h"]["usd"]
    context = {}
    context["name"] = coin
    context["about"] = about[:200]
    context["image"] = image
    context["hash_algo"] = hash_alog
    context["market_rank"] = market_rank
    context["high_price"] = high_price
    context["low_price"] = low_price
    context["current_price"] = current_price
    context["predict_price"] = 000000
    if coin=="bitcoin":
        return redirect(request,'/')
    if coin == "ethereum":
        path=f"https://api.coingecko.com/api/v3/coins/litecoin"
        res = requests.get(path).json()
        ltc_price= res["market_data"]["current_price"]["usd"]
        path=f"https://api.coingecko.com/api/v3/coins/bitcoin"
        res = requests.get(path).json()
        eth_price= res["market_data"]["current_price"]["usd"]
        context["current_price"] = eth_price
        context["ltc"] = ltc_price
        context["eth"] = current_price
    if coin=="litecoin":
        path=f"https://api.coingecko.com/api/v3/coins/litecoin"
        res = requests.get(path).json()
        ltc_price= res["market_data"]["current_price"]["usd"]
        path=f"https://api.coingecko.com/api/v3/coins/bitcoin"
        res = requests.get(path).json()
        eth_price= res["market_data"]["current_price"]["usd"]
        context["current_price"] = eth_price
        context["eth"] = ltc_price
        context["ltc"] = current_price

    return render(request,"user/base.html",context)



    