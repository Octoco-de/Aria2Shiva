import math
import subprocess
import os
import shlex
import hashlib

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from pathlib import Path

from src.yts import search, get_movie_details
from src.utils import constrain_text_to_length 



# Create a movie button for the inline keyboard
def movie_button(movie):
    return [
        InlineKeyboardButton(
            text=movie['title'],
            callback_data=f"userselectedmovie:{movie['id']}",
        )
    ]

# Create a torrent button for the inline keyboard
def torrent_button(torrent, movie_id, index):
    size = torrent['size'].upper()
    if " MB" in size:
        size = size.replace(" MB", "")
        size = f"{math.ceil(float(size))} MB"
    return InlineKeyboardButton(text=f"{torrent['quality']} {size}", callback_data=f"dowM:{movie_id}:{index}")



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


async def user_selected_movie(update, context, chat_id, movie_id):
    try:
        context.user_data["selected_movie_id"] = movie_id
        movie_data = await get_movie_details(movie_id) # Store the movie_id in user_data
        temp_array = []
        buttons = []

        torrents = movie_data['torrents']

        for index, torrent in enumerate(torrents):
            if torrent['url']:  # Check if torrent URL is not empty
                temp_array.append(torrent_button(torrent, movie_id, index))
                if len(temp_array) == 2:
                    buttons.append(temp_array)
                    temp_array = []

        if len(temp_array) > 0:
            buttons.append(temp_array)

        # Append context.both buttons as a list to create a single row
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
    print(f"display_summary {movie_id}")
    try:
        print(f'movie id {movie_id}')
        movie_data = await get_movie_details(movie_id)
        await context.bot.send_message(chat_id, f"`{movie_data['summary']}`", parse_mode="Markdown")
    except Exception:
        await context.bot.send_message(chat_id, 'Well this is embarrassing....')





# Function to check if tmux is running
def is_tmux_running():
    try:
        subprocess.check_output(['tmux', 'ls'], stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        if "error connecting" in str(e.stderr) or "no server running" in str(e.stderr):
            return False
        return True

# Download the selected movie using the provided torrent URL
async def download_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id, url):
    try:
        # Check if tmux is running, and start it if it isn't
        created_new_session = False
        if not is_tmux_running():
            created_new_session = True
            subprocess.run(['tmux', 'new-session', '-d', '-s', 'mysession'], check=True)
            

        session_id = hashlib.md5(url.encode()).hexdigest()
        tmux_session_name = f"Aria2Shiva-{session_id}"

        # Check if there is an existing session with the same name
        existing_sessions_output = subprocess.check_output(['tmux', 'list-sessions']).decode()
        if tmux_session_name in existing_sessions_output:
            await context.bot.send_message(chat_id, "This download has already started!")
            return

        tmux_cmd = ['tmux', 'new-session', '-d', '-s', tmux_session_name]
        subprocess.run(tmux_cmd, check=True)

        download_directory = os.path.expanduser('~/Torrents')

        aria2c_cmd = [
            'aria2c', url, '-d', download_directory, '-s', '16', '-x', '16', '-k', '1M', '-c', '--seed-time=0'
        ]

        # Execute the aria2c command and close the tmux session when the process is done
        tmux_send_keys_cmd = ['tmux', 'send-keys', '-t', tmux_session_name, ' '.join(aria2c_cmd), 'C-m', ';']
        subprocess.run(tmux_send_keys_cmd, check=True)

        # Kill mysession if it was used to start the server
        if created_new_session:
            subprocess.run(['tmux', 'kill-session', '-t', 'mysession'], check=True)

        await context.bot.send_message(chat_id, "The download has started!")
    except subprocess.CalledProcessError as e:
        print(f"Error starting tmux or aria2c: {e}")
        await context.bot.send_message(chat_id, "Oops! There was an error starting the download. Please try again later.")
    except Exception as e:
        print(f"Unknown error: {e}")
        await context.bot.send_message(chat_id, "Oops! Something went wrong. Please try again later.")






# Handle button callbacks from the inline keyboard
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id

    print(f'querty data {data}')

    if data.startswith("userselectedmovie:"):
        movie_id = data.split(':')[1]
        context.user_data['selected_movie_id'] = movie_id
        print(f'userselectedmovie movie id {movie_id}')
        await user_selected_movie(update, context, chat_id, movie_id)
    elif 'SUM:' in data:
        movie_id = data.split(':')[1]
        movie_data = await get_movie_details(movie_id)
        summary = movie_data['summary'] or "No summary available."
        await context.bot.send_message(chat_id, f"`{summary}`", parse_mode="Markdown")
    elif 'dowM:' in data:
        _, movie_id, torrent_index = data.split(':')
        torrent_index = int(torrent_index)
        movie_data = await get_movie_details(movie_id)
        torrent_url = movie_data['torrents'][torrent_index]['url']
        await download_torrent(update, context, chat_id, torrent_url)
    else:
        await context.bot.send_message(chat_id, "Unknown command. Please try again.")


    

    
        
    
    





