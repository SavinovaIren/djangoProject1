from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TgUser
from .serializers import TgUserSerializer
from .tg.client import TgClient


# Create your views here
class BotVerifyView(generics.UpdateAPIView):
    model = TgUser
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class(request.data).data
        tg_client = TgClient('5717472826:AAFhRnkZGDl2ChzbR9qiooGEDFW8-fTefWg')
        tg_user = TgUser.objects.filter(verification_code=data['verification_code']).first()
        if not tg_user:
            raise Exception
        tg_user.user = request.user
        tg_user.save()
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text='Успешно!')
        return Response(data=data)
