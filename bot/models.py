from django.db import models
import string
import random


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name="id чата")
    tg_user_id = models.BigIntegerField(verbose_name="id пользователя", unique=True)
    user = models.ForeignKey('core.User',
                             verbose_name="Пользователь приложения",
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE
                             )
    verification_code = models.CharField(verbose_name="Код верификации",
                                         max_length=6,
                                         unique=True,
                                         null=True,
                                         blank=True
                                         )

    class Meta:
        verbose_name = "Пользователь Tlgrm"
        verbose_name_plural = "Пользователи Tlgrm"

    def generate_verification_code(self):
        code = string.digits + string.ascii_letters
        verification_code = ''

        for _ in range(6):
            verification_code += code[random.randrange(0, len(code))]

        self.verification_code = verification_code
        self.save()

