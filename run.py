import sys

def run():
    if len(sys.argv) == 0:
        print("No entry point specified.")
        exit(1)

    app = sys.argv[0]
    print(app)

    if "discordbot" in sys.argv:
        from discordbot import bot
        bot.init()
    elif "decksite" in sys.argv:
        from decksite import main
        main.init()
    elif "price_grabber" in sys.argv:
        from price_grabber import price_grabber
        price_grabber.fetch()
        price_grabber.price.cache()
    elif "srv_price" in sys.argv:
        from price_grabber import srv_prices
        srv_prices.init()

run()
