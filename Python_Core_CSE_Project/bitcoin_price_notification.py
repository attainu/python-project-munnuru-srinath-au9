import requests
import time
from datetime import datetime
import threading
import sys
menu = \
"****************************************\n\
*                                      *\n\
*      BITCOIN PRICE NOTIFIER          *\n\
*                                      *\n\
****************************************"

BITCOIN_PRICE_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'

# "https://api.coindesk.com/v1/bpi/currentprice.json" From this URL we will fecth the json data that includes bitcoin price

class Configuration :
    def __init__(self, time_in_seconds, no_of_messages, max_price, min_price) :
        self.time_in_seconds = time_in_seconds
        self.no_of_messages = no_of_messages
        self.max_price = max_price
        self.min_price = min_price
    
    def print_configurations(self) :
        print("Time = ", self.time_in_seconds)
        print("No of messages = ", self.no_of_messages)
        print("Maximum Price = ", self.max_price)
        print("Minimum Price = ", self.min_price)
    
    def set_time_in_seconds(self, time) :
        self.time_in_seconds = time
    def set_no_of_messages(self, messages) :
        self.no_of_messages = messages
    def set_max_price(self, max_price) :
        self.max_price = max_price
    def set_min_price(self, min_price) :
        self.min_price = min_price

class Bitcoin() :

    def __init__(self, configurations) :
        self.configurations = configurations
        self.time_out = False
    
    def change_time_out(self) :
        self.time_out = True

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
    def run(self) :

        bitcoin_history = []

        if configurations.time_in_seconds > 0  :
            timer = threading.Timer(configurations.time_in_seconds, self.change_time_out)
            timer.start()
        while not self.time_out:
            price = self.taking_latest_bitcoin_prices()
            print("Latest bitcoin price is :" , price,"dollars")
            date = datetime.now()

            # Appending price and date as a dictionary in to bitcon_history list

            bitcoin_history.append({'date': date, 'price': price})

            # sends an emergency notification if the bitcoin prices falls below minimum  bitcoin price value 
            if price < configurations.min_price :

                self.send_notification_to_IFTTT_app("bitcoin_price_emergency_if_price_is less", price)
            #sends an emergency notification if the bitcoin price goes above the maximum bitcoin price value
            if price > configurations.max_price :

                self.send_notification_to_IFTTT_app("bitcoin_price_emergency_if_price_is_greater_than_max_price", price)

            # send the five latest bitcoin prices as a message to telegram 
            if len(bitcoin_history) == configurations.no_of_messages :

                self.send_message_to_telegram('bitcoin_price_update',self.format_bitcoin_history(bitcoin_history))
                # Reset the history
                bitcoin_history = []
            # Sleep for 5 seconds
            time.sleep(5)
def solve_argument(arguments) :
    if "--help" == arguments :
        return "--help"

    for i in range(len(arguments)) :
        if arguments[i] == "=" :
            return arguments[:i]
    return None

def get_argument_value(arguments) :
    if len(arguments) > 100 :
        return -1

    for i in range(len(arguments)) :
        if arguments[i] == "=" :
            value = arguments[i + 1 :]
            for i in range(len(value)) :
                if not (ord(value[i]) >=ord("0") and ord(value[i]) <= ord("9")) :
                    return -1

            return int(value)
        
        

def parse_command_line_args(args, configurations) :
    for i in range(1, len(args)) :
        if "-time" == solve_argument(args[i]) :
            value = get_argument_value(args[i])
            if value != -1  :
                configurations.set_time_in_seconds(value)
        elif "-messages" == solve_argument(args[i]) :
            value = get_argument_value(args[i])
            if value != -1  :
                configurations.set_no_of_messages(value)
        elif "-maxprice" == solve_argument(args[i]) :
            value = get_argument_value(args[i])
            if value != -1  :
                configurations.set_max_price(value)
        elif "-minprice" == solve_argument(args[i]) :
            value = get_argument_value(args[i])
            if value != -1  :
                configurations.set_min_price(value)
        elif "--help" == solve_argument(args[i]) :

            print("-time                      Duration for which the application has to run")
            print("-messages                  Number of messages to be sent at once")
            print("-maxprice                  Price above which the alert has to be sent")
            print("-minprice                  Price below which the alert has to be sent")
            print("--help                     Displays how to cofigure application using command line arguments\n")
            print("If you want to run this application for Infinite time of time don't give time arugument in command line")
            
            return -1
        else :
            print("INVALID arguments, Please Use --help to know the valid arguments")
            return -1
    return 1



if __name__ == "__main__" :
    #global menu
    print(menu)
    configurations = Configuration(-1, 5, 10000, 12000)
    args = sys.argv
    if 1 == parse_command_line_args(args, configurations) :
        configurations.print_configurations()
        bitcoinprice = Bitcoin(configurations)
        bitcoinprice.run()