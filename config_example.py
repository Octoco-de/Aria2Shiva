# This is a demo configuration file for a Telegram bot that downloads torrents.

# To use this file, copy it and save it as "config.py". Then, fill in the values
# below with your own Telegram bot token, chat IDs, and download directory.

# Your Telegram bot token, which you can get from the BotFather.
telegram_token = 'ENTER YOUR TELEGRAM TOKEN HERE'

# A dictionary of allowed chat IDs and their associated passwords.
# Use this format: { 'CHAT_ID': 'PASSWORD' }
allowedIDs = {
    'CHAT_ID_1': 'PASSWORD_FOR_CHAT_1',
    'CHAT_ID_2': 'PASSWORD_FOR_CHAT_2'
}

# The directory where downloaded torrents should be saved.
download_directory = '~/Torrents'
