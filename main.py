import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot(
    "6488484967:AAEb6bYZyeogekUOvKmfks4W3A71hlqwWqw",
    state_storage=state_storage,
    parse_mode="Markdown",
)


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Поиск шуток"  # Можно менять текст
text_button_1 = "Анекдоты"  # Можно менять текст
text_button_2 = "Смешные истории"  # Можно менять текст
text_button_3 = "Интересные видео"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    ),
)


@bot.message_handler(state="*", commands=["start"])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        "Приветик! Что тебе показать?",  # Можно менять текст
        reply_markup=menu_keyboard,
    )


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(
        message.chat.id, "Введите ключевое слово для поиска анекдота:"
    )  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    bot.send_message(
        message.chat.id, "Отличный выбор! Введите количество нужных анекдотов:"
    )  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["age"] = message.text
    bot.send_message(
        message.chat.id,
        "Вот что я нашел: `lorem ipsum blablabla`",
        reply_markup=menu_keyboard,
    )  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(
        message.chat.id, "`Какая-то шутка`", reply_markup=menu_keyboard
    )  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(
        message.chat.id,
        "`Какая-то ну ооочень смешная и интересная история`",
        reply_markup=menu_keyboard,
    )  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(
        message.chat.id,
        "[Посмотри это видео](https://www.youtube.com/watch?v=6dDQaDu7YpE)",
        reply_markup=menu_keyboard,
    )  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
