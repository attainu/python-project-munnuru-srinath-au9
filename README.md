# BITCOIN PRICE NOTIFICATION
## PROJECT DESCRIPTION :
### As well all know, the Bitcoin price is fickle thing. You never really know where it’s going to be at the end of the day. So, instead of constantly checking various sites for the latest updates, this project gives us the IFTTT app notification if the bitcoin price falls under the some threshold price and also sends telegram messages for regular bitcoin price updates to our telegram app on mobile
## Target :
### 1) Telegram message
### 2) IFTTT app notification
## Technologies used :
### 1) Python 3.8
### 2) HTTPS
### 3) Webhooks
### 4) Messaging pltforms like telegram, IFTT
## API References :
### Coindesk
### IFTTT API References

![image](https://github.com/attainu/python-project-munnuru-srinath-au9/blob/dev/Screen_shots/Screenshot%20(116).png)
![image](https://github.com/attainu/python-project-munnuru-srinath-au9/blob/dev/Screen_shots/Screenshot_20200918-165418_One%20UI%20Home.jpg)
![image](https://github.com/attainu/python-project-munnuru-srinath-au9/blob/dev/Screen_shots/Screenshot_20200918-165524_One%20UI%20Home.jpg)

## Dependencies :
### In this project we need to import requests library and time library. "requests" library is used to make an htttp(hyper text transfer protocol) request to a server so that we can get data from the sever using requests.get() method , post data to user using requests.post() method, update data at server using requests.update() method and we can delete data using requests.delete() method
### Time library is used to import present date and time so that we can notify user the price of bitcoin along with date and time
### sys library is used to take command line arguments from user. The arguments that are accepted in this project are
### <b>-time ,time in seconds that the program needs to end</b>
### <b>-messages, number of messages that a user wants to get in telegram</b>
### <b>-maxprice, maximum price of bitcoin according to user</b>
### <b>-minprice, minimum price of bitcoin according to user</b>
### threading library is used to add a timer so the the program ends after the user given time

## Work Flow :
### Fisrt the user have to give command line arguments as mentioned in dependencies, according to those argument values we will send notifications to user. If the user don't want to give any command line arguments then the default values will be taken and the notifications will be sent to user as per those default calues
### The applications firstly runs by fetching the bitcoin price value from "https://api.coindesk.com/v1/bpi/currentprice.json" this server using requests.get() method .
### The next step is to create IFTTT(if this, then that) applets. We need three applets, first One is for sending emergency notification from IFTTT app if the bitcoin price is below minimum price given by the user, second one is for sending emergency notification from IFTTT app if the bitcoin price is above maximum price given by user and the last applet is for sending regular price updates to user as a message in telegram
### After this it will check the bitcoin price value with the maximum bitcoin price and minimum bitcoin price given by user . If the bitcoin price is less than minimum price given by user then we will send a notification from IFTTT app and same for maximum price. We will send the regular price updates of bitcoin as a message in telegram

## Output :
![image](https://github.com/attainu/python-project-munnuru-srinath-au9/blob/dev/Screen_shots/Screenshot%20(117).png)

