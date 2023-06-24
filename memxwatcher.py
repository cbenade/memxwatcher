import os
import random
import re
import time
from bs4 import BeautifulSoup as soup
from discord_webhook import DiscordWebhook
from twilio.rest import Client
from urllib.request import Request, urlopen


def main():
    verbose("memxwatcher.py entering main")
    random.seed(a=None)
    check_interval = 5
    city = os.environ['CITY']
    client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
    prog = re.compile("c-cact-product-list--empty")
    urls = {"South": os.environ['URL_SOUTH'], "West": os.environ['URL_WEST']}

    while True:
        for store in urls.keys():
            req = Request(urls[store], headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            page_soup = soup(webpage, "html.parser")
            parser_result = str(page_soup.find(id="AjaxProductList")).splitlines()[0]
            result = prog.search(parser_result)

            if result is None:
                verbose(f"found gpu(s) at {city} {store} location! sending text to C")
                client.messages.create(
                    body=f"RTX 3080 in stock at {city} {store} location! {os.environ['URL_ALL']}",
                    from_=os.environ['TWILIO_PN'],
                    to=os.environ['MY_PN']
                )
            else:
                verbose(f"no gpu(s) found at {city} {store} location")

        sleep_timer = ((check_interval + random.randint(0, 6)) * 60) + random.randint(0, 60)
        verbose(f"about to sleep for {sleep_timer} seconds...")
        time.sleep(sleep_timer)


def verbose(message):
    print(message)
    webhook = DiscordWebhook(url=os.environ['DISCORD_WEBHOOK_URL'], content=message)
    webhook.execute()


if __name__ == "__main__":
    main()
