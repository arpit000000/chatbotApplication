import os
import logging
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TOKEN = os.getenv("TOKEN")

# Ensure API key is set
if not GEMINI_API_KEY:
    raise ValueError("🚨 ERROR: Gemini API key is missing! Set it in the .env file.")

if not TOKEN:
    raise ValueError("🚨 ERROR: Telegram bot token is missing! Set it in the .env file.")

# Initialize Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Bot and Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

class Reference:
    """A class to store previous response from the Gemini API"""
    def __init__(self) -> None:
        self.response = ""

reference = Reference()

# Clear previous conversation
def clear_past():
    reference.response = ""

# Command Handlers
@dp.message(Command("start"))
async def welcome(message: Message):
    await message.answer("Hi\nI am Tele Bot!\nNow powered by Google Gemini! 🤖 How can I assist you?")

@dp.message(Command("clear"))
async def clear(message: Message):
    clear_past()
    await message.answer("I've cleared the past conversation and context.")

@dp.message(Command("help"))
async def helper(message: Message):
    help_command = (
        "Hi there, I'm a Telegram bot powered by Google Gemini! \n"
        "Please follow these commands:\n"
        "✅ /start - Start the conversation\n"
        "✅ /clear - Clear past conversation and context\n"
        "✅ /help - Get this help menu\n\n"
        "I hope this helps! 😊"
    )
    await message.answer(help_command)

# Gemini Message Handler
@dp.message()
async def chat_with_gemini(message: Message, state: FSMContext):
    print(f">>> USER: {message.text}")
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Using Gemini Pro
        response = model.generate_content([reference.response, message.text])
        
        reference.response = response.text
        print(f">>> Gemini: {reference.response}")
        
        await message.answer(reference.response)
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("Oops! Something went wrong. Please try again later.")

# Run the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
