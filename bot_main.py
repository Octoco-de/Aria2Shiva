import logging
import time
import re
from config import telegram_token, allowedIDs
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update, InputMediaAnimation
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
)

# Import the action functions from actions.py
from src.actions import button_callback, search_movie, download_torrent

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

allowed_chat_ids = {chat_id: {"password": password, "last_login": 0} for chat_id, password in allowedIDs.items()}

async def check_user_permission(update: Update) -> bool:
    chat_id = update.effective_chat.id
    user_allowed = chat_id in allowed_chat_ids

    if user_allowed:
        last_login = allowed_chat_ids[chat_id]["last_login"]
        current_time = time.time()
        if current_time - last_login > 8 * 60 * 60:  # 8 hours in seconds
            await update.message.reply_text("Speak, friend, and enter")
            return False
        return True
    else:
        await update.message.reply_animation("https://media.giphy.com/media/njYrp176NQsHS/giphy.gif")
        return False


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_user_permission(update):
        return

    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_user_permission(update):
        return

    await update.message.reply_text("Help!")

async def textHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    
    message_text = update.message.text
    if chat_id in allowed_chat_ids and allowed_chat_ids[chat_id]["password"] == message_text:
        allowed_chat_ids[chat_id]["last_login"] = time.time()
        await update.message.reply_animation("https://szeged365.hu/wp-content/uploads/2020/12/lotr-door-.gif")
        return

    if not await check_user_permission(update):
        return

    message_text = update.message.text
    magnet_or_torrent = re.search(r"(magnet:\?xt=urn:btih:[a-zA-Z0-9]+)|(https?://.*\.(torrent))", message_text)

    if magnet_or_torrent:
        context.args = [message_text]
        await download_command(update, context)
    else:
        await update.message.reply_text(message_text)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_user_permission(update):
        return

    chat_id = update.effective_chat.id
    query = ' '.join(context.args)
    if query:
        await search_movie(update, context, chat_id, query)
    else:
        await update.message.reply_text("Please provide a movie title to search for.")

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_user_permission(update):
        return

    chat_id = update.effective_chat.id
    torrent_url = ' '.join(context.args)
    if torrent_url:
        await download_torrent(update, context, chat_id, torrent_url)
    else:
        await update.message.reply_text("Please provide a torrent URL or a magnet link to download.")

async def password_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    password = update.message.text
    if chat_id in allowed_chat_ids and allowed_chat_ids[chat_id]["password"] == password:
        allowed_chat_ids[chat_id]["last_login"] = time.time()
        await update.message.reply_text("Welcome!")
    else:
        await update.message.reply_text("Incorrect password.")

async def who_am_i(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"{chat_id}")



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegram_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("download", download_command))
    application.add_handler(CommandHandler("password", password_check))
    application.add_handler(CommandHandler("whoami", who_am_i))

    application.add_handler(CallbackQueryHandler(button_callback))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, textHandler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
