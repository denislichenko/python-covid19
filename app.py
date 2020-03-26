import telebot
import requests
import json
import etc
import configuration


class Serializer(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)


bot = telebot.TeleBot(configuration.botToken)


@bot.message_handler(commands=['start'])
def send_hello(message):
    text = etc.text['start_0'] + message.chat.first_name + etc.text['start_1']
    bot.reply_to(message, text)


@bot.message_handler(commands=['cases'])
def send_cases(message):
    response = requests.request("GET", configuration.apiUrl, headers=configuration.apiHeaders)
    stats = Serializer(response.text).response
    for item in stats:
        if item['country'] == 'All':
            bot.reply_to(message, getInfo(item))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, etc.text['help'])


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all(message):
    try:
        querystring = {"country": message.text}
        response = requests.request("GET", configuration.apiUrl, headers=configuration.apiHeaders, params=querystring)
        stats = Serializer(response.text).response
        if len(stats) > 0:
            bot.reply_to(message, getInfo(stats[0]))
        else:
            bot.reply_to(message, "No info")
    except:
        bot.reply_to(message, "No info")


def getInfo(item):
    country = item['country']
    cases = item['cases']
    active = cases['active']
    new = cases['new']
    critical = cases['critical']
    recovered = cases['recovered']

    deaths = item['deaths']
    total_deaths = deaths['total']
    new_deaths = deaths['new']

    date = item['day']

    return "COVID-19 stats for {date} (Country: {country}):\n" \
           "☣️ Active: {active} ({new})\n" \
           "😷 Critical: {critical}\n" \
           "💀 Deaths: {deaths} ({newDeaths})\n" \
           "💉 Recovered: {recovered}".format(date=date, country=country, active=active, new=new, critical=critical,
                                              deaths=total_deaths, newDeaths=new_deaths, recovered=recovered)


bot.polling();
