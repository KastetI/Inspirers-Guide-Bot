import asyncio
import aiohttp
import logging
import json 
import sys
from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties

from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

TOKEN = "6426210653:AAEli4fk64tBTTF6NyX4c3qAWkBA--gDPVs"
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

keyboard_markup = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Каталог лекций"), types.KeyboardButton(text="Поделиться мечтой!")], 
    [types.KeyboardButton(text="Ближайшее мероприятие"), types.KeyboardButton(text="Мини-игра")]
])

class functions(StatesGroup):
    catalog = State()
    event = State()
    share_dream = State()
    game = State()

class Lecture():
    def __init__(self, id:int, lecture_name:str, video_path:str, lecturer:str=None, lecturer_about:str=None, ) -> None:
        self.lecture_name = lecture_name
        self.video_path = video_path
        self.lecturer = lecturer
        self.lecturer_about = lecturer_about
        
event = {"date" : "20 июня 2024г",
    "name" : "Вдохновляем в Липецке",
    "place" : "город Липецк", 
    "about" : "Сбор Вдохновителей, которого все так ждали! С фотозоной, активностями и экспертами",
    "photo_path" : "C:\\Users\\Main\\Desktop\\Coding\\inspirersGuideBot\\Post.jpg" 
    }

@dp.message(Command(commands="start"), StateFilter(None))
async def start(msg: Message):
    await msg.answer(
f"""Привет, {msg.from_user.first_name}! Я твой помощник от движения \"Вдохновители\". 
У меня множество функций, например, могу рассказать о ближайшем мероприятии или показать тебе лекции экспертов!""", 
    reply_markup=keyboard_markup)


@dp.message(StateFilter(None))
async def choose(msg: Message, state: FSMContext):
    if msg.text.lower() == "каталог лекций":
        await state.set_state(functions.catalog)
        catalog = await load_catalog()
        buttons = [[types.InlineKeyboardButton(text=lec.lecture_name, callback_data=lec.video_path)] for lec in catalog]
        markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        text ="🎥 Записали для вас несколько лекций:\n"
        for i, lecture in enumerate(catalog):
            text += f" {i+1}: «{lecture.lecture_name}». {lecture.lecturer} — {lecture.lecturer_about}.\n"
        f = types.FSInputFile("Record.png")
        await msg.answer_photo(f, text, reply_markup=markup)
        await state.set_state(None)
        
    if msg.text.lower() in ("поделиться мечтой!", "поделиться мечтой") :
        pass
    if msg.text.lower() == "ближайшее мероприятие":
        event = await load_event()
        photo = types.FSInputFile(event["photo_path"])
        text =f"💫{event['name']}\n📌Место проведения: {event['place']}\n🗓Дата проведения: {event['date']}\n\n{event['about']}"
        await msg.answer_photo(photo=photo, caption=text)
    if msg.text.lower() in ("мини-игра", "мини игра"):
        pass

@dp.callback_query()
async def callback(call: CallbackQuery):
    path = call.data
    video = types.FSInputFile(path)
    await call.message.answer_video(video, caption="Приятного просмотра!")
    
async def load_event():
    f = open("event.json", "r")
    json_event = f.read()
    f.close()
    event = json.loads(json_event)
    return event
    

async def load_catalog():
    catalog = [
    Lecture(0, "Твой первый стартап!", "C:\\Users\\Main\\Downloads\\Lecture1.MP4", "Олег Тарасов", "Создатель стартапа «ЕГЭПРОРЫВ»"),
    Lecture(1, "О киберспорте", "C:\\Users\\Main\\Downloads\\Lecture2.MP4", "Ратибор Попов", "Основатель и президент Ассоциации компьютерного спорта"),
    Lecture(2, "Вдохновители", "C:\\Users\\Main\\Downloads\\Lecture3.MP4", "Алексей Чумаков", "Руководитель Всероссийского движения «Вдохновители»")
    ]
    return catalog 


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())