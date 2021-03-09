import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from parser import Post
from service import get_posts_keyboard, post_detail
import config

import requests

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

posts_list = []


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    markup = ReplyKeyboardMarkup([[KeyboardButton(text="Posts")]], one_time_keyboard=True)
    await message.answer(text="Hello\nClick on the button to view all posts", reply_markup=markup)


@dp.message_handler()
async def some_message(message: types.Message):

    if message.text == "Posts":
        posts = requests.get(config.POST_API)
        global posts_list
        posts_list = [Post(post) for post in posts.json()["results"]]
        posts_markup = get_posts_keyboard(posts_list)

        await message.answer(text="Select to view post.", reply_markup=posts_markup)
    else:
        markup = ReplyKeyboardMarkup([[KeyboardButton(text="Posts")]], one_time_keyboard=True)
        await message.answer(text="Click on the button to view all posts", reply_markup=markup)


@dp.callback_query_handler()
async def callback_handler(callback: types.CallbackQuery):
    #answer = post_detail(posts_list, callback.data)
    if callback.data.startswith("like"):
        user_id = int(callback.data.split(" ")[1])
        post_id = int(callback.data.split(" ")[2])

        request = 0

        for post in posts_list:
            if post.id == post_id:
                request = post.like(user_id)
                break

        likes_data = request.json()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f"❤️{likes_data['likes']}", callback_data=callback.data))
        markup.add(InlineKeyboardButton(text="URL", url=f"{config.HOST}/{post.slug}"))
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)
        await callback.answer(str(likes_data['status']))

    else:
        markup = InlineKeyboardMarkup()
        answer = "Error"
        for post in posts_list:
            if str(post.id) == callback.data:
                answer = f"*Title*: {post.title}\n" \
                         + f"👤: {post.author.first_name}\n" \
                         + f"🕚: {post.created}\n" \
                           f"*Comments*:\n"
                for comment in post.comments:
                    answer += f"  *{comment.author}*: {comment.body}"

                markup.add(InlineKeyboardButton(text=f"❤️{post.like_count}", callback_data=f"like {callback.from_user.id} {post.id}"))
                markup.add(InlineKeyboardButton(text="URL", url=f"{config.HOST}/{post.slug}"))
                break

        await bot.send_message(chat_id=callback.message.chat.id, text=answer, parse_mode=types.ParseMode.MARKDOWN, reply_markup=markup)
        await callback.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
