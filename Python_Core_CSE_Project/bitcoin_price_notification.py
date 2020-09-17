import requests
import time
from datetime import datetime
BITCOIN_PRICE_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'

# "https://api.coindesk.com/v1/bpi/currentprice.json" From this URL we will fecth the json data that includes bitcoin price

class Bitcoin() :
    def __init__(self) :
        pass
    def taking_latest_bitcoin_prices(self) :

        # we use requests library to fecth bitcoin price
        #In this fuction we will return bitcoin price to the calling function as floating value

        response = requests.get(BITCOIN_PRICE_URL)
        response_json = response.json()
        BITCOIN_PRICE = response_json["bpi"]['USD']['rate']
        BITCOIN_PRICE = BITCOIN_PRICE.replace(",", "")
        return float(BITCOIN_PRICE)

    def send_notification_to_IFTTT_app(self, event, value) :

        # In this function we use IFTTT web hook url for sending notifications to IFTTT app if the bitcoin price falls below threshold value

        data = {'value1' : value}
        IFTTT_url_for_IFTTT_app_notification = 'https://maker.ifttt.com/trigger/{}/with/key/b3ar4w7HdU-dl2y8gssZREZFE-v1my9f1SISVyTuGDc'
        ifttt_event_url = IFTTT_url_for_IFTTT_app_notification.format(event)
        requests.post(ifttt_event_url, json = data)

    def send_message_to_telegram(self, event, value) :

        # In this function we will send Latest 5 bitcoin prices to telegram as message

        data = {"value1" : value}
        IFTTT_url_for_telegram_message = 'https://maker.ifttt.com/trigger/{}/with/key/b3ar4w7HdU-dl2y8gssZREZFE-v1my9f1SISVyTuGDc'
        ifttt_event_url = IFTTT_url_for_telegram_message.format(event)
        requests.post(ifttt_event_url, json = data)

    def format_bitcoin_history(self, bitcoin_history) :

        # In this function we will format the date in to a string

        latest_five_bitcoin_prices = []
        for bitcoin_price in bitcoin_history :
            date = bitcoin_price['date'].strftime('%d.%m.%Y')
            time = bitcoin_price['date'].strftime('%H : %M : %S')
            price = bitcoin_price['price']

            # <b> (bold) tag creates bolded text
            # 24.02.2018 15:09: $<b>10123.4</b>

            row = '<b> The price of Bitcoin is ${} at Time {} on Date {} </b>'.format(price, time, date)
            latest_five_bitcoin_prices.append(row)

            # Use a <br> (break) tag to create a new line
            # Join the rows delimited by <br> tag: row1<br>row2<br>row3

        return '<br>'.join(latest_five_bitcoin_prices)
    def main(self) :

        BITCOIN_PRICE_THRESHOLD = int(input("Enter your bictcoin price threshold value : \n"))
        bitcoin_history = []

        while True :
            price = self.taking_latest_bitcoin_prices()
            print("Latest bitcoin price is :" , price,"dollars")
            date = datetime.now()

            # Appending price and date as a dictionary in to bitcon_history list

            bitcoin_history.append({'date': date, 'price': price})

            # sends and emergency notification if the bitcoin prices falls below bitcoin threshold value
            if price < BITCOIN_PRICE_THRESHOLD :

                self.send_notification_to_IFTTT_app("bitcoin_price_emergency", price)

            # send the five latest bitcoin prices as a message to telegram 
            if len(bitcoin_history) == 5 :

                self.send_message_to_telegram('bitcoin_price_update',self.format_bitcoin_history(bitcoin_history))
                # Reset the history
                bitcoin_history = []
                print("DO YOU WANT TO EXIT")
                user_input = input("Enter yes or no :\n") 
                if user_input == "yes" :
                    return
                else :
                    continue
            # Sleep for 5 minutes s
            time.sleep(5 * 60)
            

if __name__ == "__main__" :

    print("Welcome to Bitcoin price Notification")

    bitcoinprice = Bitcoin()
    bitcoinprice.main()