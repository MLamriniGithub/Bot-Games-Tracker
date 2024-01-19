"""
Main.py

The main script
Goal : 

The goal of this code is to retrieve information about a player's recent game history from the op.gg API,
analyze the data, and send a notification with a summary of the player's gaming activity for the current day.
"""

import requests

import time



# Get informations on the date

import datetime

import pytz



from send_notification import send_notification



def make_request():

    cookies = {

        '__hist': '%5B%7B%22region%22%3A%22euw%22%2C%22summonerName%22%3A%22lejpex%22%7D%5D',

    }



    headers = {

        'authority': 'op.gg',

        'accept': 'application/json, text/plain, */*',

        'accept-language': 'fr-FR,fr;q=0.8',

        # 'cookie': '__hist=%5B%7B%22region%22%3A%22euw%22%2C%22summonerName%22%3A%22lejpex%22%7D%5D',

        'if-none-match': 'W/"6165a-573zG68S0TjK81027yrnIj9Bvbs"',

        'origin': 'https://www.op.gg',

        'referer': 'https://www.op.gg/',

        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',

        'sec-ch-ua-mobile': '?0',

        'sec-ch-ua-platform': '"Windows"',

        'sec-fetch-dest': 'empty',

        'sec-fetch-mode': 'cors',

        'sec-fetch-site': 'same-site',

        'sec-gpc': '1',

        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',

    }



    response = requests.get(

        'https://op.gg/api/v1.0/internal/bypass/games/euw/summoners/GmTrq6mXRllaS-kiNYYMLBnICNsDxr7Q4Z_ifm8cIl6NeqIwji8iw96Ajg?&limit=20&hl=fr_FR&game_type=total',

        cookies=cookies,

        headers=headers,

    )



    return response.json()



def is_today(date):

    # Convert the time into a datetime object

    date_heure = datetime.datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S")



    # Subtract 7 hours from the given time

    date_heure_france = date_heure - datetime.timedelta(hours=7)



    # Get the current date and time in France

    maintenant_france = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)



    # Check if the date corresponds to the current date

    if date_heure_france.date() == maintenant_france.date():

        return True



    return False



def get_time_lost(seconds):

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    seconds = (seconds % 3600) % 60

    str = ""

    if hours > 0:

        str += f"{hours} hour(s) "

    if minutes > 0:

        str += f"{minutes} minute(s) "

    if seconds > 0:

        str += f"{seconds} secondes..."



    return str



def poucave():

    historic = make_request()

    day_time = 0

    day_lp = 0

    for game in historic['data']:

        if is_today(game['created_at']):

            # print(game)

            day_time += game["game_length_second"]

            try:

                day_lp += game['myData']["tier_info"]['lp']

            except:

                day_lp = day_lp

        else:

            break

    if day_lp > 0:

        lp_text = "win " + str(day_lp) + " lps..."

    elif day_lp < 0:

        lp_text = "lost " + str(day_lp) + " lps..."

    else:

        lp_text = ""

    text = "Results\n⌚: " + get_time_lost(day_time) + "\n" + lp_text

    print(text)

    send_notification(text)



def main():

    historic = make_request()

    print(historic['data'][0]['created_at'])

    while True:

        time.sleep(10)

        try:

            new_historic = make_request()

        except Exception as e:

            new_historic = historic

        print(new_historic['data'][0]['created_at'])

        # if 1 != 2:

        if new_historic['data'][0]['created_at'] != historic['data'][0]['created_at']:

            historic = new_historic

            day_time = 0

            day_lp = 0

            for game in historic['data']:

                if is_today(game['created_at']):

                    day_time += game["game_length_second"]

                    try:

                        day_lp += game['myData']["tier_info"]['lp']

                    except:

                        day_lp = day_lp

                else:

                    break

            if day_lp > 0:

                lp_text = "win " + str(day_lp) + " lps..."

            elif day_lp < 0:

                lp_text = "lost" + str(day_lp) + " lps..."

            else:

                lp_text = ""

            text = "New game \n⌚Total time for today : " + get_time_lost(day_time) + "\n" + lp_text

            print(text)

            send_notification(text)

        # time.sleep(10)



if __name__ == "__main__":

    # print(is_today("2023-06-23T08:15:50+09:00"))

    # main()

    poucave()