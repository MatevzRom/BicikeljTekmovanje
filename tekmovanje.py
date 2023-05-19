import numpy as np
import pandas as pd
from typing import Optional, Tuple, Dict, List
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def convert_data_into_input(train,pastKolesa, trenutniTimes, postaja):
    # trainTimesValues = trainTimes.values
    trainTimes = train["timestamp"]
    
    

    numberOfData = trenutniTimes.size
    # prepare data: timestamps to variables
    # year:usles k je zmer isto leto
    # month: 8.9.10
    # day: 1,2,3,4,5,6,7
    day = np.zeros([numberOfData,7])
    month = np.zeros([numberOfData,3])
    sinXcos = np.zeros([numberOfData,2])
    pastH = np.zeros([numberOfData,1])
    pastPol = np.zeros([numberOfData,1])
    aproxRightNow = np.zeros([numberOfData, 1])

    for i, date in enumerate(trenutniTimes):
        closest = np.argmin(np.abs(trainTimes - date))
        pastH[i] = pastKolesa[f"{postaja}:1h"][closest]
        pastPol[i] = pastKolesa[f"{postaja}:30min"][closest]
        aproxRightNow[i] = train[postaja][closest] 
        # print(pastH)
        # print(pastPol)
        # print(closest)
        # print(pastKolesa[f"{postaja}:1h"][closest])
    # print(pastH)
    # print(pastPol)
    # raise("omg")
        


    


    # dodaj: st koles v pretekli urei/preteklih dveh urah

    for i, date in enumerate(trenutniTimes):
        mesc = date.month
        match mesc:
            case 8:
                month[i,0] = 1
            case 9:
                month[i,1] = 1
            case 10:
                month[i,2] = 1
            case _:
                raise("BIG ERROR, NEZNAN MESC")
            
        dan = date.weekday()
        day[i,dan] = 1

        ura = date.hour
        minute = date.minute
        uraZdruzen = ura + minute/60
        sinXcos[i,0] = np.sin(2*np.pi*uraZdruzen/24)
        sinXcos[i,1] = np.cos(2*np.pi*uraZdruzen/24)
   
    
        
    
    # X = np.concatenate((month, day, sinXcos, pastH, pastPol), axis=1)
    X = np.concatenate((aproxRightNow ,pastH, pastPol,sinXcos,month,day), axis=1)

    # X = np.concatenate((month, day, sinXcos, predEnoUro, predPolUre), axis=1)
    return X

def createPastBikes(array,train):
    numberOfData = array.size
    # print("huhu")
    # print(len(train.keys()))
    # print(train.keys())
    # raise("konc")
    predEnoUro = np.zeros([numberOfData])
    predPolUre = np.zeros([numberOfData])
    result = pd.DataFrame()
    # result.columns = ["pred eno uro(-12)", "pred pol ure (-6)"]
    # print(result)
    # raise("okok")
   

    for i, key in enumerate(train):
        if key == "timestamp":
            continue
        for j in range(numberOfData):
            predEnoUro[j] = list(train[key])[j-12]
            predPolUre[j] = list(train[key])[j-6]
            # print(predEnoUro)
            # print(predPolUre)
            
            # print(X[0])
            # print("HIHIHI")
            # raise("stop")
            # if(j == 3):
            #     break
        mojStringUro = f"{key}:1h"
        mojStringPolUre = f"{key}:30min"

        result[mojStringUro] = predEnoUro
        result[mojStringPolUre] = predPolUre
        # if(i ==2):
        #     break
            
        
    
    result.to_csv("pastShitTest.csv", sep=",", index=False)


if __name__ == "__main__":
    train = pd.read_csv("bicikelj_train.csv")
    train["timestamp"] = [pd.to_datetime(ts).tz_localize(None) for ts in train["timestamp"].values]

    test = pd.read_csv("bicikelj_test.csv")
    test["timestamp"] = [pd.to_datetime(ts).tz_localize(None) for ts in test["timestamp"].values]

    # print(test["timestamp"])

    pastKolesa = pd.read_csv("pastShit.csv")

    times = train["timestamp"].values
    ptimes = test["timestamp"].values
    # print(train["timestamp"][0])

    # for i, t in enumerate(ptimes):
    #     closest = np.argmin(np.abs(times - t))
    #     test.iloc[i, 1:] = train.iloc[closest, 1:]

    # test.to_csv("closest_time.csv", sep=",", index=False)


    # print(type(test))
    # print(test.iloc[0:,1])

    # podatki to nparray:
    year = train["timestamp"].dt.year
    month = train["timestamp"].dt.month
    hour = train["timestamp"].dt.hour
    minutes = train["timestamp"].dt.minute
    # print(type(train["timestamp"]))
    # print(year.dt.hour)
    # print("lolo")

    
    # print(X[0])

    

    # print(X[0])
    # print(month[0])
    # print(day[0])
    # print(sinXcos[0])
    print("month0")
    testMoj = np.array(test)
    # print(testMoj[0])
    mojDataResult = pd.DataFrame()
    mojDataResult["timestamp"] = test["timestamp"]
    # print(len(mojDataResult["timestamp"]))
    # raise("fucking deli")

    prvikey = ""
    for i, key in enumerate(test):
        if key == "timestamp":
            continue
        prvikey = key
        # print(test["timestamp"])
        # raise("test")
        X = convert_data_into_input(train, pastKolesa,train["timestamp"],key)
       
        min = 0
        max = 27
        y = np.array(train[key])
        # print(y)
        
        # key je postaja, za vsako treba zgradit podel
        lr = LinearRegression()
        poly = PolynomialFeatures(2)
        Xtest = convert_data_into_input(train, pastKolesa,test["timestamp"],key)

        # pastHour = np.array(pastKolesa[f"{key}:1h:{i}"])
        # pastHalfHour = np.array(pastKolesa[f"{key}:30min:{i}"])
        # print(pastHour)
        # print("UPSI")
        # raise("moj")
        # delovniX = np.concatenate((X,pastHour,pastHalfHour), axis=1)
        delovniX = X 
        vmes = poly.fit_transform(delovniX)
        
        napovednik = lr.fit(vmes,y)

        
        
        # for j, t in enumerate(ptimes):
        #     closest = np.argmin(np.abs(times - t))
        # TOLE ZDELE DELAM, ZRIHTI KAK DOBIT PODATKE VREDI!!!!!!!!!!!!!!!!!!





        # 
        Xtest = poly.fit_transform(Xtest)
        
        result = napovednik.predict(X=Xtest)
        for i in range(len(result)):
            if(result[i] <0 ):
                result[i]=0
            if(result[i] > 26):
                result[i] = 26
        result = result.round(0)
        print(result)
        # print(result.size)
        # if(i==5):
        #     # print(X)
        #     # print(Xtest)
        #     # print(result)
        #     raise("ok")
        # print(len(result))
        # print(len(test.iloc[i, 1:]))
        # print("ahh")
        # test.iloc[0:,i] = result
        mojDataResult[key] = result

        # print(test.iloc[0:,i])
        
        # print(np.array(test["timestamp"]))
    mojDataResult.to_csv("Poly_plus_past_bikes_+_round.csv", sep=",", index=False)
    # createPastBikes(train["timestamp"],train)
    # createPastBikes(test["timestamp"],test)

    
    # print(napovednik)
    # print(prvikey)
    # print(np.array(test[prvikey]))
    # print(np.array(test[prvikey]))

    print("HELLO")