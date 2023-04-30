import logging

from telegram import Update, ForceReply, Dispatcher
from telegram.ext import ExtBot, CommandHandler, MessageHandler, filters, CallbackContext


from config import telegram_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def main() -> None:
    bot = ExtBot(telegram_token)
    dispatcher = Dispatcher(bot)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, echo))

    dispatcher.start_polling()
    dispatcher.idle()

if __name__ == '__main__':
    main()
