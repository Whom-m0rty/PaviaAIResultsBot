from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request

from bot.models import BotUser, Check

requests = Request(
    connect_timeout=0.5,
    read_timeout=1.0,
)

bot = Bot(
    request=requests,
    token=settings.TELEGRAM_BOT_TOKEN,
)


class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **options):
        updater = Updater(
            bot=bot,
            use_context=True
        )
        print(f'@{bot.get_me().username}')

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CommandHandler('change_notifications', change_notifications))
        updater.dispatcher.add_handler(CommandHandler('profile', start))

        updater.start_polling()
        updater.idle()


def __notification_status(user: BotUser):
    return 'Web page change & per request' if user.send_notification_about_check else 'Only web page change'


def __get_time_as_string(time):
    hours = time.hour
    if len(str(hours)) == 1:
        hours = f'0{hours}'

    minutes = time.minute
    if len(str(minutes)) == 1:
        minutes = f'0{minutes}'

    return f'{hours}:{minutes}'


def start(update: Update, context):
    user, _ = BotUser.objects.get_or_create(
        chat_id=update.effective_chat.id,
    )

    last_check = Check.objects.last().created_at
    # last_check = timezone.now()

    update.message.reply_text(
        text=f"""<b>Welcome to AI Pavia bot!</b>

This bot will check web page unipv every minute. 
Bot will send notification if it will be something new!        

Last check web page was at: {last_check.date()} {__get_time_as_string(last_check)} {last_check.tzinfo}

Your notification status: <b>{__notification_status(user)}</b>
""", parse_mode='HTML'
    )


def change_notifications(update: Update, context):
    user, _ = BotUser.objects.get_or_create(
        chat_id=update.effective_chat.id,
    )
    user.change_notification_status()

    update.message.reply_text(
        f"""Successfully changed your notification status to: <b>{__notification_status(user)}</b>""",
        parse_mode='HTML'
    )
