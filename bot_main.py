import logging
from bot_list import sqlite_3_select, Rates
from exchange import Exchange
from keyboard import *
from get_diagram import Diagram

logging.basicConfig(level=logging.INFO)
bot = Bot(token='1617603896:AAHUmL3ufG8yvRG2RNJe1944zovFxKux4y8')
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Hi, I'm a bot, I have the following features available:\n/list\n/exchange"
                                      "\n/getdiagram")


@dp.message_handler(commands=['list'])
async def lst(message: types.Message):
    await message.reply('To view the exchange rate, select it from the panel', reply_markup=keyboard,
                        reply=False)


@dp.callback_query_handler(text_contains='1')
async def get_rates(call: types.callback_query):
    sqlite_3_select(call.data.replace('1', ''))
    answer_message = Rates.get_rates()
    await bot.send_message(call.message.chat.id,'\n'.join(map(str, answer_message)))


@dp.message_handler(commands=['exchange'])
async def exchange(message: types.Message):
    await message.reply('Enter the amount of currency to exchange', reply=False)


@dp.message_handler(commands=['getdiagram'])
async def get_diagram(message: types.Message):
    await message.reply('To get diagram select the base currency', reply=False, reply_markup=keyboard4)


@dp.message_handler()
async def exchange_amount(message: types.Message):

    try:
        float(message.text)
    except:
        await message.reply('The entered value must be numeric, please try again', reply=False)
    else:
        Exchange.put_numeric(message.text)
        await message.reply('To exchange select the base currency', reply=False, reply_markup=keyboard2)


@dp.callback_query_handler(text_contains='2')
async def base_currently(call: types.callback_query):
    Exchange.request(call.data.replace('2', ''))
    await bot.send_message(call.message.chat.id,'Select the currency to which the transfer will be made',
                           reply_markup=keyboard3)


@dp.callback_query_handler(text_contains='3')
async def transfer_base(call: types.callback_query):
    Exchange.put_transfer_base(call.data.replace('3',''))
    answer_message = Exchange.get_exchange_data()
    await bot.send_message(call.message.chat.id, '\n'.join(map(str, answer_message)))


@dp.callback_query_handler(text_contains='4')
async def diagram_base(call: types.callback_query):
    Diagram.put_base(call.data.replace('4', ''))
    await bot.send_message(call.message.chat.id, 'To get diagram select the second currency',
                           reply_markup=keyboard5)


@dp.callback_query_handler(text_contains='5')
async def diagram_base(call: types.callback_query):
    Diagram.put_transfer(call.data.replace('5', ''))
    Diagram.request()
    await bot.send_photo(call.message.chat.id, photo=open('diagrams/{}.png'.format(call.data.replace('5', '')), 'rb'))
    Diagram.dell_diagram()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
