import  matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    image=buffer.getvalue()
    graph = base64.b64encode(image)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y,name):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title(f"Last 7 Days Closing Price($) of {name}")
    plt.plot(x,y,color="orange")
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Price (In $)")
    plt.tight_layout()
    graph = get_graph()
    return graph



def anylysePlot(name=[]):
    if len(name)==0:
        currency="USD"
        metric="Close"
        start = dt.datetime(2018,1,1)
        end = dt.datetime.now()

        crypto = ["BTC","ETH","LTC"]
        colnames = []
        first = True
        combined = ""
        for ticker in crypto:
            data = web.DataReader(f"{ticker}-{currency}","yahoo",start,end)
            if first:
                combined = data[[metric]].copy()
                colnames.append(ticker)
                combined.columns = colnames
                first=False
            else:
                combined = combined.join(data[metric])
                colnames.append(ticker)
                combined.columns = colnames

        plt.switch_backend('AGG')
        plt.figure(figsize=(10,5))
        plt.title(f"Analysis of Top 3 Crypto Currency")
        plt.plot(combined["BTC"],color="orange",label="Bitcoin")
        plt.plot(combined["ETH"],color="blue",label="Ethereum")
        plt.plot(combined["LTC"],color="red",label="Litecoin")
        plt.xkcd()
        plt.grid()
        
        plt.legend(["Orange BTC","Blue ETH","Red LTC"])
        plt.xlabel("Dates In 6 Months Gap")
        plt.ylabel("Price In $")
        plt.tight_layout()
        plt.yscale("log")
        graph = get_graph()
        return graph
    else:
        currency="USD"
        metric="Close"
        start = dt.datetime(2016,1,1)
        end = dt.datetime.now()
        data = web.DataReader(f"{name[0]}-{currency}","yahoo",start,end)
        plt.switch_backend('AGG')
        plt.title(f"Analysis Of {name[1]} in Years")
        plt.figure(figsize=(10,5))
        plt.plot(data[metric],color="orange")
        plt.xkcd()
        plt.xlabel("Year")
        plt.ylabel("Price In $")
        plt.tight_layout()
        graph = get_graph()
        return graph
        
