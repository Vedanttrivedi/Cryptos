from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests
from . models import Currency
import pandas_datareader as web
import datetime as dt
from .utils import get_plot,anylysePlot
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
# Create your views here.

def home(request):
    start = dt.datetime(2020,3,4)
    end = dt.datetime.now()
    data = web.DataReader("BTC-USD","yahoo",start,end)
    indexes = data.tail(7).index
    
    x_date = indexes
    y_price = data.tail(7)["Close"]
    chart = get_plot(x_date,y_price,"bitcoin")
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
    context["chart"] = chart
    context["name"] = "bitcoin"
    context["about"] = about[:250]
    context["image"] = image
    context["hash_algo"] = hash_alog
    context["market_rank"] = market_rank
    context["high_price"] = high_price
    context["low_price"] = low_price
    context["first"] = current_price
    context["current_price"] = current_price
    context["predict_price"] = 000000
    context["second"] = eth_price
    context["third"] = ltc_price
    c1 = Currency.objects.get(currency_name="bitcoin")
    c1.currency_highprice = high_price
    c1.currency_lowprice = low_price
    c1.prediction_price = 000000
    c1.currency_icon = image
    c1.save()
    return render(request,"user/base.html",context)

@login_required
def oneCoin(request,coin):
    if coin=="bitcoin":
        return redirect(request,'/')
    path=f"https://api.coingecko.com/api/v3/coins/{coin}"
    res = requests.get(path).json()
    about = res["description"]["en"]
    hash_alog = res["hashing_algorithm"]
    image = res["image"]["large"]
    market_rank = res["market_cap_rank"]
    current_price = res["market_data"]["current_price"]["usd"]
    high_price = res["market_data"]["high_24h"]["usd"]
    low_price = res["market_data"]["low_24h"]["usd"]
    start = dt.datetime(2020,3,4)
    end = dt.datetime.now()
    ticker = ""
    if coin=="ethereum":
        ticker = "ETH"
    if coin=="litecoin":
        ticker = "LTC"
    data = web.DataReader(f"{ticker}-USD","yahoo",start,end)
    indexes = data.tail(7).index
    
    x_date = indexes
    y_price = data.tail(7)["Close"]
    chart = get_plot(x_date,y_price,coin)
    context = {}
    context["name"] = coin
    context["chart"] = chart
    context["about"] = about[:200]
    context["image"] = image
    context["hash_algo"] = hash_alog
    context["market_rank"] = market_rank
    context["high_price"] = high_price
    context["low_price"] = low_price
    context["current_price"] = current_price
    context["predict_price"] = 000000
    c1 = Currency.objects.get(currency_name=coin)
    c1.currency_highprice = high_price
    c1.currency_lowprice = low_price
    c1.prediction_price = 000000
    c1.currency_icon = image
    c1.save()
    if coin == "ethereum":
        path=f"https://api.coingecko.com/api/v3/coins/litecoin"
        res = requests.get(path).json()
        ltc_price= res["market_data"]["current_price"]["usd"]
        path=f"https://api.coingecko.com/api/v3/coins/bitcoin"
        res = requests.get(path).json()
        btc_price= res["market_data"]["current_price"]["usd"]
        context["first"] = btc_price
        context["third"] = ltc_price
        context["second"] = current_price
        
    if coin=="litecoin":
        path=f"https://api.coingecko.com/api/v3/coins/ethereum"
        res = requests.get(path).json()
        eth_price= res["market_data"]["current_price"]["usd"]
        path=f"https://api.coingecko.com/api/v3/coins/bitcoin"
        res = requests.get(path).json()
        btc_price= res["market_data"]["current_price"]["usd"]
        context["first"] = btc_price
        context["second"] = eth_price
        context["third"] = current_price

    return render(request,"user/base.html",context)


def modelPredict(request):
    start = dt.datetime(2016,1,1)
    end = dt.datetime.now()
    df = pdr.DataReader("BTC-USD","yahoo",start,end)
    scalr = MinMaxScaler(feature_range=(0,1))
    scal_data = scalr.fit_transform(data["Close"].values.reshape(-1,1))
    prediction_days = 7
    x_tr,y_tr = [],[]
    for x in range(prediction_days,len(scal_data)):
        x_tr.append(scal_data[x-prediction_days:x,0])
        y_tr.append(scal_data[x,0])

    x_tr,y_tr = np.array(x_tr),np.array(y_tr)
    x_tr = np.reshape(x_tr,(x_tr.shape[0],x_tr.shape[1],1))
    model  = Sequential()
    model.add(LSTM(units=50,return_sequences=True,input_shape=(x_tr.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50,return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer="adam",loss="mean_squared_error")
    model.fit(x_tr,y_tr,epochs=25,batch_size=32)
    test_start = dt.datetime(2020,1,1)
    test_end = dt.datetime.now()
    test_data = web.DataReader("BTC-USD","yahoo",test_start,test_end)
    actual_price = test_data["Close"].values
    total_dataset = pd.concat((data["Close"],test_data["Close"]),axis=0)
    model_inputs = total_dataset[len(total_dataset)-len(test_data)-prediction_days]
    model_inputs = model_inputs.reshape(-1,1)
    model_inputs = scalr.fit_transform(model_inputs)

    x_test = []
    for x in range(prediction_days,len(model_inputs)):
        x_test.append(model_inputs[x-prediction_days:x,0])
    
    x_test = np.array(x_test)
    x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
    predict_prices = model.predict(x_test)
    predict_prices = scalr.inverse_transform(predict_prices)
    plt.plot(actual_price,color="black",label="actual prices")
    plt.plot(predict_price,color="green",label="Prediction Prices")
    plt.legend("upper left")
    plt.show()

    real_data = [model_inputs[len(model_inputs)+1 - prediction_days:len(model_inputs)+1,0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data,(real_data.shape[0],real_data.reshape[1],1))
    prediction = model.predict(real_data)
    prediction = scalr.inverse_transform(prediction)
    print(prediction)
    return HttpResponse(prediction)



def anylyse(request):
    graph = anylysePlot()
    context = {}
    context["chart"] = graph
    return render(request,"user/anylyse.html",context)

def analysisCoin(request,coin):
    n = []
    if coin=="bitcoin":
        n.append("BTC")
        n.append("Bitcoin")
    elif coin=="litecoin":
        n.append("LTC")
        n.append("Litecoin")
    elif coin=="ethereum":
        n.append("ETH")
        n.append("Ethereum")
    graph = anylysePlot(n)
    context = {}
    context["chart"] = graph
    context["name"] = coin
    return render(request,"user/anylyseCoin.html",context)

