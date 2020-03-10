import requests
import urllib.request
import io
import os.path
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
import pandas as pd
from covid_nl import update_data


def main():    
    while True:
        url = 'https://www.volksgezondheidenzorg.info/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19'
        rivm_update_time = "2:00PM"
        today = datetime.now().strftime('%d%m%Y')
        csv_local = f"input_data/klik_corona{today}.csv"
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