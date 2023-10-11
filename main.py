from datetime import time
import datetime
from fastapi import FastAPI
from time import sleep
import requests
import json

# checke jede 5 mins https://api.hitbtc.com/#trades auf
# width>1.5 und volume >120 und trades >200 in den letzten 15 minuten


app = FastAPI()
url = "https://api.hitbtc.com/api/3/public/trades"
r = requests.get(url).content
j = json.loads(r)
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    while True:
        for i in j:
            a = j[i]
            tradecounter = 0
            for m in a:
                t = m['timestamp']
                time.strptime(t)
                print(t)
                tradecounter = tradecounter + 1
            print(i + "\ttrades:" + str(tradecounter))
        sleep(5)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


