from django.db import models
from customuser.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, blank=True, null=True, verbose_name='Пользователи',
                                    related_name='chatusers')
    isNewMessages = models.BooleanField('Есть новые сообщения', default=False)
    lastMessageOwn = models.BooleanField( default=False)
    lastMsgBy = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Сообщение от')
    createdAt = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, blank=False, null=True, on_delete=models.CASCADE, verbose_name='В чате')
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Сообщение от')
    message = models.TextField('Сообщение', blank=True,null=True)
    isUnread = models.BooleanField('Не прочитанное сообщение', default=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.isUnread:
            self.chat.isNewMessages = True
            self.chat.save()
        super(Message, self).save(*args, **kwargs)