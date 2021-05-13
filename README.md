# covid-vaccine-alerts

Checks the Cowin portal periodically to find vaccination slots available in the pin code and for your age. If found, it will send you push notifications on telegram every minute until the slots are available.


Steps to run the script:

Open telegram app and search for @PushitBot
Generate pushitbot token by sending /token to the bot.
Enter the details in the .env file
Install dependencies pip install -r requirements.txt
Run the application python main.py


Configuring .env file

PINCODES=533001, 533003, 533002, 533005
MIN_AGE_LIMIT=18
TOKEN=<your-token>
INTERVAL=60
