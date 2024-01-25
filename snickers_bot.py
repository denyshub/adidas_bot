import json
import time
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.utils.markdown import hlink
from main import get_page

# Initialize the bot and dispatcher
bot = Bot(token="6532612576:AAHsLqp5atDsdntNfmOpRlSs3AXe0PozcjY", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Variables to store user data
user_data = {}

# Function to split a list into chunks
def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Function to check if a string can be converted to a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

@dp.message_handler(commands='start')
async def send_hello(message: types.Message):
    # Create a custom keyboard with buttons
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("чоловічі кросівки"))
    keyboard.add(types.KeyboardButton("жіночі кросівки"))

    # Send the message with the custom keyboard
    await message.answer("Оберіть тип взуття:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["чоловічі кросівки", "жіночі кросівки"])
async def choose_shoes_type(message: types.Message):
    # Store the selected type in the 'sex' variable
    user_data['sex'] = message.text.lower()

    # Ask for the size
    await message.answer(f"Ви обрали {user_data['sex']}. Тепер введіть розмір:")

@dp.message_handler(lambda message: is_float(message.text.replace(',','.')))
async def choose_shoes_size(message: types.Message):
    # Store the selected size in the 'size' variable
    user_data['size'] = message.text.replace('.', '-').replace(',', '-')
    await message.answer(f"Ви обрали розмір {user_data['size']}. Дякуємо за вибір!")

    # Perform the action with the user's choices
    get_page(user_data['sex'], user_data['size'])
    with open("adidas_snickers.json") as file:
        data = json.load(file)

    chunk_size = 10
    delay_between_messages = 5  # Set the delay between messages in seconds
    await message.answer(f"Кількість результатів: {len(data)}")
    for chunk in chunks(data, chunk_size):
        for snickers in chunk:
            card = (
                f"{hlink(snickers.get('product name'), snickers.get('link'))}\n"
                f"<b>{snickers.get('sale price')}</b>\n"
                f"<b>{snickers.get('sale %').strip()}</b>\n"
            )
            await message.answer(card)
        time.sleep(delay_between_messages)

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
