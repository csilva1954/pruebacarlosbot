from bs4 import BeautifulSoup  #del módulo bs4, necesitamos BeautifulSoup
import requests
import json
import os


from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name} {update.effective_user.last_name}')


def btc_scraping():
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
    format_result = result.text

    return format_result


def bitcoin(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'El precio del Bitcoin es: {btc_scraping()}')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hola {update.effective_user.first_name}\n\nLos comandos que entiendo son: \n/start\n/bitcoin\n/boletin\n/covid\n/clima\n/hello\n/help')

def boletinProvincia():
    # https://www.boletinoficial.gba.gob.ar/
    r = requests.get('https://www.boletinoficial.gba.gob.ar/')
    soup = BeautifulSoup(r.text, 'lxml')
    
    # print(soup.prettify())

    # div_main = soup.div
    # div_main['id']
    # div_main.attrs{'id': 'main', 'class': ['fa fa-file-text-o']}
    
    result = soup.find('p', {'class': 'last-bulletin'})
    # result = (result.replace('<strong>','')).replace('</strong>','')
    # print(result)
    
    format_result = result.text
    format_result = format_result.replace('Ver anteriores', '')

    return format_result


def boletin(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{boletinProvincia()}')


def covidEstadistica():

    # r = requests.get('https://www.argentina.gob.ar/salud/coronavirus-COVID-19/sala-situacion')
    r = requests.get('https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Argentina')
    soup = BeautifulSoup(r.text, 'lxml')
    
    # print(soup.prettify())

    # div_main = soup.div
    # div_main['id']
    # div_main.attrs{'id': 'main', 'class': ['fa fa-file-text-o']}


    result = soup.find('table', {'class': "infobox"})
    
    # result = result.find('tr': {'th class': ['infobox-label scope=row>Confirmed cases']})
    # print(result)

    temp = result.text.index('Confirmed cases')

    # print('Valor de temp:', temp)
    
    format_result = result.text[int(temp) + 15: int(temp) + 24]
    # format_result = format_result.replace('Ver anteriores', '')

    return format_result

def covid(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Los casos hasta la fecha en Argentina son: {covidEstadistica()}')


def climaLaPlata():
    r = requests.get('https://www.meteored.com.ar/tiempo-en_La+Plata-America+Sur-Argentina-Provincia+de+Buenos+Aires-SADL-1-16930.html')
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.prettify())
    result = soup.find('span', {'class': "datos-estado-actual"})
    
    # print('\n\n', result)
    format_result = result.text

    inicio = int(format_result.index('Tiempo en La Plata'))
    final = int(format_result.index('Por horas'))

    format_result1 = format_result[inicio:final]

    return format_result1


def clima(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'El {climaLaPlata()}')



def citaCod():
    r = requests.get('https://zenquotes.io/api/random')

    json_data = json.loads(r.text)

    # print(json_data)

    # print('\n\n', json_data[0])

    cita = json_data[0]['q'] + ' - ' + json_data[0]['a']

    # print(cita)

    # soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.prettify())
    # result = soup.find('tags', {'famous-quotes': "content"})
    
    # print('\n\n', result)
    # format_result = soup

    # inicio = int(format_result.index('Tiempo en La Plata'))
    #  final = int(format_result.index('Por horas'))

    # format_result1 = format_result[inicio:final]

    return cita


def cita(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{citaCod()}')

# print(os.environ)

updater = Updater(token=os.environ['BOTTOKEN'], use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.dispatcher.add_handler(CommandHandler('bitcoin', bitcoin))

updater.dispatcher.add_handler(CommandHandler('boletin', boletin))

updater.dispatcher.add_handler(CommandHandler('covid', covid))

updater.dispatcher.add_handler(CommandHandler('clima', clima))

updater.dispatcher.add_handler(CommandHandler('cita', cita))

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(CommandHandler('help', start))

updater.start_polling()
updater.idle()
