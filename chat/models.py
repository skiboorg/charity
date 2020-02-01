from django.db import models
from customuser.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, blank=True, null=True, verbose_name='Пользователи',
                                    related_name='chatusers')
    createdAt = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, blank=False, null=True, on_delete=models.CASCADE, verbose_name='В чате')
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Сообщение от')
    message = models.TextField('Сообщение', blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)