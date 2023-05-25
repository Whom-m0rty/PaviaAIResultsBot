from .management.commands.bot import bot
from .models import BotUser


def _broadcast_message(text: str, users, disable_notification=True):
    for user in users:
        try:
            bot.send_message(
                chat_id=user.chat_id,
                text=text,
                disable_notification=disable_notification
            )
        except:
            pass


def broadcast_per_request():
    text = '''Nothing was changed :('''
    users = BotUser.objects.filter(is_active=True, send_notification_about_check=True)
    _broadcast_message(text, users)


def broadcast_per_new():
    text = 'SMTH WAS CHANGED!!! \n\nhttps://portale.unipv.it/it/didattica/corsi-di-laurea/corsi-di-laurea-triennale-e' \
           '-magistrali-a-ciclo-unico/artificial'
    users = BotUser.objects.filter(is_active=True)
    _broadcast_message(text, users, disable_notification=False)
