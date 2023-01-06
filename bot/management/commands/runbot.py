from django.conf import settings
from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message


class Command(BaseCommand):
    help = "Run Telegram bot"
    offset = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **kwargs):
        while True:
            response = self.tg_client.get_updates(offset=self.offset)

            for item in response.result:
                self.offset = item.update_id + 1
                if hasattr(item, "message"):
                    self.handle_message(item.message)
                    continue

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.from_.id,
            tg_chat_id=msg.chat.id,
        )

        if created:
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Подтвердите, пожалуйста, аккаунт.\n"
                     f"введите проверочный код:\n\n"
                     f"{tg_user.verification_code}на сайте\n\n"
            )

        elif not tg_user.user:
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                tg_user.tg_chat_id,
                f'Для дальнейшей работы подтвердите, пожалуйста, аккаунт. '
                f'Необходимо ввести проверочный код: '
                f'{tg_user.verification_code}'
            )
