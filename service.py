from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_posts_keyboard(posts_list):
    posts_markup = InlineKeyboardMarkup()

    loop_iterations = 4 if len(posts_list) / 2 > 4 else int(len(posts_list) / 2)

    for i in range(0, loop_iterations, 2):

        posts_markup.add(InlineKeyboardButton(text=posts_list[i].title, callback_data=posts_list[i].id),
                         InlineKeyboardButton(text=posts_list[i+1].title, callback_data=posts_list[i+1].id)
                         )

    if loop_iterations % 2 == 1:
        posts_markup.add(InlineKeyboardButton(text=posts_list[loop_iterations+1].title,
                                              callback_data=posts_list[loop_iterations+1].id)
                         )
    return posts_markup


def post_detail(posts_list, callback_data):
    answer = "Error"
    for post in posts_list:
        if str(post.id) == callback_data:
            answer = f"*Title*: {post.title}\n" \
                     + f"👤: {post.author.first_name}\n" \
                     + f"🕚: {post.created}\n" \
                       f"*Comments*:\n"
            for comment in post.comments:
                answer += f"   *{comment.author}*: {comment.body}"
            break

    return answer
