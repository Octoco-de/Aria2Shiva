import math

from src.yts import search, get_movie_details
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.utils import constrain_text_to_length, shorten_link


# Create a movie button for the inline keyboard
def movie_button(movie):
    return [
        InlineKeyboardButton(
            text=movie['title'],
            callback_data=f"userselectedmovie:{movie['id']}",
        )
    ]

# Create a torrent button for the inline keyboard
def torrent_button(torrent):
    size = torrent['size'].upper()
    if " MB" in size:
        size = size.replace(" MB", "")
        size = f"{math.ceil(float(size))} MB"
    return InlineKeyboardButton(text=f"{torrent['quality']} {size}", callback_data=torrent['shortLink'])



# Create a summary button for the inline keyboard
def summary_button(movie_id):
    return InlineKeyboardButton(text="Full Summary", callback_data=f"SUM: {movie_id}")

# Create a site button for the inline keyboard
def site_button(movie_data):
    return InlineKeyboardButton(text="Open Yts", url=movie_data['url'])

# Search for a movie using the provided query
async def search_movie(update, context, chat_id, query):
    try:
        movies = await search(query)
        print(f'yts response: {movies}')
        if not movies:
            await context.bot.send_message(chat_id, "Ain't Nobody Here but Us Chickens")
        else:
            buttons = [movie_button(movie) for movie in movies]
            await context.bot.send_message(chat_id, 'This is what I found for you 👀', reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        print(f"Error in search_movie: {e}")
        await context.bot.send_message(chat_id, 'Well this is embarrassing...')


# Handle the user's movie selection and display movie details and download options
async def user_selected_movie(update, context, chat_id, movie_id):
    try:
        movie_data = await get_movie_details(movie_id)
        temp_array = []
        buttons = []

        torrents = movie_data['torrents']

        for torrent in torrents:
            if torrent['url']:  # Check if torrent URL is not empty
                short_link = await shorten_link(torrent['url'])
                if short_link:  # Check if there is a short link
                    torrent['shortLink'] = short_link
                    temp_array.append(torrent_button(torrent))
                    if len(temp_array) == 2:
                        buttons.append(temp_array)
                        temp_array = []

        if len(temp_array) > 0:
            buttons.append(temp_array)

        # Append both buttons as a list to create a single row
        buttons.append([summary_button(movie_id), site_button(movie_data)])

        caption = movie_data['title']

        if movie_data['summary']:
            summary = await constrain_text_to_length(movie_data['summary'], 150)
            caption = f"{caption}\n\n`{summary}`"

        await context.bot.send_photo(
            chat_id,
            movie_data['image'],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as error:
        print(f"Error while handling user_selected_movie: {error}")
        await context.bot.send_message(chat_id, 'Well this is embarrassing....')





# Display the full movie summary for the selected movie
async def display_summary(update, context, chat_id, movie_id):
    try:
        movie_data = await get_movie_details(movie_id)
        await context.bot.send_message(chat_id, f"`{movie_data['summary']}`", parse_mode="Markdown")
    except Exception:
        await context.bot.send_message(chat_id, 'Well this is embarrassing....')


# Download the selected movie using the provided torrent URL
def download_yts_movie(context, chat_id, url):
    # Aria2Module.download_torrent(context.bot, chat_id, url)
    print('aria2')

# Handle button callbacks from the inline keyboard
def button_handler(update, context):
    button_data = update.callback_query.data

    if 'movie: ' in button_data:
        user_selected_movie(update, context, update.callback_query.from_user.id, button_data.replace('movie: ', ''))
    elif 'SUM: ' in button_data:
        display_summary(update, context, update.callback_query.from_user.id, button_data.replace('SUM: ', ''))
    else:
        download_yts_movie(context, update.callback_query.from_user.id, 'https://bit.ly/' + button_data)


