from django.db import models


class Banner(models.Model):
    image = models.ImageField('Изображение категории', upload_to='img/', blank=True)
    url = models.CharField('Ссылка', max_length=255,blank=True)

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"


