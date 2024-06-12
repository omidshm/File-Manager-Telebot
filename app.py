import asyncio
import os
import pathlib
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
import telebot
from modules import file_utils

load_dotenv("config.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUDO_ID = os.getenv("SUDO_ID")

bot = AsyncTeleBot(BOT_TOKEN)

@bot.callback_query_handler(func=lambda call:True)
async def callback(call: telebot.types.CallbackQuery):
    chat_id = call.message.chat.id
    if call.data[:5] == "file:":
        file_name = call.data[5:]
        file_markup = telebot.types.InlineKeyboardMarkup()
        upload_btn = telebot.types.InlineKeyboardButton(str("Upload New"), callback_data=f"write:{file_name}")
        get_btn = telebot.types.InlineKeyboardButton(str("Download"), callback_data=f"read:{file_name}")
        
        file_markup.add(upload_btn)
        file_markup.add(get_btn)
        
        text = file_name
        await bot.send_message(chat_id, text, reply_markup=file_markup)
        #await bot.send_message(call.message.chat.id, f"You select a {file_name} to download")
    if call.data[:5] == "read:":
        file_name = call.data[5:]
        
        await bot.send_document(
            chat_id,
            telebot.types.InputFile(pathlib.Path(file_name))
        )
        
    if call.data[:6] == "write:":
        context_file_name = call.data[6:]
        await bot.send_message(chat_id, f"Now Upload your new {context_file_name}")


@bot.message_handler(content_types=['document'])
async def handle_document(message:telebot.types.Message):
    file_info = await bot.get_file(message.document.file_id)

    downloaded_file = await bot.download_file(file_info.file_path)
    file_name = message.document.file_name
    
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
# Handle '/start' and '/help'
@bot.message_handler(commands=['list'])
async def list_files(message:telebot.types.Message):
    
    list_files = file_utils.list_files_in_folder(".", ".txt")
    files_markup = telebot.types.InlineKeyboardMarkup()
    for _ in list_files:
        btn = telebot.types.InlineKeyboardButton(str(_), callback_data=f"file:{_}")
        
        files_markup.add(btn)
        
    # بتونه تموم فایل های موجود رو به صورت دکمه شیشه ای ببینه
    text = 'List of files in folder 1:'
    await bot.send_message(message.chat.id, text, reply_markup=files_markup)


@bot.message_handler(commands=['start'])
async def welcome(message:telebot.types.Message):    
    
    text = 'Hi bitch'
    await bot.send_message(message.chat.id, text)
    
def get_file():
    # با انتخاب کیبورد شیشه ای فایل مورد نظر رو دریافت کنه
    ...
    
def write_to_the_file():
    # بتونه با ارسال فایل تو یک فایل دیگه بنویسه
    ...
    
    
asyncio.run(bot.polling())