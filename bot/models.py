from django.db import models

# Create your models here.
from django.utils import timezone


class BotUser(models.Model):
    chat_id = models.IntegerField()
    is_active = models.BooleanField(default=True)

    send_notification_about_check = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def change_notification_status(self):
        if self.send_notification_about_check:
            self.send_notification_about_check = False
        else:
            self.send_notification_about_check = True
        self.save()


class Check(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
