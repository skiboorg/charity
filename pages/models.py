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
    image = models.ImageField('Лого фонда', upload_to='fond/', blank=True)
    description_short = RichTextUploadingField('Описание для окна покупки', blank=False, null=True)
    description_full = RichTextUploadingField('Полное описание', blank=False, null=True)
    description_contact = RichTextUploadingField('Контакты', blank=False, null=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.nameSlug:
            slugRandom = ''
            testSlug = Fond.objects.filter(nameSlug=slug)
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.nameSlug = slug + slugRandom
            else:
                self.nameSlug = slug

        super(Fond, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Фонд"
        verbose_name_plural = "Фонды"




