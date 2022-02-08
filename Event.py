# -*-coding: utf-8 -*-
import logging
import sqlite3
import random
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import quote_html
from aiogram.types import ContentTypes
from aiogram.types import ContentType
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decimal import Decimal
from bs4 import BeautifulSoup
import requests
from pycoingecko import CoinGeckoAPI

logging.basicConfig(level=logging.INFO)

# TOKEN EVENT - 5194858844:AAHXLAiQTT2PJS3TRS9ftXvwb-qHLCcWN3g

#CoinGeckoAPI
api = CoinGeckoAPI()

# bot init
bot = Bot(token='5194858844:AAHXLAiQTT2PJS3TRS9ftXvwb-qHLCcWN3g')
dp = Dispatcher(bot)

# datebase
connect = sqlite3.connect("users.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id BIGINT,
    balance INT,
    bank BIGINT,
    deposit INT,
    bitkoin INT,
    Ecoins INT,
    energy INT,
    expe INT,
    games INT,
    user_name STRING,
    user_status STRING,
    deposit_status INT,
    rating INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS mine(
    user_id BIGINT,
    user_name STRING,
    iron INT,
    gold INT,
    diamonds INT,
    amethysts INT,
    aquamarine INT,
    emeralds INT,
    matter INT,
    plasma INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS property(
    user_id BIGINT,
    user_name STRING,
    have STRING,
    yacht INT,
    cars INT,
    plane INT,
    helicopter INT,
    house INT,
    phone INT,
    business INT,
    farm INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS bot(
    chat_id INT,
    last_stavka INT
)
""")




# start command
@dp.message_handler(commands=['start'])
async def start_cmd(message):
    msg = message
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    user_status = "Player"
    have = 'off'
    chat_id = message.chat.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 10000, 0, 0, 0, 0, 10, 0, 0, user_name, user_status, 0, 0))
        cursor.execute("INSERT INTO property VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, have,0 ,0, 0, 0, 0, 0, 0, 0))
        cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, 0, 0, 0, 0, 0, 0, 0, 0))
        cursor.execute("INSERT INTO bot VALUES(?, ?);", (chat_id, 0))
        connect.commit()
    else:
        cursor.execute("INSERT INTO bot VALUES(?, ?);", (chat_id, 0))
        connect.commit()
        return

    name1 = message.from_user.get_mention(as_html=True)
    await message.reply(
        f'📌👋 Привет {name1}!\nЯ бот для игры в различные игры.\nТебе выдан подарок в размере 10.000$.\n\nТак же ты можешь добавить меня в беседу для игры с друзьями.\n🆘 Чтобы узнать все команды введи "Помощь"',
        parse_mode='html')


###########################################БАЛАНС###########################################
@dp.message_handler()
async def prof_user(message: types.Message):
    if message.forward_date != None:
        rx = ['😌','🥱','🙄','😎','😏']
        rdrx = random.choice(rx)
        await bot.send_message(message.chat.id,f"Извини, но тут дюп запрещён{rdrx}")
        return
    if message.text.lower() in ["баланс", "Баланс", "Б", "б"]:
        msg = message
        user_id = msg.from_user.id
        user_name = msg.from_user.full_name
        chat_id = message.chat.id
        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])
        bitkoin2 = '{:,}'.format(bitkoin)
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        balance2 = '{:,}'.format(balance)
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = round(int(bank[0]))
        bank2 = '{:,}'.format(bank)
        c = 999999999999999999999999
        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
        else:
            pass
        if bank >= 999999999999999999999999:
            bank = 999999999999999999999999
            cursor.execute(f'UPDATE users SET bank = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            bank2 = '{:,}'.format(bank)
        else:
            pass
        if bitkoin >= 999999999999999999999999:
            biktoin = 999999999999999999999999
            cursor.execute(f'UPDATE users SET bitkoin = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
        await bot.send_message(message.chat.id,
                               f"👫Ник: {user_name} \n💰Деньги: {balance2}$ \n🏦Банк: {bank2}$\n💽 Биткоины: {bitkoin2}🌐")
    ################################################КУПИТЬ Энергию######################################################
    if message.text.startswith('Купить энергию'):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        summ = int(message.text.split()[2])

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        ob_summ = summ + energy
        c = 5000
        ob_summ2 = c * summ
        ob_summ3 = '{:,}'.format(ob_summ2)
        if ob_summ <= 10:
            if ob_summ <= balance:
                await bot.send_message(message.chat.id, f'{name}, вы успешно купили {summ} ⚡️ за {ob_summ3}$ {rwin}', parse_mode='html')
                cursor.execute(f'UPDATE users SET energy = {energy + summ}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - ob_summ2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас нехватает средств! {rloser}', parse_mode='html')
        else:
            await bot.send_message(message.chat.id, f'{name}, нельзя делать покупку Энергии больше лимита {rloser}\nЛимит: 10 ⚡️', parse_mode='html')


    ################################################ПРОФИЛЬ#############################################################
    if message.text.lower() in ["профиль", "Профиль"]:
        msg = message
        chat_id = message.chat.id
        name1 = message.from_user.get_mention(as_html=True)
        user_name = msg.from_user.full_name
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])
        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        expe2 = '{:,}'.format(expe)
        games = cursor.execute("SELECT games from users where user_Id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        games2 = '{:,}'.format(games)
        balance = int(balance[0])
        bank = int(bank[0])
        rating = int(rating[0])
        Ecoins = cursor.execute("SELECT Ecoins from users where user_id = ?", (message.from_user.id,)).fetchone()
        Ecoins = int(Ecoins[0])
        Ecoins2 = "{:,}".format(Ecoins)
        have = cursor.execute("SELECT have from property where user_id = ?", (message.from_user.id,)).fetchone()
        have = str(have[0])
        c = 999999999999999999999999

        yacht = cursor.execute("SELECT yacht from property where user_id = ?", (message.from_user.id,)).fetchone()
        yacht = int(yacht[0])
        cars = cursor.execute("SELECT cars from property where user_id = ?", (message.from_user.id,)).fetchone()
        cars = int(cars[0])
        plane = cursor.execute("SELECT plane from property where user_id = ?", (message.from_user.id,)).fetchone()
        plane = int(plane[0])
        helicopter = cursor.execute("SELECT helicopter from property where user_id = ?", (message.from_user.id,)).fetchone()
        helicopter = int(helicopter[0])
        house = cursor.execute("SELECT house from property where user_id = ?", (message.from_user.id,)).fetchone()
        house = int(house[0])
        phone = cursor.execute("SELECT phone from property where user_id = ?", (message.from_user.id,)).fetchone()
        phone = int(phone[0])
        besiness = cursor.execute("SELECT business from property where user_id = ?", (message.from_user.id,)).fetchone()
        besiness = int(besiness[0])
        farm = cursor.execute("SELECT farm from property where user_id = ?", (message.from_user.id,)).fetchone()
        farm = int(farm[0])

        #Фермы
        if farm == 0:
            farm2 = ''
        if farm == 1:
            farm2 = '🔋 Ферма: TI-Miner'
        if farm == 2:
            farm2 = '🔋 Ферма: Saturn'
        if farm == 3:
            farm2 = '🔋 Ферма: Calisto'
        if farm == 4:
            farm2 = '🔋 Ферма: HashMiner'
        if farm == 5:
            farm2 = '🔋 Ферма: MegaWatt'
        #Бизнесы
        if besiness == 0:
            besiness2 = ''
        if besiness == 1:
            besiness2 = '💼 Бизнес: Шаурмечная'
        if besiness == 2:
            besiness2 = '💼 Бизнес: Ночной клуб'
        if besiness == 3:
            besiness2 = '💼 Бизнес: Кальянная'
        if besiness == 4:
            besiness2 = '💼 Бизнес: АЗС'
        if besiness == 5:
            besiness2 = '💼 Бизнес: Порностудия'
        if besiness == 6:
            besiness2 = '💼 Бизнес: Маленький офис'
        if besiness == 7:
            besiness2 = '💼 Бизнес: Нефтевышка'
        if besiness == 8:
            besiness2 = '💼 Бизнес: Космическое агентство'
        if besiness == 9:
            besiness2 = '💼 Бизнес: Межпланетный экспресс'
        if besiness == 10:
            besiness2 = '💼 Бизнес: Генератор материи'
        if besiness == 11:
            besiness2 = '💼 Бизнес: Генератор материи'
        #Телефоны
        if phone == 0:
            phone2 = ''
        if phone == 1:
            phone2 = '📱 Телефон: Nokia 3310'
        if phone == 2:
            phone2 = '📱 Телефон: ASUS ZenFone 4'
        if phone == 3:
            phone2 = '📱 Телефон: BQ Aquaris X'
        if phone == 4:
            phone2 = '📱 Телефон: Huawei P40'
        if phone == 5:
            phone2 = '📱 Телефон: Samsung Galaxy S21 Ultra'
        if phone == 6:
            phone2 = '📱 Телефон: Xiaomi Mi 11'
        if phone == 7:
            phone2 = '📱 Телефон: iPhone 11 Pro'
        if phone == 8:
            phone2 = '📱 Телефон: iPhone 12 Pro Max'
        if phone == 9:
            phone2 = '📱 Телефон: Blackberry'
        #Дома
        if house == 0:
            house2 = ''
        if house == 1:
            house2 = '🏠 Дом: Коробка'
        if house == 2:
            house2 = '🏠 Дом: Подвал'
        if house == 3:
            house2 = '🏠 Дом: Сарай'
        if house == 4:
            house2 = '🏠 Дом: Маленький домик'
        if house == 5:
            house2 = '🏠 Дом: Квартира'
        if house == 6:
            house2 = '🏠 Дом: Огромный дом'
        if house == 7:
            house2 = '🏠 Дом: Коттедж'
        if house == 8:
            house2 = '🏠 Дом: Вилла'
        if house == 9:
            house2 = '🏠 Дом: Загородный дом'
        if house == 10:
            house2 = '🏠 Дом: Небоскрёб'
        if house == 11:
            house2 = '🏠 Дом: Дом на мальдивах'
        if house == 12:
            house2 = '🏠 Дом: Технологичный небосрёб'
        if house == 13:
            house2 = '🏠 Дом: Собственный остров'
        if house == 14:
            house2 = '🏠 Дом: Дом на марсе'
        if house == 15:
            house2 = '🏠 Дом: Остров на марсе'
        if house == 16:
            house2 = '🏠 Дом: Свой марс'

        #Вертолёты
        if helicopter == 0 :
            helicopter2 = ''
        if helicopter == 1 :
            helicopter2 = '🚁 Вертолёт: Воздушный шар'
        if helicopter == 2 :
            helicopter2 = '🚁 Вертолёт: RotorWay Exec 162F'
        if helicopter == 3 :
            helicopter2 = '🚁 Вертолёт: Robinson R44'
        if helicopter == 4 :
            helicopter2 = '🚁 Вертолёт: Hiller UH-12C'
        if helicopter == 5 :
            helicopter2 = '🚁 Вертолёт: AW119 Koala'
        if helicopter == 6 :
            helicopter2 = '🚁 Вертолёт: MBB BK 117'
        if helicopter == 7 :
            helicopter2 = '🚁 Вертолёт: Eurocopter EC130'
        if helicopter == 8 :
            helicopter2 = '🚁 Вертолёт: Leonardo AW109 Power'
        if helicopter == 9 :
            helicopter2 = '🚁 Вертолёт: Sikorsky S-76'
        if helicopter == 10 :
            helicopter2 = '🚁 Вертолёт: Bell 429WLG'
        if helicopter == 11 :
            helicopter2 = '🚁 Вертолёт: NHI NH90'
        if helicopter == 12 :
            helicopter2 = '🚁 Вертолёт: Kazan Mi-35M'
        if helicopter == 13 :
            helicopter2 = '🚁 Вертолёт: Bell V-22 Osprey'
        #Самолёты
        if plane == 0:
            plane2 = ''
        if plane == 1:
            plane2 = '✈️ Самолёт: Параплан'
        if plane == 2:
            plane2 = '✈️ Самолёт: АН-2'
        if plane == 3:
            plane2 = '✈️ Самолёт: Cessna-172E'
        if plane == 4:
            plane2 = '✈️ Самолёт: BRM NG-5'
        if plane == 5:
            plane2 = '✈️ Самолёт: Cessna T210'
        if plane == 6:
            plane2 = '✈️ Самолёт: Beechcraft 1900D'
        if plane == 7:
            plane2 = '✈️ Самолёт: Cessna 550'
        if plane == 8:
            plane2 = '✈️ Самолёт: Hawker 4000'
        if plane == 9:
            plane2 = '✈️ Самолёт: Learjet 31'
        if plane == 10:
            plane2 = '✈️ Самолёт: Airbus A318'
        if plane == 11:
            plane2 = '✈️ Самолёт: F-35A'
        if plane == 12:
            plane2 = '✈️ Самолёт: Boeing 747-430'
        if plane == 13:
            plane2 = '✈️ Самолёт: C-17A Globemaster III'
        if plane == 14:
            plane2 = '✈️ Самолёт: F-22 Raptor'
        if plane == 15:
            plane2 = '✈️ Самолёт: Airbus 380 Custom'
        if plane == 16:
            plane2 = '✈️ Самолёт: B-2 Spirit Stealth Bomber'
        #Машины
        if cars == 0:
            cars2 = ''
        if cars == 1:
            cars2 = '🚗 Машина: Самокат'
        if cars == 2:
            cars2 = '🚗 Машина: Велосипед'
        if cars == 3:
            cars2 = '🚗 Машина: Гироскутер'
        if cars == 4:
            cars2 = '🚗 Машина: Сегвей'
        if cars == 5:
            cars2 = '🚗 Машина: Мопед'
        if cars == 6:
            cars2 = '🚗 Машина: Мотоцикл'
        if cars == 7:
            cars2 = '🚗 Машина: ВАЗ 2109'
        if cars == 8:
            cars2 = '🚗 Машина: Квадроцикл'
        if cars == 9:
            cars2 = '🚗 Машина: Багги'
        if cars == 10:
            cars2 = '🚗 Машина: Вездеход'
        if cars == 11:
            cars2 = '🚗 Машина: Лада Xray'
        if cars == 12:
            cars2 = '🚗 Машина: Audi Q7'
        if cars == 13:
            cars2 = '🚗 Машина: BMW X6'
        if cars == 14:
            cars2 = '🚗 Машина: Toyota FT-HS'
        if cars == 15:
            cars2 = '🚗 Машина: BMW Z4 M'
        if cars == 16:
            cars2 = '🚗 Машина: Subaru WRX STI'
        if cars == 17:
            cars2 = '🚗 Машина: Lamborghini Veneno'
        if cars == 18:
            cars2 = '🚗 Машина: Tesla Roadster'
        if cars == 19:
            cars2 = '🚗 Машина: Yamaha YZF R6'
        if cars == 20:
            cars2 = '🚗 Машина: Bugatti Chiron'
        if cars == 21:
            cars2 = '🚗 Машина: Thrust SSC'
        if cars == 22:
            cars2 = '🚗 Машина: Ferrari LaFerrari'
        if cars == 23:
            cars2 = '🚗 Машина: Koenigsegg Regear'
        if cars == 24:
            cars2 = '🚗 Машина: Tesla Semi'
        if cars == 25:
            cars2 = '🚗 Машина: Venom GT'
        if cars == 26:
            cars2 = '🚗 Машина: Rolls-Royce'
        #Яхты
        if yacht == 0:
            yacht2 = ''
        if yacht == 1:
            yacht2 = '🛥 Яхта: Ванна'
        if yacht == 2:
            yacht2 = '🛥 Яхта: Nauticat 331'
        if yacht == 3:
            yacht2 = '🛥 Яхта: Nordhavn 56 MS'
        if yacht == 4:
            yacht2 = '🛥 Яхта: Princess 60'
        if yacht == 5:
            yacht2 = '🛥 Яхта: Bayliner 288'
        if yacht == 6:
            yacht2 = '🛥 Яхта: Dominator 40M'
        if yacht == 7:
            yacht2 = '🛥 Яхта: Sessa Marine C42'
        if yacht == 8:
            yacht2 = '🛥 Яхта: Wider 150'
        if yacht == 9:
            yacht2 = '🛥 Яхта: Palmer Johnson 42M SuperSport'
        if yacht == 10:
            yacht2 = '🛥 Яхта: Serene'
        if yacht == 11:
            yacht2 = '🛥 Яхта: Dubai'
        if yacht == 12:
            yacht2 = '🛥 Яхта: Azzam'
        if yacht == 13:
            yacht2 = '🛥 Яхта: Streets of Monaco'


        if have == 'off':
            have2 = '😔 У вас нет имущества'

        if have == 'on':
            have2 = f"""
📦 Имущество:
    {yacht2}
    {cars2}
    {plane2}
    {helicopter2}
    {house2}
    {phone2}
    {besiness2}
            """

        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
        else:
            pass
        if int(balance) in range(0, 1000):
            balance3 = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
            balance3 = int(balance3[0])
        if int(balance) in range(1000, 999999):
            balance1 = balance / 1000
            balance2 = round(balance1)
            balance3 = f'{balance2} тыс'
        if int(balance) in range(1000000, 999999999):
            balance1 = balance / 1000000
            balance2 = round(balance1)
            balance3 = f'{balance2} млн'
        if int(balance) in range(1000000000, 999999999999):
            balance1 = balance / 1000000000
            balance2 = round(balance1)
            balance3 = f'{balance2} млрд'
        if int(balance) in range(1000000000000, 999999999999999):
            balance1 = balance / 1000000000000
            balance2 = round(balance1)
            balance3 = f'{balance2} трлн'
        if int(balance) in range(1000000000000000, 999999999999999999):
            balance1 = balance / 1000000000000000
            balance2 = round(balance1)
            balance3 = f'{balance2} квдр'
        if int(balance) in range(1000000000000000000, 999999999999999999999):
            balance1 = balance / 1000000000000000000
            balance2 = round(balance1)
            balance3 = f'{balance2} квнт'
        if int(balance) in range(1000000000000000000000, 999999999999999999999999):
            balance1 = balance / 1000000000000000000000
            balance2 = round(balance1)
            balance3 = f'{balance2} скст'
        if bank >= 999999999999999999999999:
            bank = 999999999999999999999999
            cursor.execute(f'UPDATE users SET bank = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
        else:
            pass
        if int(bank) in range(0, 1000):
            bank3 = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
            bank3 = int(bank3[0])
        if int(bank) in range(1000, 999999):
            bank1 = bank / 1000
            bank2 = round(bank1)
            bank3 = f'{bank2} тыс'
        if int(bank) in range(1000000, 999999999):
            bank1 = bank / 1000000
            bank2 = round(bank1)
            bank3 = f'{bank2} млн'
        if int(bank) in range(1000000000, 999999999999):
            bank1 = bank / 1000000000
            bank2 = round(bank1)
            bank3 = f'{bank2} млрд'
        if int(bank) in range(1000000000000, 999999999999999):
            bank1 = bank / 1000000000000
            bank2 = round(bank1)
            bank3 = f'{bank2} трлн'
        if int(bank) in range(1000000000000000, 999999999999999999):
            bank1 = bank / 1000000000000000
            bank2 = round(bank1)
            bank3 = f'{bank2} квдр'
        if int(bank) in range(1000000000000000000, 999999999999999999999):
            bank1 = bank / 1000000000000000000
            bank2 = round(bank1)
            bank3 = f'{bank2} квнт'
        if int(bank) in range(1000000000000000000000, 999999999999999999999999):
            bank1 = bank / 1000000000000000000000
            bank2 = round(bank1)
            bank3 = f'{bank2} скст'
        if rating >= 999999999999999999999999:
            rating = 999999999999999999999999
            cursor.execute(f'UPDATE users SET rating = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
        else:
            pass
        if int(rating) in range(0, 1000):
            rating3 = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
            rating3 = int(rating3[0])
        if int(rating) in range(1000, 999999):
            rating1 = rating / 1000
            rating2 = round(rating1)
            rating3 = f'{rating2} тыс'
        if int(rating) in range(1000000, 999999999):
            rating1 = rating / 1000000
            rating2 = round(rating1)
            rating3 = f'{rating2} млн'
        if int(rating) in range(1000000000, 999999999999):
            rating1 = rating / 1000000000
            rating2 = round(rating1)
            rating3 = f'{rating2} млрд'
        if int(rating) in range(1000000000000, 999999999999999):
            rating1 = rating / 1000000000000
            rating2 = round(rating1)
            rating3 = f'{rating2} трлн'
        if int(rating) in range(1000000000000000, 999999999999999999):
            rating1 = rating / 1000000000000000
            rating2 = round(rating1)
            rating3 = f'{rating2} квдр'
        if int(rating) in range(1000000000000000000, 999999999999999999999):
            rating1 = rating / 1000000000000000000
            rating2 = round(rating1)
            rating3 = f'{rating2} квнт'
        if int(rating) in range(1000000000000000000000, 999999999999999999999999):
            rating1 = rating / 1000000000000000000000
            rating2 = round(rating1)
            rating3 = f'{rating2} скст'
        if bitkoin > 999999999999999999999999:
            bitkoin = 999999999999999999999999
            cursor.execute(f"UPDATE users SET bitkoin = {999999999999999999999999}  WHERE user_id = ?", (user_id,))
            connect.commit()
        else:
            pass
        if int(bitkoin) in range(0, 1000):
            bitkoin3 = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
            bitkoin3 = int(bitkoin3[0])
        if int(bitkoin) in range(1000, 999999):
            bitkoin1 = bitkoin / 1000
            bitkoin2 = round(bitkoin1)
            bitkoin3 = f'{bitkoin2} тыс'
        if int(bitkoin) in range(1000000, 999999999):
            bitkoin1 = bitkoin / 1000000
            bitkoin2 = round(bitkoin1)
            bitkoin3 = f'{bitkoin2} млн'
        if int(bitkoin) in range(1000000000, 999999999999):
            bitkoin1 = bitkoin / 1000000000
            bitkoin2 = round(bitkoin1)
            bitkoin3 = f'{bitkoin2} млрд'
        if int(bitkoin) in range(1000000000000, 999999999999999):
            bitkoin1 = bitkoin / 1000000000000
            bitkoin2 = round(bitkoin1)
            bitkoin3 = f'{bitkoin2} трлн'
        if int(bitkoin) in range(1000000000000000, 999999999999999999):
            bitkoin1 = bitkoin / 1000000000000000
            bitkoin2 = round(bitkoin1)
            bitkoin3 = f'{bitkoin2} квдр'
        if int(bitkoin) in range(1000000000000000000, 999999999999999999999):
            bitkoin1 = bitkoin / 1000000000000000000
            bitkoin2 = round(bitkoin1)
            bitkoin3 = f'{bitkoin2} квнт'
        if int(bitkoin) in range(1000000000000000000000, 999999999999999999999999):
            bitkoin1 = bitkoin / 1000000000000000000000
            bitkoin2 = round(bitkoin1)
            bitkoin3 = f'{bitkoin2} скст'
        await bot.send_message(message.chat.id,
                               f"{name1}, ваш профиль : \n 🔎 ID: {user_id}\n 💰 Деньги: {balance3}$\n 🏦 В банке: {bank3}$\n💳 E-Coins: {Ecoins2}\n💽 Биткоины: {bitkoin3}🌐\n🏋️ Энергия: {energy}\n 👑 Рейтинг: {rating3}\n🌟 Опыт: {expe2}\n🎲 Всего сыграно игр: {games2}\n\n {have2}",
                               parse_mode='html')
################################################КУРС РУДЫ###############################################################
    if message.text.lower() in ['курс руды','Курс руды']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'''
{name},курс руды:
⛓ 1 железо - 230.000$
🌕 1 золото - 1.000.000$
💎 1 алмаз - 116.000.000$
🎆 1 аметист - 216.000.000$
💠 1 аквамарин - 302.000.000$
🍀 1 изумруд - 366.000.000$
🌌 1 материя - 412.000.000$
💥 1 плазма - 632.000.000$
''', parse_mode='html')
###############################################ОГРАБИТЬ МЭРИЮ###########################################################
    if message.text.lower() in ['Ограбить мэрию', 'ограбить мэрию']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name}, эта команда в разработке ❌', parse_mode='html')
##############################################ИНВЕНТАРЬ#################################################################
    if message.text.lower() in ['Инвентарь', 'инвентарь']:
        name = message.from_user.get_mention(as_html=True)
        iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
        iron = int(iron[0])

        gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
        gold = int(gold[0])

        diamonds = cursor.execute("SELECT diamonds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        diamonds = int(diamonds[0])

        amethysts = cursor.execute("SELECT amethysts from mine where user_id = ?", (message.from_user.id,)).fetchone()
        amethysts = int(amethysts[0])

        aquamarine = cursor.execute("SELECT aquamarine from mine where user_id = ?", (message.from_user.id,)).fetchone()
        aquamarine = int(aquamarine[0])

        emeralds = cursor.execute("SELECT emeralds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        emeralds = int(emeralds[0])

        matter = cursor.execute("SELECT matter from mine where user_id = ?", (message.from_user.id,)).fetchone()
        matter = int(matter[0])

        plasma = cursor.execute("SELECT plasma from mine where user_id = ?", (message.from_user.id,)).fetchone()
        plasma = int(plasma[0])
        
        await bot.send_message(message.chat.id, f'''
{name}
⛓ Железо: {iron} шт.
🌕 Золото: {gold} шт.
💎 Алмазы: {diamonds} шт.
🎆 Аметисты: {amethysts} шт.
💠 Аквамарин: {aquamarine} шт.
❇️ Изумруды: {emeralds} шт.
🌌 Материя: {matter} шт.
🎇 Плазма: {plasma} шт.
''', parse_mode='html')
    #######################################БЕСЕДА#############################################
    if message.text.lower() in ['!беседа', '!Беседа']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} Официальная беседа💭\n@event_game_chat', parse_mode='html')
    #######################################РП Команды#########################################
    if message.text.lower() in ['отлизать', 'отлизать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} отлизал(а)  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Отсосать', 'отсосать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} отсосал(а)  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Облизать', 'облизать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} облизал(а) всего  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Шлепнуть', 'шлепнуть']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} шлепнул(а) {reply_name}', parse_mode='html')
    if message.text.lower() in ['Убить', 'убить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} убил(а) с оружия {reply_name}', parse_mode='html')
    if message.text.lower() in ['Укусить', 'укусить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} укусил(а) {reply_name}', parse_mode='html')
    if message.text.lower() in ['Ударить', 'ударить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} ударил(а) по голове  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Уебать', 'уебать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} жоско уебал(а) по ебалу {reply_name}', parse_mode='html')
    if message.text.lower() in ['Ущепнуть', 'ущепнуть']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} ущепнул(а) {reply_name}', parse_mode='html')
    if message.text.lower() in ['Трахнуть', 'трахнуть']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} занялся(лась) сексом в анал с {reply_name}', parse_mode='html')
    if message.text.lower() in ['Сжечь', 'сжечь']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} спалил(а) на костре  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Секс', 'секс']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} пошёл(а) заниматься сексом с  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Расстрелять', 'расстрелять']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} расстрелял(а) на палигоне  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Покормить', 'Покормить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} покормил(а)  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Пнуть', 'пнуть']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} дал по жопе с ноги  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Дать по лбу', 'дать по лбу']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} дал лычку  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Погладить', 'погладить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} погладил(а) по голове  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Понюхать', 'понюхать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} принюхался(лась) к  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Похвалить', 'похвалить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} похвалил(а)  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Послать нахуй', 'послать нахуй']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} послал(а) нахуй  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Пожать руку', 'пожать руку']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} пожал(а) руку очень крепко  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Потрогать', 'потрогать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} потрогал(а)  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Прижать', 'прижать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} прижал(а) к себе  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Поцеловать', 'поцеловать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} поцеловал(а)  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Поздравить', 'поздравить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} поздравил с праздником  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Отдаться', 'отдаться']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} отдался(лась) в кровате  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Отравить', 'отравить']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} отравил(а) ядом  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Обнять', 'Обнять']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} обнял(а) очень крепко  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Лизь', 'Лизь']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} лизнул(а)  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Лизнуть', 'лизнуть']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} лизнуть в щёку  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Кастрировать', 'кастрировать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} пошёл кастрировать  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Кусь', 'кусь']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} куснул  {reply_name}', parse_mode='html')
    if message.text.lower() in ['Изнасиловать', 'изнасиловать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} изнасиловал {reply_name}', parse_mode='html')
    if message.text.lower() in ['Извиниться', 'извиниться']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} извинилься перед {reply_name}', parse_mode='html')
    if message.text.lower() in ['Испугать', 'испугать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} испугал(а) {reply_name}', parse_mode='html')
    if message.text.lower() in ['Дать пять', 'дать пять']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} дал(а) пять {reply_name}', parse_mode='html')
    if message.text.lower() in ['Выебать', 'выебать']:
        name = message.from_user.get_mention(as_html=True)
        reply_name = message.reply_to_message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name} пошел(ла) заниматься интимом с {reply_name}', parse_mode='html')
    if message.text.lower() in ['Рп Команды', 'рп команды']:
        name = message.from_user.get_mention(as_html=True)


        await bot.send_message(message.chat.id, f'''
{name}, вот все доступные РП команды:
1) Выебать
2) Дать пять
3) Испугать
4) Ивиниться
5) Изнасиловать
6) Кусь
7) Кастрировать
8) Лизнуть
9) Лизь
10) Обнять
11) Отравить
12) Отдаться
13) Поздравить
14) Поцеловать
15) Прижать
16) Потрогать
17) Пожать руку
18) Послать нахуй
19) Похвалить
20) Понюхать
21) Погладить
22) Дать по лбу
23) Пнуть
24) Покормить
25) Расстрелять
26) Секс
27) Сжечь
28) Трахнуть
29) Ущепнуть
30) Уебать
31) Ударить
32) Укусить
33) Убить
34) Шлепнуть
35) Куснуть
36) Облизать
37) Отсосать
38) Отлизать
''', parse_mode='html')

    #######################################НИК################################################
    if message.text.lower() in ['Мой ник', 'мой ник']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name}, на данный моммент команда ещё в разработке ❌',
                               parse_mode='html')
    if message.text.lower() in ['Сменить ник', 'сменить ник']:
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        await bot.send_message(message.chat.id, f'{name}, что бы сменить ник введите команду "Сменить ник [Ваш ник]" {rloser}', parse_mode='html')
    if message.text.startswith('Сменить ник'):
        name = message.from_user.get_mention(as_html=True)

        nik = str(message.text.split()[2])

        await bot.send_message(message.chat.id, f'{name}, на данный моммент команда ещё в разработке ❌',
                               parse_mode='html')
    ######################################КАЗНА###############################################
    if message.text.lower() in ['Казна', 'казна']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name}, на данный моммент команда ещё в разработке ❌', parse_mode='html')
    ##################################ЕЖЕДНЕВНЫЙ БОНУС########################################
    if message.text.lower() in ['Ежедневный бонус', 'ежедневный бонус']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'{name}, на данный моммент команда ещё в разработке ❌', parse_mode='html')
    ###########################################БИТКОИН########################################
    if message.text.lower() in ['Биткоины', 'биткоины']:
        name = message.from_user.get_mention(as_html=True)

        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])
        bitkoin2 = '{:,}'.format(bitkoin)

        await bot.send_message(message.chat.id, f'{name}, на вашем балансе {bitkoin2} ВТС 🌐', parse_mode='html')
    if message.text.lower() in ['Биткоин продать','биткоин продать']:
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])
        bitkoin2 = '{:,}'.format(bitkoin)

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        c = api.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']

        summ = bitkoin * c
        summ2 = '{:,}'.format(summ)

        if bitkoin > 0:
            await bot.send_message(message.chat.id, f'{name}, вы успешно продали {bitkoin2} BTC за {summ2}$ {rwin}', parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET bitkoin = {bitkoin - bitkoin}  WHERE user_id = "{user_id}"')
            connect.commit()
        else:
            await bot.send_message(message.chat.id, f'{name}, недостаточно средств! {rloser}', parse_mode='html')

    if message.text.startswith('Биткоин продать'):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        bitcoin_c = int(message.text.split()[2])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        c = api.get_price(ids='bitcoin', vs_currencies = 'usd')['bitcoin']['usd']

        summ = bitcoin_c * c
        summ2 = '{:,}'.format(summ)

        if bitcoin_c <= bitkoin :
            if bitcoin_c > 0:
                await bot.send_message(message.chat.id,f'{name}, вы успешно продали {bitcoin_c} BTC за {summ2}$ {rwin}', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bitkoin = {bitkoin - bitcoin_c}  WHERE user_id = "{user_id}"')
                connect.commit()
                return
            else:
                await bot.send_message(message.chat.id,f'{name}, нельзя продать отрицательное число {rloser}', parse_mode='html')
                return
        else:
            await bot.send_message(message.chat.id,f'{name}, недостаточно средств! {rloser}', parse_mode='html')
            return
    if message.text.startswith('биткоин продать'):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        bitcoin_c = int(message.text.split()[2])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        c = api.get_price(ids='bitcoin', vs_currencies = 'usd')['bitcoin']['usd']

        summ = bitcoin_c * c
        summ2 = '{:,}'.format(summ)

        if bitcoin_c <= bitkoin :
            if bitcoin_c > 0:
                await bot.send_message(message.chat.id,f'{name}, вы успешно продали {bitcoin_c} BTC за {summ2}$ {rwin}', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bitkoin = {bitkoin - bitcoin_c}  WHERE user_id = "{user_id}"')
                connect.commit()
                return
            else:
                await bot.send_message(message.chat.id,f'{name}, нельзя продать отрицательное число {rloser}', parse_mode='html')
                return
        else:
            await bot.send_message(message.chat.id,f'{name}, недостаточно средств! {rloser}', parse_mode='html')
            return



    if message.text.startswith('биткоин купить'):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        bitcoin_c = int(message.text.split()[2])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        c = api.get_price(ids='bitcoin', vs_currencies = 'usd')['bitcoin']['usd']

        summ = bitcoin_c * c
        summ2 = '{:,}'.format(summ)

        if summ <= balance :
            if bitcoin_c > 0:
                await bot.send_message(message.chat.id,f'{name}, вы успешно купили {bitcoin_c} BTC за {summ2}$ {rwin}', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bitkoin = {bitkoin + bitcoin_c}  WHERE user_id = "{user_id}"')
                connect.commit()
                return
            else:
                await bot.send_message(message.chat.id,f'{name}, нельзя купить отрицательное число {rloser}', parse_mode='html')
                return
        else:
            await bot.send_message(message.chat.id,f'{name}, недостаточно средств! {rloser}', parse_mode='html')
            return


    if message.text.startswith('Биткоин купить'):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        bitcoin_c = int(message.text.split()[2])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        bitkoin = cursor.execute("SELECT bitkoin from users where user_id = ?", (message.from_user.id,)).fetchone()
        bitkoin = int(bitkoin[0])

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        c = api.get_price(ids='bitcoin', vs_currencies = 'usd')['bitcoin']['usd']

        summ = bitcoin_c * c
        summ2 = '{:,}'.format(summ)

        if summ <= balance :
            if bitcoin_c > 0:
                await bot.send_message(message.chat.id,f'{name}, вы успешно купили {bitcoin_c} BTC за {summ2}$ {rwin}', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bitkoin = {bitkoin + bitcoin_c}  WHERE user_id = "{user_id}"')
                connect.commit()
                return
            else:
                await bot.send_message(message.chat.id,f'{name}, нельзя купить отрицательное число {rloser}', parse_mode='html')
                return
        else:
            await bot.send_message(message.chat.id,f'{name}, недостаточно средств! {rloser}', parse_mode='html')
            return


    if message.text.lower() in ['Биткоин курс', 'биткоин курс']:
        name = message.from_user.get_mention(as_html=True)



        c = api.get_price(ids='bitcoin', vs_currencies = 'usd')['bitcoin']['usd']

        c2 = '{:,}'.format(c)

        await bot.send_message(message.chat.id, f'{name}, на данный момент курс 1 BTC состовляет - {c2}🌐',parse_mode='html')



    ###########################################БАНК###########################################
    # bank
    if message.text.lower() in ["Банк", "банк"]:
        msg = message
        chat_id = message.chat.id
        name1 = message.from_user.get_mention(as_html=True)
        user_name = msg.from_user.full_name
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        deposit_status = cursor.execute("SELECT deposit_status from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        deposit = cursor.execute("SELECT deposit from users where user_id = ?", (message.from_user.id,)).fetchone()
        rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
        deposit_status = int(deposit_status[0])
        deposit = int(deposit[0])
        balance = int(balance[0])
        bank = int(bank[0])
        rating = int(rating[0])
        balance2 = '{:,}'.format(balance)
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = round(int(bank[0]))
        bank2 = '{:,}'.format(bank)
        deposit2 = '{:,}'.format(deposit)
        if deposit_status == 0:
            deposit_status2 = 'Обычный'
        if deposit_status == 0:
            deposit_status3 = 6
        c = 999999999999999999999999
        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
        else:
            pass
        if bank >= 999999999999999999999999:
            bank = 999999999999999999999999
            cursor.execute(f'UPDATE users SET bank = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            bank2 = '{:,}'.format(bank)
        else:
            pass
        if deposit >= 999999999999999999999999:
            deposit = 999999999999999999999999
            cursor.execute(f'UPDATE users SET deposit = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            deposit2 = '{:,}'.format(deposit)
        await bot.send_message(message.chat.id, f'''
{name1}, ваш банковский счёт:
👫 Владелец: {user_name}
💰 Деньги в банке: {bank2}$
💎 Статус: {deposit_status2}
   〽️ Процент под депозит: {deposit_status3}%
   💵 Под депозитом: {deposit2}$
   ⏳ Можно снять: в разработке ❌
''', parse_mode='html')

    if message.text.startswith("Банк положить"):
        msg = message
        chat_id = message.chat.id
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)

        bank_p = int(msg.text.split()[2])
        print(f"{name} положил в банк: {bank_p}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = round(int(bank[0]))
        bank2 = '{:,}'.format(bank_p)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)
        if bank_p > 0:
            if balance >= bank_p:
                await bot.send_message(message.chat.id, f'{user_name}, вы успешно положили в банк {bank2}$ {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                connect.commit()

            elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f'{user_name}, недостаточно средств! {rloser}',
                                       parse_mode='html')

        if bank_p <= 0:
            await bot.send_message(message.chat.id,
                                   f'{user_name}, нельзя положить в банк отрицательное число! {rloser}',
                                   parse_mode='html')
    if message.text.startswith("банк положить"):
        msg = message
        chat_id = message.chat.id
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)

        bank_p = int(msg.text.split()[2])
        print(f"{name} положил в банк: {bank_p}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = round(int(bank[0]))
        bank2 = '{:,}'.format(bank_p)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)
        if bank_p > 0:
            if balance >= bank_p:
                await bot.send_message(message.chat.id, f'{user_name}, вы успешно положили в банк {bank2}$ {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                connect.commit()

            elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f'{user_name}, недостаточно средств! {rloser}',
                                       parse_mode='html')

        if bank_p <= 0:
            await bot.send_message(message.chat.id,
                                   f'{user_name}, нельзя положить в банк отрицательное число! {rloser}',
                                   parse_mode='html')

    if message.text.startswith("Банк снять"):
        msg = message
        chat_id = message.chat.id
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)

        bank_s = int(msg.text.split()[2])
        print(f"{name} снял с банка: {bank_s}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = round(int(bank[0]))
        bank2 = '{:,}'.format(bank_s)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        if bank_s > 0:
            if bank >= bank_s:
                await bot.send_message(message.chat.id,
                                       f'{user_name}, вы успешно сняли с банковского счёта {bank2}$ {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
                connect.commit()

            elif int(bank) < int(bank_s):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, недостаточно средств на банковском счету! {rloser}',
                                       parse_mode='html')
    if message.text.startswith("банк снять"):
        msg = message
        chat_id = message.chat.id
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)

        bank_s = int(msg.text.split()[2])
        print(f"{name} снял с банка: {bank_s}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
        bank = round(int(bank[0]))
        bank2 = '{:,}'.format(bank_s)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        if bank_s > 0:
            if bank >= bank_s:
                await bot.send_message(message.chat.id,
                                       f'{user_name}, вы успешно сняли с банковского счёта {bank2}$ {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
                connect.commit()

            elif int(bank) < int(bank_s):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, недостаточно средств на банковском счету! {rloser}',
                                       parse_mode='html')

        if bank_s <= 0:
            await bot.send_message(message.chat.id, f'{user_name}, нельзя снять с банка отрицательное число! {rloser}',
                                   parse_mode='html')

        ###########################################АДМИН КОМАНДЫ###########################################

    if message.text.lower() in ["админ", "Админ"]:
        await bot.send_message(message.chat.id,
                               f' Полный список команд для Администрации бота EVENT  : \n1️⃣Умножить [Количество] - Умножает баланс игрока\n2️⃣Выдать [Сумма] - выдает игроку деньги \n3️⃣Забрать [Сумма] - Забирает с баланса у игрока \n4️⃣Обнулить - Обнуляет игрока \n \n 🆘Эти команды работают только при условии ответа на сообщение игрока')
    if message.text.startswith("Умножить"):
        msg = message
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        perevod = int(msg.text.split()[1])
        reply_user_id = msg.reply_to_message.from_user.id
        perevod2 = '{:,}'.format(perevod)
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])
        if user_status[0] == 'Admin':
            await message.reply(f'Вы умножили Баланс в {perevod2} раза, пользователю {reply_user_name} {rwin}',
                                parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
            connect.commit()
        elif user_status[0] == 'Player':
            await message.reply(f'{user_name}, Доступ к данной команде ограничен. Для покупки администратора обратитесь к создателю 👨‍🦰', parse_mode='html')
    if message.text.startswith("умножить"):
        msg = message
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        perevod = int(msg.text.split()[1])
        reply_user_id = msg.reply_to_message.from_user.id
        perevod2 = '{:,}'.format(perevod)
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])
        if user_status[0] == 'Admin':
            await message.reply(f'Вами было умножено {perevod2}$ пользователю {reply_user_name} {rwin}',
                                parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
            connect.commit()
        elif user_status[0] == 'Player':
            await message.reply(f'{user_name}, Доступ к данной команде ограничен. Для покупки администратора обратитесь к создателю 👨‍🦰', parse_mode='html')

    if message.text.startswith("Выдать"):
        msg = message
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        perevod = int(msg.text.split()[1])
        reply_user_id = msg.reply_to_message.from_user.id
        perevod2 = '{:,}'.format(perevod)
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])
        if user_status[0] == 'Admin':
            await message.reply(f'Вами было ввыдано {perevod2}$ пользователю {reply_user_name} {rwin}',
                                parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
            connect.commit()
        elif user_status[0] == 'Player':
            await message.reply(f'{user_name}, Доступ к данной команде ограничен. Для покупки администратора обратитесь к создателю 👨‍🦰',
                                parse_mode='html')

    if message.text.startswith("забрать"):
        msg = message
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        user_name = message.from_user.get_mention(as_html=True)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        perevod = int(msg.text.split()[1])
        reply_user_id = msg.reply_to_message.from_user.id
        perevod2 = '{:,}'.format(perevod)
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])
        if user_status[0] == 'Admin':
            await message.reply(f'Вами было успешно отобрано {perevod2}$ у пользователя {reply_user_name} {rwin}',
                                parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
            connect.commit()
        elif user_status[0] == 'Player':
            await message.reply(f'{user_name}, Доступ к данной команде ограничен. Для покупки администратора обратитесь к создателю 👨‍🦰',
                                parse_mode='html')

    if message.text.startswith("Забрать"):
        msg = message
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        perevod = int(msg.text.split()[1])
        reply_user_id = msg.reply_to_message.from_user.id
        perevod2 = '{:,}'.format(perevod)
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])
        if user_status[0] == 'Admin':
            await message.reply(f'Вами было успешно отобрано {perevod2}$ у пользователя {reply_user_name} {rwin}',
                                parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
            connect.commit()
        elif user_status[0] == 'Player':
            await message.reply(f'{user_name}, Доступ к данной команде ограничен. Для покупки администратора обратитесь к создателю 👨‍🦰',
                                parse_mode='html')

    if message.text.lower() in ["обнулить", "Обнулить"]:
        msg = message
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        reply_user_id = msg.reply_to_message.from_user.id
        user_id = msg.from_user.id
        user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                     (message.from_user.id,)).fetchone()
        if user_status[0] == 'Admin':
            await message.reply(f'Вы обнулили игрока {reply_user_name} {rwin}', parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
            cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
            cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
            connect.commit()
        if user_status[0] == 'Player':
            await message.reply(f'ℹ{user_name}, Доступ к данной команде ограничен. Для покупки администратора обратитесь к создателю 👨‍🦰',
                                parse_mode='html')
#######################################################ДОМА#############################################################
    if message.text.startswith("купить дом"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        house = cursor.execute("SELECT house from property where user_id = ?", (message.from_user.id,)).fetchone()
        house = int(house[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 500000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Коробка" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 1000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Подвал" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 3000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Сарай" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 5000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Маленький домик" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 7000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Квартира" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 10000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Огромный дом" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 50000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Коттедж" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 100000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Вилла" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 5000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Загородный дом" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 50000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Небоскрёб" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 200000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Дом на мальдивах" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 1000000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Технологичный небосрёб" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 5000000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Собственный остров" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 14:
            price = 15000000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Дом на марсе" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {14}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 15:
            price = 25000000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Остров на марсе" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {15}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 16:
            price = 50000000000000
            if balance >= price:
                if house < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили дом "Свой марс" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET house = {16}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть дом {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')


    if message.text.lower() in ['Продать дом', "продать дом"]:
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        house = cursor.execute("SELECT house from property where user_id = ?", (message.from_user.id,)).fetchone()
        house = int(house[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)

        if house > 0 :
            if house == 1:
                price = 500000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 2:
                price = 1000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 3:
                price = 3000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 4:
                price = 5000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 5:
                price = 7000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 6:
                price = 10000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 7:
                price = 50000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 8:
                price = 100000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 9:
                price = 5000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 10:
                price = 50000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 11:
                price = 200000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 12:
                price = 1000000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 13:
                price = 5000000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 14:
                price = 15000000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 15:
                price = 25000000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if house == 16:
                price = 50000000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали дом за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET house = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
    if message.text.lower() in ['дома', 'Дома']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'''
{name}, доступные дома:
🏠 1. Коробка - 500.000$
🏠 2. Подвал - 1.000.000$
🏠 3. Сарай - 3.000.000$
🏠 4. Маленький домик - 5.000.000$
🏠 5. Квартира - 7.000.000$
🏠 6. Огромный дом - 10.000.000$
🏠 7. Коттедж - 50.000.000$
🏠 8. Вилла - 100.000.000$
🏠 9. Загородный дом - 5.000.000.000$
🏠 10. Небоскрёб - 50.000.000.000$
🏠 11. Дом на мальдивах - 200.000.000.000$
🏠 12. Технологичный небосрёб - 1.000.000.000.000$
🏠 13. Собственный остров - 5.000.000.000.000$
🏠 14. Дом на марсе - 15.000.000.000.000$
🏠 15. Остров на марсе - 25.000.000.000.000$
🏠 16. Свой марс - 50.000.000.000.000$

🛒 Для покупки дома введите "Купить дом [номер]"
''', parse_mode='html')
#######################################################КЕЙСЫ############################################################
    if message.text.lower() in ['Кейсы', 'кейсы']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id,f'{name}, данная команда ещё в разработке ❌')
######################################################ЯХТЫ##############################################################
    if message.text.lower() in ['Продать вертолёт', "продать вертолёт"]:
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        yacht = cursor.execute("SELECT yacht from property where user_id = ?", (message.from_user.id,)).fetchone()
        yacht = int(yacht[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)

        if yacht > 0 :
            if yacht == 1:
                price = 1000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 2:
                price = 10000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 3:
                price = 30000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 4:
                price = 100000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 5:
                price = 500000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 6:
                price = 800000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 7:
                price = 5000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 8:
                price = 15000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 9:
                price = 40000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 10:
                price = 90000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 11:
                price = 200000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 12:
                price = 600000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if yacht == 13:
                price = 1600000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали яхту за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET yacht = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
    if message.text.startswith("купить яхту"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        yacht = cursor.execute("SELECT yacht from property where user_id = ?", (message.from_user.id,)).fetchone()
        yacht = int(yacht[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 1000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Ванна" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 10000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Nauticat 331" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 30000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Nordhavn 56 MS" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 100000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Princess 60" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 500000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Bayliner 288" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 800000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Dominator 40M" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 5000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Sessa Marine C42" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 15000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Wider 150" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 40000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Palmer Johnson 42M SuperSport" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 90000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Serene" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 200000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Dubai" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 600000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Azzam" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 1600000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Streets of Monaco" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
    if message.text.startswith("Купить яхту"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        yacht = cursor.execute("SELECT yacht from property where user_id = ?", (message.from_user.id,)).fetchone()
        yacht = int(yacht[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 1000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Ванна" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 10000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Nauticat 331" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 30000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Nordhavn 56 MS" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 100000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Princess 60" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 500000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Bayliner 288" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 800000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Dominator 40M" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 5000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Sessa Marine C42" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 15000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Wider 150" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 40000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Palmer Johnson 42M SuperSport" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 90000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Serene" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 200000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Dubai" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 600000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Azzam" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 1600000000000
            if balance >= price:
                if yacht < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили яхту "Streets of Monaco" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET yacht = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть яхта {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
    if message.text.lower() in ['Яхты','яхты']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id,f'''
{name}, доступные яхты:
🛳 1. Ванна - 1.000.000$
🛳 2. Nauticat 331 - 10.000.000$
🛳 3. Nordhavn 56 MS - 30.000.000$
🛳 4. Princess 60 - 100.000.000$
🛳 5. Bayliner 288 - 500.000.000$
🛳 6. Dominator 40M - 800.000.000$
🛳 7. Sessa Marine C42 - 5.000.000.000$
🛳 8. Wider 150 - 15.000.000.000$
🛳 9. Palmer Johnson 42M SuperSport - 40.000.000.000$
🛳 10. Serene - 90.000.000.000$
🛳 11. Dubai - 200.000.000.000$
🛳 12. Azzam - 600.000.000.000$
🛳 13. Streets of Monaco - 1.600.000.000.000$

🛒 Для покупки яхты введите "Купить яхту [номер]"
''', parse_mode='html')
######################################################ВЕРТОЛЁТЫ#########################################################
    if message.text.startswith("Купить вертолёт"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        helicopter = cursor.execute("SELECT helicopter from property where user_id = ?", (message.from_user.id,)).fetchone()
        helicopter = int(helicopter[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 100000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Воздушный шар" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 350000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "RotorWay Exec 162F" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 700000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Robinson R44" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 1000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Hiller UH-12C" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 1400000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "AW119 Koala" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 2600000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "MBB BK 117" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 5500000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Eurocopter EC130" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 8800000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Leonardo AW109 Power" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 450000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Sikorsky S-76" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 800000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Bell 429WLG" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 1600000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "NHI NH90" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 2250000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Kazan Mi-35M" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 3500000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Bell V-22 Osprey" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
    if message.text.startswith("купить вертолёт"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        helicopter = cursor.execute("SELECT helicopter from property where user_id = ?", (message.from_user.id,)).fetchone()
        helicopter = int(helicopter[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 100000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Воздушный шар" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 350000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "RotorWay Exec 162F" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 700000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Robinson R44" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 1000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Hiller UH-12C" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 1400000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "AW119 Koala" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 2600000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "MBB BK 117" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 5500000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Eurocopter EC130" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 8800000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Leonardo AW109 Power" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 450000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Sikorsky S-76" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 800000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Bell 429WLG" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 1600000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "NHI NH90" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 2250000000000
            if balance >= price:
                if helicopter < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Kazan Mi-35M" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET helicopter = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 3500000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили вертолёт "Bell V-22 Osprey" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть вертолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
    if message.text.lower() in ['Продать вертолёт', "продать вертолёт"]:
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        helicopter = cursor.execute("SELECT helicopter from property where user_id = ?", (message.from_user.id,)).fetchone()
        helicopter = int(helicopter[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)

        if helicopter > 0 :
            if helicopter == 1:
                price = 100000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 2:
                price = 3500000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 3:
                price = 10000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 4:
                price = 30000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 5:
                price = 63400000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 6:
                price = 150000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 7:
                price = 350000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 8:
                price = 750000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 9:
                price = 1240000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 10:
                price = 8890000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 11:
                price = 88330000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 12:
                price = 225750000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if helicopter == 13:
                price = 945300000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали вертолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET helicopter = {0}  WHERE user_id = "{user_id}"')
                connect.commit()


    if message.text.lower() in ['Вертолёты', 'вертолёты']:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'''
{name}, доступные вертолёты:
🚁 1. Воздушный шар - 100.000$
🚁 2. RotorWay Exec 162F - 3.500.000$
🚁 3. Robinson R44 - 10.000.000$
🚁 4. Hiller UH-12C - 30.000.000$
🚁 5. AW119 Koala - 63.400.000$
🚁 6. MBB BK 117 - 150.000.000$
🚁 7. Eurocopter EC130 - 350.000.000$
🚁 8. Leonardo AW109 Power - 750.000.000$
🚁 9. Sikorsky S-76 - 1.240.000.000$
🚁 10. Bell 429WLG - 8.890.000.000$
🚁 11. NHI NH90 - 88.330.000.000$
🚁 12. Kazan Mi-35M - 225.750.000.000$
🚁 13. Bell V-22 Osprey - 945.300.000.000$

🛒 Для покупки вертолёта введите "Купить вертолет [номер]"
''', parse_mode='html')
######################################################САМОЛЁТЫ##########################################################
    if message.text.lower() in ['Продать самолёт', "продать самолёт"]:
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        plane = cursor.execute("SELECT plane from property where user_id = ?", (message.from_user.id,)).fetchone()
        plane = int(plane[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)

        if plane > 0 :
            if plane == 1:
                price = 100000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 2:
                price = 350000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 3:
                price = 700000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 4:
                price = 1000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 5:
                price = 1400000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 6:
                price = 2600000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 7:
                price = 5500000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 8:
                price = 8800000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 9:
                price = 450000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 10:
                price = 800000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 11:
                price = 1600000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 12:
                price = 2250000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 13:
                price = 3500000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 14:
                price = 4000000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 15:
                price = 6000000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if plane == 16:
                price = 13500000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали самолёт за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET plane = {0}  WHERE user_id = "{user_id}"')
                connect.commit()


    if message.text.startswith("купить самолёт"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        plane = cursor.execute("SELECT plane from property where user_id = ?", (message.from_user.id,)).fetchone()
        plane = int(plane[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 100000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Параплан" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 350000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Параплан" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 700000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Cessna-172E" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 1000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "BRM NG-5" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 1400000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Cessna T210" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 2600000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Beechcraft 1900D" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 5500000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Cessna 550" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 8800000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Hawker 4000" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 450000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Learjet 31" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 800000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Airbus A318" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 1600000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "F-35A" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 2250000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Boeing 747-430" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 3500000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "C-17A Globemaster III" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 14:
            price = 4000000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "F-22 Raptor" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {14}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 15:
            price = 6000000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Airbus 380 Custom" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {15}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 16:
            price = 13500000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "B-2 Spirit Stealth Bomber" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {16}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
    if message.text.startswith("Купить самолёт"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        plane = cursor.execute("SELECT plane from property where user_id = ?", (message.from_user.id,)).fetchone()
        plane = int(plane[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 100000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Параплан" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 350000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Параплан" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 700000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Cessna-172E" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 1000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "BRM NG-5" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 1400000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Cessna T210" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 2600000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Beechcraft 1900D" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 5500000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Cessna 550" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 8800000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Hawker 4000" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 450000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Learjet 31" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 800000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Airbus A318" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 1600000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "F-35A" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 2250000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Boeing 747-430" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 3500000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "C-17A Globemaster III" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 14:
            price = 4000000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "F-22 Raptor" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {14}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 15:
            price = 6000000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "Airbus 380 Custom" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {15}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 16:
            price = 13500000000000
            if balance >= price:
                if plane < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили самолёт "B-2 Spirit Stealth Bomber" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET plane = {16}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть самолёт {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
    if message.text.lower() in ['Самолёты', "самолёты"]:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id,f'''
{name}, доступные самолеты:
✈️ 1. Параплан - 100.000.000$
✈️ 2. АН-2 - 350.000.000$
✈️ 3. Cessna-172E - 700.000.000$
✈️ 4. BRM NG-5 - 1.000.000.000$
✈️ 5. Cessna T210 - 1.400.000.000$
✈️ 6. Beechcraft 1900D - 2.600.000.000$
✈️ 7. Cessna 550 - 5.500.000.000$
✈️ 8. Hawker 4000 - 8.800.000.000$
✈️ 9. Learjet 31 - 450.000.000.000$
✈️ 10. Airbus A318 - 800.000.000.000$
✈️ 11. F-35A - 1.600.000.000.000$
✈️ 12. Boeing 747-430 - 2.250.000.000.000$
✈️ 13. C-17A Globemaster III - 3.500.000.000.000$
✈️ 14. F-22 Raptor - 4.000.000.000.000$
✈️ 15. Airbus 380 Custom - 6.000.000.000.000$
✈️ 16. B-2 Spirit Stealth Bomber - 13.500.000.000.000$

🛒 Для покупки самолёта введите "Купить самолёт [номер]"
''', parse_mode='html')
####################################################ТЕЛЕФОНЫ############################################################
    if message.text.startswith("Купить телефон"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        phone = cursor.execute("SELECT phone from property where user_id = ?", (message.from_user.id,)).fetchone()
        phone = int(phone[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 100000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "Nokia 3310" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 3500000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "ASUS ZenFone 4" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 10000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "BQ Aquaris X" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 30000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "Huawei P40" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 63400000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "Samsung Galaxy S21 Ultra" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 150000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "Xiaomi Mi 11" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 350000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "iPhone 11 Pro" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 750000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "iPhone 12 Pro Max" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 1240000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили телефон "Blackberry" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
    if message.text.startswith("купить телефон"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        phone = cursor.execute("SELECT phone from property where user_id = ?", (message.from_user.id,)).fetchone()
        phone = int(phone[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])

        if nomer == 1:
            price = 100000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "Nokia 3310" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 2:
            price = 3500000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "ASUS ZenFone 4" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 3:
            price = 10000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "BQ Aquaris X" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 4:
            price = 30000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "Huawei P40" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 5:
            price = 63400000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id,
                                           f'{name}, вы успешно купили телефон "Samsung Galaxy S21 Ultra" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 6:
            price = 150000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "Xiaomi Mi 11" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 7:
            price = 350000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "iPhone 11 Pro" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 8:
            price = 750000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "iPhone 12 Pro Max" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
        if nomer == 9:
            price = 1240000000
            if balance >= price:
                if phone < 1:
                    await bot.send_message(message.chat.id, f'{name}, вы успешно купили телефон "Blackberry" 🎉',
                                           parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET phone = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть телефон {rloser}',
                                           parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}',
                                       parse_mode='html')
    if message.text.lower() in ['Продать телефон', "продать телефон"]:
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        phone = cursor.execute("SELECT phone from property where user_id = ?", (message.from_user.id,)).fetchone()
        phone = int(phone[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)

        if phone > 0 :
            if phone == 1:
                price = 100000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 2:
                price = 3500000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 3:
                price = 10000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 4:
                price = 30000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 5:
                price = 63400000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 6:
                price = 150000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 7:
                price = 350000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 8:
                price = 750000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if phone == 9:
                price = 1240000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали телефон за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET phone = {0}  WHERE user_id = "{user_id}"')
                connect.commit()


    if message.text.lower()in ['Телефоны', "телефоны"]:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'''
{name}, доступные телефоны:
📱 1. Nokia 3310 - 100.000$
📱 2. ASUS ZenFone 4 - 3.500.000$
📱 3. BQ Aquaris X - 10.000.000$
📱 4. Huawei P40 - 30.000.000$
📱 5. Samsung Galaxy S21 Ultra - 63.400.000$
📱 6. Xiaomi Mi 11 - 150.000.000$
📱 7. iPhone 11 Pro - 350.000.000$
📱 8. iPhone 12 Pro Max - 750.000.000$
📱 9. Blackberry - 1.240.000.000$

🛒 Для покупки телефона введите "Купить телефон [номер]"''', parse_mode='html')
#####################################################МАШИНЫ#############################################################
    if message.text.lower() in ['Продать машину', "продать машину"]:
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        cars = cursor.execute("SELECT cars from property where user_id = ?", (message.from_user.id,)).fetchone()
        cars = int(cars[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)

        if cars > 0 :
            if cars == 1:
                price = 10000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 2:
                price = 15000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 3:
                price = 30000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 4:
                price = 50000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 5:
                price = 90000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 6:
                price = 100000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 7:
                price = 250000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 8:
                price = 400000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 9:
                price = 600000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 10:
                price = 900000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 11:
                price = 1400000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 12:
                price = 2500000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 13:
                price = 6000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 14:
                price = 8000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 15:
                price = 10000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 16:
                price = 40000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 17:
                price = 100000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 18:
                price = 300000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 19:
                price = 500000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 20:
                price = 700000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 21:
                price = 900000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 22:
                price = 210000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 23:
                price = 310000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 24:
                price = 443000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 25:
                price = 643000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
            if cars == 26:
                price = 943000000000
                price2 = price / 2
                price3 = '{:,}'.format(price2)

                await bot.send_message(message.chat.id, f'{name}, вы успешно продали машину за {price3}$ ', parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + price2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE property SET cars = {0}  WHERE user_id = "{user_id}"')
                connect.commit()
        else:
            await bot.send_message(message.chat.id, f'{name}, у вас нет данного имущества {rloser}')

    if message.text.startswith("Купить машину"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        cars = cursor.execute("SELECT cars from property where user_id = ?", (message.from_user.id,)).fetchone()
        cars = int(cars[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 10000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Самокат" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 15000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Велосипед" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 30000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Гироскутер" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 50000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Сегвей" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 90000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Мопед" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 100000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Мотоцикл" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 250000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "ВАЗ 2109" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 400000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Квадроцикл" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 600000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Багги" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 900000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Вездеход" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 1400000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Лада Xray" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 2500000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Audi Q7" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 6000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "BMW X6" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 14:
            price = 8000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Toyota FT-HS" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {14}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 15:
            price = 10000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "BMW Z4 M" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {15}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 16:
            price = 40000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Subaru WRX STI" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {16}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 17:
            price = 100000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Lamborghini Veneno" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {17}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 18:
            price = 300000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Tesla Roadster" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {18}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 19:
            price = 500000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Yamaha YZF R6" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {19}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 20:
            price = 700000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Bugatti Chiron" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {20}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 21:
            price = 900000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Thrust SSC" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {21}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 22:
            price = 2100000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Ferrari LaFerrari" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {22}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 23:
            price = 3100000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Koenigsegg Regear" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {23}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 24:
            price = 4430000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Tesla Semi" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {24}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 25:
            price = 6430000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Venom GT" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {25}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 26:
            price = 9430000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Rolls-Royce" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {26}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        else:
            await bot.send_message(message.chat.id, f'{name}, такого номера нету в продаже {rloser}', parse_mode='html')
    if message.text.startswith("купить машину"):
        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        cars = cursor.execute("SELECT cars from property where user_id = ?", (message.from_user.id,)).fetchone()
        cars = int(cars[0])

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        nomer = int(message.text.split()[2])


        if nomer == 1:
            price = 10000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Самокат" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {1}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 2:
            price = 15000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Велосипед" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {2}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 3:
            price = 30000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Гироскутер" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {3}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 4:
            price = 50000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Сегвей" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {4}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 5:
            price = 90000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Мопед" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {5}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 6:
            price = 100000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Мотоцикл" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {6}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 7:
            price = 250000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "ВАЗ 2109" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {7}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 8:
            price = 400000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Квадроцикл" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {8}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 9:
            price = 600000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Багги" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {9}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 10:
            price = 900000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Вездеход" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {10}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 11:
            price = 1400000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Лада Xray" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {11}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')

        if nomer == 12:
            price = 2500000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Audi Q7" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {12}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 13:
            price = 6000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "BMW X6" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {13}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 14:
            price = 8000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Toyota FT-HS" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {14}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 15:
            price = 10000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "BMW Z4 M" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {15}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 16:
            price = 40000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Subaru WRX STI" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {16}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 17:
            price = 100000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Lamborghini Veneno" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {17}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 18:
            price = 300000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Tesla Roadster" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {18}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 19:
            price = 500000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Yamaha YZF R6" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {19}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 20:
            price = 700000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Bugatti Chiron" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {20}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 21:
            price = 900000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Thrust SSC" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {21}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 22:
            price = 2100000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Ferrari LaFerrari" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {22}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 23:
            price = 3100000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Koenigsegg Regear" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {23}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 24:
            price = 4430000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Tesla Semi" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {24}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 25:
            price = 6430000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Venom GT" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {25}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')
        if nomer == 26:
            price = 9430000000000
            if balance >= price:
                if cars < 1:
                    await bot.send_message(message.chat.id,f'{name}, вы успешно купили машину "Rolls-Royce" 🎉', parse_mode='html')
                    cursor.execute(f'UPDATE property SET have = "on"  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE users SET balance = {balance - price}  WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE property SET cars = {26}  WHERE user_id = "{user_id}"')
                    connect.commit()
                else:
                    await bot.send_message(message.chat.id, f'{name}, у вас уже есть машина {rloser}', parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f'{name}, у вас недостаточно средств для покупки данного имущества {rloser}', parse_mode='html')





    if message.text.lower()in ['Машины', "машины"]:
        name = message.from_user.get_mention(as_html=True)

        await bot.send_message(message.chat.id, f'''{name}, доступные машины:
🚗 1. Самокат - 10.000.000$
🚗 2. Велосипед - 15.000.000$
🚗 3. Гироскутер - 30.000.000$
🚗 4. Сегвей - 50.000.000$
🚗 5. Мопед - 90.000.000$
🚗 6. Мотоцикл - 100.000.000$
🚗 7. ВАЗ 2109 - 250.000.000$
🚗 8. Квадроцикл - 400.000.000$
🚗 9. Багги - 600.000.000$
🚗 10. Вездеход - 900.000.000$
🚗 11. Лада Xray - 1.400.000.000$
🚗 12. Audi Q7 - 2.500.000.000$
🚗 13. BMW X6 - 6.000.000.000$
🚗 14. Toyota FT-HS - 8.000.000.000$
🚗 15. BMW Z4 M - 10.000.000.000$
🚗 16. Subaru WRX STI - 40.000.000.000$
🚗 17. Lamborghini Veneno - 100.000.000.000$
🚗 18. Tesla Roadster - 300.000.000.000$
🚗 19. Yamaha YZF R6 - 500.000.000.000$
🚗 20. Bugatti Chiron - 700.000.000.000$
🚗 21. Thrust SSC - 900.000.000.000$
🚗 22. Ferrari LaFerrari - 2.100.000.000.000$
🚗 23. Koenigsegg Regear - 3.100.000.000.000$
🚗 24. Tesla Semi - 4.430.000.000.000$
🚗 25. Venom GT - 6.430.000.000.000$
🚗 26. Rolls-Royce - 9.430.000.000.000$

🛒 Для покупки машины введите "Купить машину [номер]"''', parse_mode='html')

##########################################ШАХТА#########################################################################
    if message.text.lower() in ['Моя шахта', 'моя шахта']:
        msg = message
        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        expe2 = '{:,}'.format(expe)

        name = message.from_user.get_mention(as_html=True)

        if expe >= 0 :
            lvl = '''
⛏ Ваш уровень: Железо ⛓
➡️ Следующий уровень: Золото 🌕'''
        if expe > 500 :
            lvl = '''
⛏ Ваш уровень: Золото 🌕
➡️ Следующий уровень: Алмазы 💎'''
        if expe > 2000:
            lvl = '''
⛏ Ваш уровень: Алмазы 💎
➡️ Следующий уровень: Аметисты ☄️'''
        if expe > 10000:
            lvl = '''
⛏ Ваш уровень: Аметисты ☄
➡️ Следующий уровень: Аквамарин  💠️'''
        if expe > 25000:
            lvl = '''
⛏ Ваш уровень: Аквамарин  💠️
➡️ Следующий уровень: Изумруды ❇️'''
        if expe > 60000:
            lvl = '''
⛏ Ваш уровень: Изумруды ❇
➡️ Следующий уровень: Материя 🌌️'''
        if expe > 100000:
            lvl = '''
⛏ Ваш уровень: Материя 🌌️
➡️ Следующий уровень: Плазма 🎇'''
        if expe >= 500000:
            lvl = '''
⛏ Ваш уровень: Плазма 🎇
➡️ Максимальный уровень 🏆'''


        await bot.send_message(message.chat.id, f'''
{name}, это ваш профиль шахты:
🏆 Опыт: {expe2}
⚡️ Энергия: {energy}
{lvl}''', parse_mode='html')

    if message.text.lower() in ['продать плазму', 'Продать плазму']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        plasma = cursor.execute("SELECT plasma from mine where user_id = ?", (message.from_user.id,)).fetchone()
        plasma = int(plasma[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = plasma * 632000000
        price2 = '{:,}'.format(price)

        if plasma <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет плазмы {rloser}')
        if plasma > 0 :
            await bot.send_message(message.chat.id, f'вы продали всю свою плазму за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET plasma = {plasma - plasma}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать плазму"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        plasma = cursor.execute("SELECT plasma from mine where user_id = ?", (message.from_user.id,)).fetchone()
        plasma = int(plasma[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 632000000
        price2 = '{:,}'.format(price)

        if quantity > plasma :
            await bot.send_message(message.chat.id, f'{name}, у вас нет плазму {rloser}')
        if quantity <= plasma :
            await bot.send_message(message.chat.id, f'вы продали {quantity} плазму за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET plasma = {plasma - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("продать плазму"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        plasma = cursor.execute("SELECT plasma from mine where user_id = ?", (message.from_user.id,)).fetchone()
        plasma = int(plasma[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 632000000
        price2 = '{:,}'.format(price)

        if quantity > plasma:
            await bot.send_message(message.chat.id, f'{name}, у вас нет плазму {rloser}')
        if quantity <= plasma:
            await bot.send_message(message.chat.id, f'вы продали {quantity} плазму за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET plasma = {plasma - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()





    if message.text.lower() in ['продать материю', 'Продать материю']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        matter = cursor.execute("SELECT matter from mine where user_id = ?", (message.from_user.id,)).fetchone()
        matter = int(matter[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = matter * 412000000
        price2 = '{:,}'.format(price)

        if matter <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет материи {rloser}')
        if matter > 0 :
            await bot.send_message(message.chat.id, f'вы продали всю свою материю за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET matter = {matter - matter}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать материю"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        matter = cursor.execute("SELECT matter from mine where user_id = ?", (message.from_user.id,)).fetchone()
        matter = int(matter[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 412000000
        price2 = '{:,}'.format(price)

        if quantity > matter :
            await bot.send_message(message.chat.id, f'{name}, у вас нет материи {rloser}')
        if quantity <= matter :
            await bot.send_message(message.chat.id, f'вы продали {quantity} материи за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET matter = {matter - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("Продать материю"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        matter = cursor.execute("SELECT matter from mine where user_id = ?", (message.from_user.id,)).fetchone()
        matter = int(matter[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 412000000
        price2 = '{:,}'.format(price)

        if quantity > matter:
            await bot.send_message(message.chat.id, f'{name}, у вас нет материи {rloser}')
        if quantity <= matter:
            await bot.send_message(message.chat.id, f'вы продали {quantity} материи за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET matter = {matter - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()





    if message.text.lower() in ['продать изумруды', 'Продать изумруды']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        emeralds = cursor.execute("SELECT emeralds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        emeralds = int(emeralds[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = emeralds * 366000000
        price2 = '{:,}'.format(price)

        if emeralds <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет изумрудов {rloser}')
        if emeralds > 0 :
            await bot.send_message(message.chat.id, f'вы продали все свои изумруды за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET emeralds = {emeralds - emeralds}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать изумруды"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        emeralds = cursor.execute("SELECT emeralds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        emeralds = int(emeralds[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 366000000
        price2 = '{:,}'.format(price)

        if quantity > emeralds :
            await bot.send_message(message.chat.id, f'{name}, у вас нет изумрудов {rloser}')
        if quantity <= emeralds :
            await bot.send_message(message.chat.id, f'вы продали {quantity} изумруды за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET emeralds = {emeralds - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("Продать изумруды"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        emeralds = cursor.execute("SELECT emeralds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        emeralds = int(emeralds[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 366000000
        price2 = '{:,}'.format(price)

        if quantity > emeralds:
            await bot.send_message(message.chat.id, f'{name}, у вас нет изумрудов {rloser}')
        if quantity <= emeralds:
            await bot.send_message(message.chat.id, f'вы продали {quantity} изумруды за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET emeralds = {emeralds - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()





    if message.text.lower() in ['продать аквамарин', 'Продать аквамарин']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        aquamarine = cursor.execute("SELECT aquamarine from mine where user_id = ?", (message.from_user.id,)).fetchone()
        aquamarine = int(aquamarine[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = aquamarine * 302000000
        price2 = '{:,}'.format(price)

        if aquamarine <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет аквамарина {rloser}')
        if aquamarine > 0 :
            await bot.send_message(message.chat.id, f'вы продали все свой аквамарин за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET aquamarine = {aquamarine - aquamarine}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать аквамарин"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        aquamarine = cursor.execute("SELECT aquamarine from mine where user_id = ?", (message.from_user.id,)).fetchone()
        aquamarine = int(aquamarine[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 302000000
        price2 = '{:,}'.format(price)

        if quantity > aquamarine :
            await bot.send_message(message.chat.id, f'{name}, у вас нет аквамарина {rloser}')
        if quantity <= aquamarine :
            await bot.send_message(message.chat.id, f'вы продали {quantity} аквамарин за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET aquamarine = {aquamarine - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("Продать аквамарин"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        aquamarine = cursor.execute("SELECT aquamarine from mine where user_id = ?", (message.from_user.id,)).fetchone()
        aquamarine = int(aquamarine[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 302000000
        price2 = '{:,}'.format(price)

        if quantity > aquamarine:
            await bot.send_message(message.chat.id, f'{name}, у вас нет аквамарина {rloser}')
        if quantity <= aquamarine:
            await bot.send_message(message.chat.id, f'вы продали {quantity} аквамарин за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET aquamarine = {aquamarine - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()




    if message.text.lower() in ['продать аметисты', 'Продать аметисты']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        amethysts = cursor.execute("SELECT amethysts from mine where user_id = ?", (message.from_user.id,)).fetchone()
        amethysts = int(amethysts[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = amethysts * 216000000
        price2 = '{:,}'.format(price)

        if amethysts <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет аметистов {rloser}')
        if amethysts > 0 :
            await bot.send_message(message.chat.id, f'вы продали все свои аметисты за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET amethysts = {amethysts - amethysts}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать аметисты"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        amethysts = cursor.execute("SELECT amethysts from mine where user_id = ?", (message.from_user.id,)).fetchone()
        amethysts = int(amethysts[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 266000000
        price2 = '{:,}'.format(price)

        if quantity > amethysts :
            await bot.send_message(message.chat.id, f'{name}, у вас нет аметистов {rloser}')
        if quantity <= amethysts :
            await bot.send_message(message.chat.id, f'вы продали {quantity} аметистов за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET amethysts = {amethysts - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("Продать аметисты"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        amethysts = cursor.execute("SELECT amethysts from mine where user_id = ?", (message.from_user.id,)).fetchone()
        amethysts = int(amethysts[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 266000000
        price2 = '{:,}'.format(price)

        if quantity > amethysts :
            await bot.send_message(message.chat.id, f'{name}, у вас нет аметистов {rloser}')
        if quantity <= amethysts :
            await bot.send_message(message.chat.id, f'вы продали {quantity} аметистов за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET amethysts = {amethysts - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()




    if message.text.lower() in ['продать алмазы', 'Продать алмазы']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        diamonds = cursor.execute("SELECT diamonds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        diamonds = int(diamonds[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = diamonds * 116000000
        price2 = '{:,}'.format(price)

        if diamonds <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет алмазов {rloser}')
        if diamonds > 0 :
            await bot.send_message(message.chat.id, f'вы продали все свои алмазы за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET diamonds = {diamonds - diamonds}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать алмазы"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        diamonds = cursor.execute("SELECT diamonds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        diamonds = int(diamonds[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 166000000
        price2 = '{:,}'.format(price)

        if quantity > diamonds :
            await bot.send_message(message.chat.id, f'{name}, у вас нет алмазов {rloser}')
        if quantity <= diamonds :
            await bot.send_message(message.chat.id, f'вы продали {quantity} алмазов за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET diamonds = {diamonds - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("Продать алмазы"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        diamonds = cursor.execute("SELECT diamonds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        diamonds = int(diamonds[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 166000000
        price2 = '{:,}'.format(price)

        if quantity > diamonds:
            await bot.send_message(message.chat.id, f'{name}, у вас нет алмазов {rloser}')
        if quantity <= diamonds:
            await bot.send_message(message.chat.id, f'вы продали {quantity} алмазов за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET diamonds = {diamonds - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()




    if message.text.lower() in ['продать золото', 'Продать золото']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
        gold = int(gold[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = gold * 1000000
        price2 = '{:,}'.format(price)

        if gold <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет золото {rloser}')
        if gold > 0 :
            await bot.send_message(message.chat.id, f'вы продали все своё золото за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET gold = {gold - gold}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать золото"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
        gold = int(gold[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 1000000
        price2 = '{:,}'.format(price)

        if quantity > gold :
            await bot.send_message(message.chat.id, f'{name}, у вас нет золото {rloser}')
        if quantity <= gold :
            await bot.send_message(message.chat.id, f'вы продали {quantity} золото за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET gold = {gold - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("Продать золото"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
        gold = int(gold[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 1000000
        price2 = '{:,}'.format(price)

        if quantity > gold:
            await bot.send_message(message.chat.id, f'{name}, у вас нет золото {rloser}')
        if quantity <= gold:
            await bot.send_message(message.chat.id, f'вы продали {quantity} золото за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET gold = {gold - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()




    if message.text.lower() in ['продать железо', 'Продать железо']:
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
        iron = int(iron[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        price = iron * 230000
        price2 = '{:,}'.format(price)

        if iron <= 0 :
            await bot.send_message(message.chat.id, f'{name}, у вас нет железа {rloser}')
        if iron > 0 :
            await bot.send_message(message.chat.id, f'вы продали все своё железо за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET iron = {iron - iron}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()
    if message.text.startswith("продать железо"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
        iron = int(iron[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 230000
        price2 = '{:,}'.format(price)

        if quantity > iron :
            await bot.send_message(message.chat.id, f'{name}, у вас нет железа {rloser}')
        if quantity <= iron :
            await bot.send_message(message.chat.id, f'вы продали {quantity} железо за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET iron = {iron - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.startswith("Продать железо"):
        user_id = message.from_user.id
        name = message.from_user.get_mention(as_html=True)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
        iron = int(iron[0])

        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])

        quantity = int(message.text.split()[2])

        price = quantity * 230000
        price2 = '{:,}'.format(price)

        if quantity > iron :
            await bot.send_message(message.chat.id, f'{name}, у вас нет железа {rloser}')
        if quantity <= iron :
            await bot.send_message(message.chat.id, f'вы продали {quantity} железо за {price2}$ ✅')
            cursor.execute(f'UPDATE mine SET iron = {iron - quantity}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET balance = {balance + price}  WHERE user_id = "{user_id}"')
            connect.commit()

    if message.text.lower() in ['копать плазму', 'Копать плазму']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        plasma = cursor.execute("SELECT plasma from mine where user_id = ?", (message.from_user.id,)).fetchone()
        plasma = int(plasma[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        rx = random.randint(10, 50)
        rx2 = random.randint(10, 40)

        if energy <= 0:
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')
        if energy >= 1:
            if expe >= 100000 :
                await bot.send_message(message.chat.id, f'{name}, +{rx} плазмы.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE mine SET plasma = {plasma + rx}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, чтобы копать плазму вам требуется 500.000 опыта {rloser}',parse_mode='html')
    if message.text.lower() in ['копать материю', 'Копать материю']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        matter = cursor.execute("SELECT matter from mine where user_id = ?", (message.from_user.id,)).fetchone()
        matter = int(matter[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        rx = random.randint(10, 50)
        rx2 = random.randint(10, 40)

        if energy <= 0:
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')
        if energy >= 1:
            if expe >= 100000 :
                await bot.send_message(message.chat.id, f'{name}, +{rx} материи.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE mine SET matter = {matter + rx}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, чтобы копать материю вам требуется 100.000 опыта {rloser}',parse_mode='html')
    if message.text.lower() in ['копать изумруды', 'Копать изумруды']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        emeralds = cursor.execute("SELECT emeralds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        emeralds = int(emeralds[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        rx = random.randint(10, 50)
        rx2 = random.randint(10, 40)

        if energy <= 0:
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')
        if energy >= 1:
            if expe >= 60000 :
                await bot.send_message(message.chat.id, f'{name}, +{rx} изумрудов.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE mine SET emeralds = {emeralds + rx}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, чтобы копать изумруды вам требуется 60.000 опыта {rloser}',parse_mode='html')
    if message.text.lower() in ['копать аквамарин', 'Копать аквамарин']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        aquamarine = cursor.execute("SELECT aquamarine from mine where user_id = ?", (message.from_user.id,)).fetchone()
        aquamarine = int(aquamarine[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        rx = random.randint(10, 50)
        rx2 = random.randint(10, 40)

        if energy <= 0:
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')
        if energy >= 1:
            if expe >= 25000 :
                await bot.send_message(message.chat.id, f'{name}, +{rx} аквамаринов.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE mine SET aquamarine = {aquamarine + rx}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, чтобы копать аквамарин вам требуется 25.000 опыта {rloser}',parse_mode='html')
    if message.text.lower() in ['копать аметисты', 'Копать аметисты']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        amethysts = cursor.execute("SELECT amethysts from mine where user_id = ?", (message.from_user.id,)).fetchone()
        amethysts = int(amethysts[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        rx = random.randint(10, 50)
        rx2 = random.randint(10, 40)

        if energy <= 0:
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')
        if energy >= 1:
            if expe >= 10000 :
                await bot.send_message(message.chat.id, f'{name}, +{rx} аметистов.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE mine SET amethysts = {amethysts + rx}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, чтобы копать аметисты вам требуется 10.000 опыта {rloser}',parse_mode='html')
    if message.text.lower() in ['копать алмазы', 'Копать алмазы']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        diamonds = cursor.execute("SELECT diamonds from mine where user_id = ?", (message.from_user.id,)).fetchone()
        diamonds = int(diamonds[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        rx = random.randint(20, 65)
        rx2 = random.randint(10, 40)

        if energy <= 0:
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')
        if energy >= 1:
            if expe >= 2000 :
                await bot.send_message(message.chat.id, f'{name}, +{rx} алмазов.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE mine SET diamonds = {diamonds + rx}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, чтобы копать алмазы вам требуется 2.000 опыта {rloser}',parse_mode='html')
    if message.text.lower() in ['копать золото', 'Копать золото']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
        gold = int(gold[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        rx = random.randint(15, 60)
        rx2 = random.randint(5, 30)

        if energy <= 0:
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')
        if energy >= 1:
            if expe >= 500 :
                await bot.send_message(message.chat.id, f'{name}, +{rx} золото.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + rx}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
                connect.commit()
            else:
                await bot.send_message(message.chat.id, f'{name}, чтобы копать золото вам требуется 500 опыта {rloser}',parse_mode='html')
    if message.text.lower() in ['копать железо', 'Копать железо']:

        name = message.from_user.get_mention(as_html=True)
        user_id = message.from_user.id

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])
        energy2 = energy - 1

        iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
        iron = int(iron[0])

        expe = cursor.execute("SELECT expe from users where user_id = ?", (message.from_user.id,)).fetchone()
        expe = int(expe[0])
        rx2 = random.randint(1, 25)
        expe2 = expe + rx2
        expe3 = '{:,}'.format(expe2)

        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)
        
        rx = random.randint(25,75)
        rx2 = random.randint(1,25)

        if energy >= 1 :
            await bot.send_message(message.chat.id, f'{name}, +{rx} железо.\n💡 Энергия: {energy2}, опыт: {expe3}',
                                   parse_mode='html')
            cursor.execute(f'UPDATE mine SET iron = {iron + rx}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET energy = {energy2}  WHERE user_id = "{user_id}"')
            cursor.execute(f'UPDATE users SET expe = {expe2}  WHERE user_id = "{user_id}"')
            connect.commit()

        if energy <= 0 :
            await  bot.send_message(message.chat.id, f'{name}, у вас закончилась энергия {rloser}', parse_mode='html')




    if message.text.lower() in ['Шахта', "шахта"]:
        name = message.from_user.get_mention(as_html=True)
        await bot.send_message(message.chat.id,f'''{name}, это шахта. Здесь вы сможете добыть ресурсы для дальнейшей продажи. На шахте можно добыть - железо, золото, алмазы, аметисты, материю. Чтобы копать вам понадобиться энергия.

 ✅ Как начать работать и добывать ресурсы?
Используйте команды «копать железо», «копать золото», «копать алмазы», «копать аметисты», «копать аквамарин», «копать изумруды», «копать материю», «копать плазму».

♻️ Как продавать ресурсы?
Используйте команды «продать железо», «продать золото», «продать алмазы», «продать аметисты», «продать аквамарин», «продать изумруды», «продать материю», «продать плазму»

📜 Как посмотреть свою статистику?
Используйте команду "Моя шахта", вы сможете просмотреть ваш опыт, сколько не хватает до следующего уровня, а также какая следующая стадия.''', parse_mode='html')
######################################Энергия####################################################
    if message.text.lower() in ['Энергия', "энергия", "енергия", "Енергия"]:
        name = message.from_user.get_mention(as_html=True)

        energy = cursor.execute("SELECT energy from users where user_id = ?", (message.from_user.id,)).fetchone()
        energy = int(energy[0])

        await bot.send_message(message.chat.id, f'{name}, на данный момент у тебя {energy} ⚡️', parse_mode='html')
    ###########################################ПРАВИЛА###########################################
    if message.text.lower() in ["Правила", "правила"]:
        await bot.send_message(message.chat.id,
                               f'⚡️ Правила EVENT ⚡️\n \n1.🐩Не оскорблять.\n1.2👿 Не провоцировать. на оскорбления.\n2.🐔Ни при каких условиях не трогать родителей и родных.\n3. 🔞НЕ скидывать контент порнографического характера (фото/видео)\n4. 🚔 Не обманывать.\n5. 🚫 Не флудить, спамить.\n6. 👻 Не присылать любого вида скримеры, а также стикеры 18+ или же стикеры которые несут в себе смысл убийства и прочее.\n7. ❌ Запрещено продавать "схемы заработка" с целью наживы и обмана игроков. Бан и обнуление аккаунта.\n8. 💰 Не заниматься попрошайничеством, не флудить "дайте денег" и т.п.\n🆘Незнание правил не освобождает от ответственности. За любое нарушение данного правила вы будете изгнаны.\n \nРазработчик - @nike_zxc')
    ###########################################ПОМОЩЬ###########################################
    if message.text.lower() in ["помощь", "Помощь"]:

        help = InlineKeyboardMarkup(row_width=2)
        main = InlineKeyboardButton(text='💡 Основные', callback_data='main')
        games = InlineKeyboardButton(text='🎲 Игры', callback_data='games')
        entertainment = InlineKeyboardButton(text='💥 Развлекательное', callback_data='entertainment')
        clan = InlineKeyboardButton(text='🏰 Кланы (В разработке...)', callback_data='clan')
        help.add(main, games, entertainment, clan)
        name1 = message.from_user.get_mention(as_html=True)
        await bot.send_message(message.chat.id,
                               f'{name1}, выберите категорию:\n  1️⃣ Основное\n   2️⃣ Игры\n   3️⃣ Развлекательное\n   4️⃣ Кланы(В разработке...)\n\n🆘 По всем вопросам - @nike_zxc', reply_markup=help , parse_mode='html')

    ###########################################ДОНАТ###########################################
    if message.text.lower() in ["донат", "Донат"]:
        await bot.send_message(message.chat.id,
                               f'На данный момент для покупки доступны такие виды товаров:\n1️⃣ Игровая валюта\n2️⃣ Admin статус\n\n🛒Для покупки обращайтесь к @nike_zxc')
    ###########################################СПИН#############################################
    if message.text.startswith("спин"):
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        balance2 = '{:,}'.format(balance)
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0, 110)
        msg = message
        name1 = message.from_user.get_mention(as_html=True)
        name = msg.from_user.last_name
        summ = int(msg.text.split()[1])
        print(f"{name} поставил в спин: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        period = 5
        getе = cursor.execute("SELECT last_stavka FROM bot WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = int(getе[0])
        stavkatime = time.time() - float(last_stavka)
        loz = ['💩|👑|👑', '💩|🖕|👑', '💎|🖕|👑', '💎|💣|🍌', '👑|🍌|🖕', '💎|🍓|💣']
        win = ['💎|🍓|🍌', '👑|💎|🍓', '🍓|👑|💎', '💎|🍓|🍌', '💎|🍓|🍓', '🍌|🍌|💎']
        Twin = ['💎|💎|💎', '🍓|🍓|🍓', '👑|👑|👑', '🍌|🍌|🍌']
        smtwin = ['🤯', '🤩', '😵', '🙀']
        smwin = ['🙂', '😋', '😄', '🤑', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rsmtwin = random.choice(smtwin)
        rsmtwin2 = random.choice(smtwin)
        rtwin = random.choice(Twin)
        rloser = random.choice(loser)
        rloser2 = random.choice(loser)
        rwin = random.choice(win)
        rloz = random.choice(loz)
        rsmwin = random.choice(smwin)
        rsmwin2 = random.choice(smwin)
        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 50):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f'{name1}, вот ваши результаты\n——————\n{rwin} - вы выиграли {c2}${rsmwin}\n——————\nПозравляю вас!{rsmwin2}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return

        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(51, 100):
                        c = Decimal(summ * 0)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f'{name1}, вот ваши результаты\n——————\n{rloz} - вы проиграли {c2}${rloser}\n——————\nПриймите мои соболезнования!{rloser2}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(101, 110):
                        c = Decimal(summ * 25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f'{name1}, вот ваши результаты\n——————\n{rtwin} - ДЖЕКПОТ, ВЫ ВЫИГРАЛИ {c2}${rsmtwin}\n——————\nПОЗДРАВЛЯЮ У ВАС ДЖЕКПОТ!{rsmtwin2}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f'{name1}, нельзя ставить отрицательное число! {rloser}',
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'{name1}, недостаточно средств! {rloser}', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'{name1}, извини. но играть можно только каждые 5️⃣ секунд. {rloser}',
                                   parse_mode='html')
            return
    if message.text.startswith("Спин"):
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        balance2 = '{:,}'.format(balance)
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0, 110)
        msg = message
        name1 = message.from_user.get_mention(as_html=True)
        name = msg.from_user.last_name
        summ = int(msg.text.split()[1])
        print(f"{name} поставил в спин: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bot WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        loz = ['💩|👑|👑', '💩|🖕|👑', '💎|🖕|👑', '💎|💣|🍌', '👑|🍌|🖕', '💎|🍓|💣']
        win = ['💎|🍓|🍌', '👑|💎|🍓', '🍓|👑|💎', '💎|🍓|🍌', '💎|🍓|🍓', '🍌|🍌|💎']
        Twin = ['💎|💎|💎', '🍓|🍓|🍓', '👑|👑|👑', '🍌|🍌|🍌']
        smtwin = ['🤯', '🤩', '😵', '🙀']
        smwin = ['🙂', '😋', '😄', '🤑', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rsmtwin = random.choice(smtwin)
        rsmtwin2 = random.choice(smtwin)
        rtwin = random.choice(Twin)
        rloser = random.choice(loser)
        rloser2 = random.choice(loser)
        rwin = random.choice(win)
        rloz = random.choice(loz)
        rsmwin = random.choice(smwin)
        rsmwin2 = random.choice(smwin)
        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 40):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f'{name1}, вот ваши результаты\n——————\n{rwin} - вы выиграли {c2}${rsmwin}\n——————\nПозравляю вас!{rsmwin2}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return

                    if int(rx) in range(41, 100):
                        c = Decimal(summ * 0)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f'{name1}, вот ваши результаты\n——————\n{rloz} - вы проиграли {c2}${rloser}\n——————\nПриймите мои соболезнования!{rloser2}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return

                    if int(rx) in range(101, 110):
                        c = Decimal(summ * 25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f'{name1}, вот ваши результаты\n——————\n{rtwin} - ДЖЕКПОТ, ВЫ ВЫИГРАЛИ {c2}${rsmtwin}\n——————\nПОЗДРАВЛЯЮ У ВАС ДЖЕКПОТ!{rsmtwin2}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f'{name1}, нельзя ставить отрицательное число! {rloser}',
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'{name1}, недостаточно средств! {rloser}', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'{name1}, извини. но играть можно только каждые 5️⃣ секунд. {rloser}',
                                   parse_mode='html')
            return

    ###########################################КАЗИНО###########################################
    if message.text.startswith("Казино"):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id

        win = ['🙂', '😋', '😄', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rx = random.randint(0, 110)
        rwin = random.choice(win)
        rloser = random.choice(loser)

        msg = message
        name1 = message.from_user.get_mention(as_html=True)
        name = msg.from_user.last_name
        summ = int(msg.text.split()[1])
        print(f"{name} поставил в казино: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bot WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 15):
                        c = Decimal(summ)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0) {rloser}', parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(16, 33):
                        c = Decimal(summ - summ * 0.25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0.25) {rloser}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(34, 54):
                        c = Decimal(summ * 0.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0.5) {rloser}',
                                               parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(54, 62):
                        c = Decimal(summ - summ * 0.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0.75) {rloser}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {balance - summ * 0.25} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(63, 73):
                        c = summ * 1
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, ваши деньги остаются при вас {c2}$ (x1) {rwin}',
                                               parse_mode='html')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(74, 83):
                        c = Decimal(summ * 1.25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x1.25) {rwin}', parse_mode='html')

                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 1.25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(84, 90):
                        c = Decimal(summ * 1.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x1.5) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 1.5)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(91, 96):
                        c = Decimal(summ * 1.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x1.75) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 1.75)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(97, 102):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x2) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(103, 106):
                        c = Decimal(summ * 3)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x3) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) == 110:
                        c = Decimal(summ * 50)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x50) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 50)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                    if int(rx) in range(107, 109):
                        c = Decimal(summ * 10)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x10) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 10)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f'{name1}, нельзя ставить отрицательное число! {rloser}',
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'{name1}, недостаточно средств! {rloser}', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'{name1}, извини. но играть можно только каждые 5️⃣ секунд. {rloser}',
                                   parse_mode='html')
            return

    if message.text.startswith("казино"):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id

        win = ['🙂', '😋', '😄', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rx = random.randint(0, 110)
        rwin = random.choice(win)
        rloser = random.choice(loser)

        msg = message
        name1 = message.from_user.get_mention(as_html=True)
        name = msg.from_user.last_name
        summ = int(msg.text.split()[1])
        print(f"{name} поставил в казино: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bot WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 15):
                        c = Decimal(summ)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0) {rloser}', parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(16, 33):
                        c = Decimal(summ - summ * 0.25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0.25) {rloser}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(34, 54):
                        c = Decimal(summ * 0.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0.5) {rloser}',
                                               parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(54, 62):
                        c = Decimal(summ - summ * 0.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы проиграли {c2}$ (x0.75) {rloser}',
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {balance - summ * 0.25} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(63, 73):
                        c = summ * 1
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, ваши деньги остаются при вас {c2}$ (x1) {rwin}',
                                               parse_mode='html')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(74, 83):
                        c = Decimal(summ * 1.25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x1.25) {rwin}', parse_mode='html')

                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 1.25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(84, 90):
                        c = Decimal(summ * 1.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x1.5) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 1.5)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(91, 96):
                        c = Decimal(summ * 1.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x1.75) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 1.75)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(97, 102):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x2) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) in range(103, 106):
                        c = Decimal(summ * 3)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x3) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                    if int(rx) == 110:
                        c = Decimal(summ * 50)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x50) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 50)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                    if int(rx) in range(107, 109):
                        c = Decimal(summ * 10)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, вы выиграли {c2}$ (x10) {rwin}', parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 10)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f'{name1}, нельзя ставить отрицательное число! {rloser}',
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'{name1}, недостаточно средств! {rloser}', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'{name1}, извини. но играть можно только каждые 5️⃣ секунд. {rloser}',
                                   parse_mode='html')
            return
    ###########################################РЕЙТИНГ###########################################
    if message.text.lower() in ["рейтинг", "Рейтинг"]:
        msg = message
        name1 = message.from_user.get_mention(as_html=True)

        rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
        rating = int(rating[0])
        rating2 = '{:,}'.format(rating)

        await bot.send_message(message.chat.id,f'{name1}, ваш рейтинг {rating2}👑', parse_mode='html')

    if message.text.startswith("Купить рейтинг"):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        user_name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[2])
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
        rating = int(rating[0])
        rating2 = '{:,}'.format(summ)
        c = summ * 150000000
        c2 = '{:,}'.format(c)
        if summ > 0:
            if int(balance) >= int(summ * 150000000):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, вы повысили количество вашего рейтинга на {rating2}👑 за {c2}$! {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET rating = {rating + summ} WHERE user_id = "{user_id}"')
                connect.commit()

            if int(balance) < int(summ * 150000000):
                await bot.send_message(message.chat.id, f'{user_name}, недостаточно средств! {rloser}',
                                       parse_mode='html')

        if summ <= 0:
            await bot.send_message(message.chat.id, f'{user_name}, нельзя купить отрицательное число! {rloser}',
                                   parse_mode='html')

    if message.text.startswith("Продать рейтинг"):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        user_name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[2])
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
        rating = int(rating[0])
        c = summ * 100000000
        c2 = '{:,}'.format(c)
        rating2 = '{:,}'.format(summ)
        if summ > 0:
            if int(rating) >= int(summ):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, вы понизили количество вашего рейтинга на {rating2}👑 за {c2}$! {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + c} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = "{user_id}"')
                connect.commit()

            if int(rating) < int(summ):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, у вас недостаточно рейтинга для его продажи! {rloser}',
                                       parse_mode='html')

        if summ <= 0:
            await bot.send_message(message.chat.id, f'{user_name}, нельзя продать отрицательное число! {rloser}',
                                   parse_mode='html')

    if message.text.startswith("купить рейтинг"):
        msg = message
        user_id = msg.from_user.id
        user_name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[2])
        chat_id = message.chat.id
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
        rating = int(rating[0])
        rating2 = '{:,}'.format(summ)
        c = summ * 150000000
        c2 = '{:,}'.format(c)
        if summ > 0:
            if int(balance) >= int(summ * 150000000):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, вы повысили количество вашего рейтинга на {rating2}👑 за {c2}$! {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET rating = {rating + summ} WHERE user_id = "{user_id}"')
                connect.commit()

            if int(balance) < int(summ * 150000000):
                await bot.send_message(message.chat.id, f'{user_name}, недостаточно средств! {rloser}',
                                       parse_mode='html')

        if summ <= 0:
            await bot.send_message(message.chat.id, f'{user_name}, нельзя купить отрицательное число! {rloser}',
                                   parse_mode='html')

    if message.text.startswith("продать рейтинг"):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        user_name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[2])
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
        rating = int(rating[0])
        c = summ * 100000000
        c2 = '{:,}'.format(c)
        rating2 = '{:,}'.format(summ)
        if summ > 0:
            if int(rating) >= int(summ):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, вы понизили количество вашего рейтинга на {rating2}👑 за {c2}$! {rwin}',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + c} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = "{user_id}"')
                connect.commit()

            if int(rating) < int(summ):
                await bot.send_message(message.chat.id,
                                       f'{user_name}, у вас недостаточно рейтинга для его продажи! {rloser}',
                                       parse_mode='html')

        if summ <= 0:
            await bot.send_message(message.chat.id, f'{user_name}, нельзя продать отрицательное число! {rloser}',
                                   parse_mode='html')

    ###########################################ПЕРЕВОДЫ###########################################
    if message.text.startswith("передать"):
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        rname = msg.reply_to_message.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        perevod = int(msg.text.split()[1])
        perevod2 = '{:,}'.format(perevod)
        print(f"{name} перевел: {perevod} игроку {rname}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])

        if not message.reply_to_message:
            await message.reply("Эта команда должна быть ответом на сообщение!")
            return

        if reply_user_id == user_id:
            await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
            return

        if perevod > 0:
            if balance >= perevod:
                await message.reply_to_message.reply(f'Вы передали {perevod2}$ игроку {reply_user_name} {rwin}',
                                                     parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
                connect.commit()

            elif int(balance) <= int(perevod):
                await message.reply(f'{user_name}, недостаточно средств! {rloser}', parse_mode='html')

        if perevod <= 0:
            await message.reply(f'{user_name}, нельзя перевести отрицательное число! {rloser}', parse_mode='html')

    if message.text.startswith("Передать"):
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        rname = msg.reply_to_message.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        perevod = int(msg.text.split()[1])
        perevod2 = '{:,}'.format(perevod)
        print(f"{name} перевел: {perevod} игроку {rname}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])

        if not message.reply_to_message:
            await message.reply("Эта команда должна быть ответом на сообщение!")
            return

        if reply_user_id == user_id:
            await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
            return

        if perevod > 0:
            if balance >= perevod:
                await message.reply_to_message.reply(f'Вы передали {perevod2}$ игроку {reply_user_name} {rwin}',
                                                     parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
                connect.commit()

            elif int(balance) <= int(perevod):
                await message.reply(f'{user_name}, недостаточно средств! {rloser}', parse_mode='html')

        if perevod <= 0:
            await message.reply(f'{user_name}, нельзя перевести отрицательное число! {rloser}', parse_mode='html')

    if message.text.startswith("дать"):
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        rname = msg.reply_to_message.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        perevod = int(msg.text.split()[1])
        perevod2 = '{:,}'.format(perevod)
        print(f"{name} перевел: {perevod} игроку {rname}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])

        if not message.reply_to_message:
            await message.reply("Эта команда должна быть ответом на сообщение!")
            return

        if reply_user_id == user_id:
            await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
            return

        if perevod > 0:
            if balance >= perevod:
                await message.reply_to_message.reply(f'Вы передали {perevod2}$ игроку {reply_user_name} {rwin}',
                                                     parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
                connect.commit()

            elif int(balance) <= int(perevod):
                await message.reply(f'{user_name}, недостаточно средств! {rloser}', parse_mode='html')

        if perevod <= 0:
            await message.reply(f'{user_name}, нельзя перевести отрицательное число! {rloser}', parse_mode='html')

    if message.text.startswith("Дать"):
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name
        rname = msg.reply_to_message.from_user.last_name
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        win = ['🙂', '😋', '😄', '🤑', '😃']
        rwin = random.choice(win)
        loser = ['😔', '😕', '😣', '😞', '😢']
        rloser = random.choice(loser)

        perevod = int(msg.text.split()[1])
        perevod2 = '{:,}'.format(perevod)
        print(f"{name} перевел: {perevod} игроку {rname}")

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        balance2 = cursor.execute("SELECT balance from users where user_id = ?",
                                  (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])

        if not message.reply_to_message:
            await message.reply("Эта команда должна быть ответом на сообщение!")
            return

        if reply_user_id == user_id:
            await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
            return

        if perevod > 0:
            if balance >= perevod:
                await message.reply_to_message.reply(f'Вы передали {perevod2}$ игроку {reply_user_name} {rwin}',
                                                     parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
                connect.commit()

            elif int(balance) <= int(perevod):
                await message.reply(f'{user_name}, недостаточно средств! {rloser}', parse_mode='html')

        if perevod <= 0:
            await message.reply(f'{user_name}, нельзя перевести отрицательное число! {rloser}', parse_mode='html')

        ###########################################ТОП###########################################
    if message.text.lower() in ["топ", "Топ"]:
        list = cursor.execute(f"SELECT * FROM users ORDER BY rating DESC").fetchmany(10)
        top_list = []
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        num = 0
        for user in list:
            if user[12] >= 999999999999999999999999:
                c6 = 999999999999999999999999
            else:
                c6 = user[12]

            if int(user[1]) < 0:
                balance3 = 0
            if int(user[1]) in range(1000, 999999):
                balance1 = user[1] / 1000
                balance2 = round(balance1)
                balance3 = f'{balance2} тыс'

            if int(user[1]) in range(1000000, 999999999):
                balance1 = user[1] / 1000000
                balance2 = round(balance1)
                balance3 = f'{balance2} млн'

            if int(user[1]) in range(1000000000, 999999999999):
                balance1 = user[1] / 1000000000
                balance2 = round(balance1)
                balance3 = f'{balance2} млрд'

            if int(user[1]) in range(1000000000000, 999999999999999):
                balance1 = user[1] / 1000000000000
                balance2 = round(balance1)
                balance3 = f'{balance2} трлн'

            if int(user[1]) in range(1000000000000000, 999999999999999999):
                balance1 = user[1] / 1000000000000000
                balance2 = round(balance1)
                balance3 = f'{balance2} квдр'

            if int(user[1]) in range(1000000000000000000, 999999999999999999999):
                balance1 = user[1] / 1000000000000000000
                balance2 = round(balance1)
                balance3 = f'{balance2} квнт'

            if int(user[1]) in range(1000000000000000000000, 999999999999999999999999):
                balance1 = user[1] / 1000000000000000000000
                balance2 = round(balance1)
                balance3 = f'{balance2} скст'
            num += 1
            c = Decimal(c6)
            c2 = '{:,}'.format(c)

            top_list.append(f"{num}. {user[9]}  — 👑{c2} | ${balance3}")
        top = "\n".join(top_list)
        await bot.send_message(message.chat.id, f"{name}, топ 10 игроков бота:\n" + top, parse_mode='html')



@dp.callback_query_handler(text='main')
async def inlinebutton(callback : types.CallbackQuery):
    await callback.message.answer(f'''
   📒 Профиль
   👑 Рейтинг
   👑 Продать рейтинг
   ⚡️ Энергия
   ⛏ Шахта
   🚗 Машины
   📱 Телефоны
   ✈️ Самолёты
   🛥 Яхты
   🚁 Вертолёты
   🏠 Дома
   💸 Б/Баланс
   📦 Инвентарь
   📊 Курс руды
   🏢 Ограбить мэрию
   💰 Банк [положить/снять] [сумма]
   🤝 Передать [сумма] [ID Игрока]
   🌐 Биткоин курс/купить/продать [кол-во]
   ⚱️ Биткоины
   💈 Ежедневный бонус
   💷 Казна
   💢 Сменить ник [новый ник]
   👨 Мой ник - узнать ник
   ⚖️ РП Команды - узнать РП команды
   💭 !Беседа - беседа бота''',parse_mode='html')
    await callback.answer()
@dp.callback_query_handler(text='games')
async def inlinebutton(callback : types.CallbackQuery):
    await callback.message.answer('''
    🎮 Спин [ставка]
   🎲 Чётное\нечётное [ставка]
   🎰 Казино [ставка]
   📦 Кейсы''')
    await callback.answer()
@dp.callback_query_handler(text='entertainment')
async def inlinebutton(callback : types.CallbackQuery):
    await callback.message.answer('🔋Купить энергию [количество]\n\nВ разработке! ❌')

@dp.callback_query_handler(text='clan')
async def inlinebutton(callback : types.CallbackQuery):
    await callback.message.answer('😕 На данный момент \'Кланы\' в разработке.')
    await callback.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



