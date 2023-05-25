import schedule
import time
import requests
from django.core.management import BaseCommand
from bot.models import Check
from bot.utils import broadcast_per_new, broadcast_per_request


def job():
    req = requests.get(
        'https://portale.unipv.it/it/didattica/corsi-di-laurea/corsi-di-laurea-triennale-e-magistrali-a-ciclo-unico'
        '/artificial'
    )
    if 'Pagina non trovata' in req.text:
        Check.objects.create()
        broadcast_per_request()
    else:
        broadcast_per_new()


schedule.every(1).minutes.do(job)


class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **options):
        job()
        while True:
            schedule.run_pending()
            time.sleep(1)
