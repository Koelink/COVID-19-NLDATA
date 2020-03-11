import requests
import urllib.request
import io
import os.path
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
import pandas as pd
from covid_nl import update_data


def latest_rivm_file(today, function):
    script_dir = os.path.dirname(__file__) + "/"
    file = script_dir + "latest_rivm_file.json"
    if function == "open":
        with open(file) as json_file:
            data = json.load(json_file)
            try:
                latest = data[today]
                return latest
            except:
                return -1
    else:
        with open(file) as json_file:
            data = json.load(json_file)
            data[today] = function
            with open(file, 'w') as outfile:
                json.dump(data, outfile)


def main(cronjob = True):    
    script_dir = os.path.dirname(__file__) + "/"
    if cronjob == True:
        today = datetime.now().strftime('%d%m%Y')
        csv_url = "https://www.volksgezondheidenzorg.info/sites/default/files/map/detail_data/klik_corona"
        today = datetime.now().strftime('%d%m%Y')
        csv_local = f"{script_dir}input_data/klik_corona{today}.csv"
        x = False
        range_end = latest_rivm_file(today, "open")
        for i in range(5, range_end, -1):
            print(i)
            try:
                s = requests.get(f"{csv_url}{today}_{i}.csv", timeout=5).content
                df = pd.read_csv(io.StringIO(s.decode('utf-8')), delimiter=";") 
                x = True
                break
            except Exception as e:
                print(i, e)
                sleep(3)   # Sleeps for 3 seconds to give the server some rest
        if x == False and range_end == -1:
            try:
                s = requests.get(f"{csv_url}{today}.csv", timeout=5).content
                df = pd.read_csv(io.StringIO(s.decode('utf-8')), delimiter=";") 
                i = -2
                x = True
            except Exception as e:
                print(i, e)
        if x == True:
            df["Aantal"].fillna(0, inplace=True)
            df["Aantal"] = df["Aantal"].astype(int)
            df.to_csv(csv_local, index=False, sep=";")
            update_data()
            latest_rivm_file(today, i)
            print(f"data updated for {today}")
            print("File used:", i)
        else:
            print("No new file")
        sleep(10)


    else:
        while True:
            url = 'https://www.volksgezondheidenzorg.info/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19'
            rivm_update_time = "2:00PM"
            today = datetime.now().strftime('%d%m%Y')
            script_dir = os.path.dirname(__file__) + "/"
            csv_local = f"{script_dir}input_data/klik_corona{today}.csv"
            print(csv_local)
            rivm_update_time = datetime.strptime(today + rivm_update_time, "%d%m%Y%I:%M%p")

            if rivm_update_time < datetime.now():  #Checks if it's after the update time
                if not os.path.isfile(csv_local):   #Checks if there is a local csv file for today
                    try:      
                        res = urllib.request.urlopen(url)
                        soup = BeautifulSoup(res.read(), features="lxml")
                        csv_file = soup.find_all('a', {'class': 'csv-export'})[0]['href'] #gets latest file from url
                        csv_date = csv_file.split("klik_corona")[-1][:8]
                    except Exception as e:
                        print(datetime.now(), e)
                        sleep(60) 
                        continue

                    if csv_date == today:      # check if latest file is from today
                        try:
                            csv_url = url.split("/onderwerp")[0] + csv_file
                            s = requests.get(csv_url).content
                            df = pd.read_csv(io.StringIO(s.decode('utf-8')), delimiter=";")     # makes a df from latest csv file
                            df.to_csv(csv_local, index=False, sep=";")
                            update_data()
                            print(f"data updated for {today}")
                            print("File used:", csv_file)
                            #TODO update to github ect

                        except Exception as e:
                            print(datetime.now(), e)
                            sleep(60) 
                            continue
                    else:
                        print(datetime.now(), ": No file on RIVM site for today, checks in 5 min")
                        sleep(300)      # Sleeps for 5 min to check again if there is a new csv file
                else:
                    rivm_tomorrow_update = rivm_update_time + timedelta(days=1)
                    time_to_wait = (rivm_tomorrow_update - datetime.now()).seconds
                    print(f"sleeps till {rivm_tomorrow_update}, {time_to_wait} seconds")
                    sleep(time_to_wait)

            else:
                time_to_wait = (rivm_update_time - datetime.now()).seconds
                print(f"sleeps till {rivm_update_time}, {time_to_wait} seconds")
                sleep(time_to_wait)
            
        
if __name__ == "__main__":
    main()