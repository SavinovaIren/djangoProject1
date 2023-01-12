from django.conf import settings

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bot.models import TgUser

from .tg.client import TgClient


class BotVerificationView(generics.UpdateAPIView):
    queryset = TgUser.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        verif_code = self.request.data.get("verification_code")

        if not verif_code:
            raise ValidationError({"Указан неверный код проверки."})

        try:
            tg_user = self.get_queryset().get(verification_code=verif_code)
        except TgUser.DoesNotExist:
            raise ValidationError({"Пользователя с введенным кодом не существует."})

        tg_user.user = self.request.user
        tg_user.save()
        TgClient(token=settings.BOT_TOKEN).send_message(chat_id=tg_user.tg_chat_id, text=f"Ваш аккаунт подтвержден.")
        return Response(data=verif_code, status=status.HTTP_201_CREATED)
