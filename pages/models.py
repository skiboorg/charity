from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify
from random import choices
import string

class Banner(models.Model):
    image = models.ImageField('Изображение категории', upload_to='img/', blank=True)
    url = models.CharField('Ссылка', max_length=255,blank=True)

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"


class Fond(models.Model):
    name = models.CharField('Название фонда', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    deviz = models.CharField('Девиз', max_length=255, blank=False, null=True, db_index=True)
    image = models.ImageField('Лого фонда (225x110)', upload_to='fond/', blank=True)
    icon = models.ImageField('Иконка для главной', upload_to='fond/', blank=True)
    image_big = models.ImageField('Картинка на страницу фонда (1240х600)', upload_to='fond/', blank=True)
    description_short = RichTextUploadingField('Описание для окна покупки', blank=False, null=True)
    description_full = RichTextUploadingField('Полное описание', blank=False, null=True)
    description_contact = RichTextUploadingField('Контакты', blank=False, null=True)
    description_req = RichTextUploadingField('Контакты', blank=False, null=True)
    money_earn = models.IntegerField('Перечислено в фонд', default=0)


    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            slugRandom = ''
            testSlug = Fond.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug

        super(Fond, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Фонд"
        verbose_name_plural = "Фонды"




