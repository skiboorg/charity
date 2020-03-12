import os

from django.db.models.signals import post_save
from pytils.translit import slugify
from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image
from django.conf import settings
import uuid
from random import choices
import string
from customuser.models import User
from pages.models import *

class Town(models.Model):
    name = models.CharField('Название города', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, editable=False)
    def __str__(self):
        return '%s ' % self.name

    def save(self, *args, **kwargs):
        print('save')
        slug = slugify(self.name)
        testSlug = Town.objects.filter(name_slug=slug)
        if not self.name_slug:
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug

        super(Town, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, editable=False)
    image = models.ImageField('Изображение категории', upload_to='img/', blank=True)
    atIndex = models.BooleanField('На главной?', default=False)

    def __str__(self):
        return '%s ' % self.name

    def save(self, *args, **kwargs):
        print('save')
        slug = slugify(self.name)
        testSlug = Category.objects.filter(name_slug=slug)
        if not self.name_slug:
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug

        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class SubCategory(models.Model):
    category = models.ForeignKey(Category, blank=True, verbose_name='Категория', on_delete=models.CASCADE,
                                 db_index=True, related_name='subcats')
    name_slug = models.CharField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField('Название подкатегории', max_length=255, blank=False, null=True)


    def __str__(self):
        return '%s ' % self.name

    def save(self, *args, **kwargs):
        print('save')
        slug = slugify(self.name)
        testSlug = SubCategory.objects.filter(name_slug=slug)
        if not self.name_slug:
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug

        super(SubCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

class Item(models.Model):
    fond = models.ForeignKey(Fond,blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Перечислить в фонд')
    category = models.ForeignKey(Category, blank=False, verbose_name='Категория',on_delete=models.CASCADE, db_index=True)
    subCategory = models.ForeignKey(SubCategory, blank=True, null=True, verbose_name='Подкатегория', on_delete=models.CASCADE,
                                 db_index=True)
    town = models.ForeignKey(Town, blank=False, verbose_name='Город', on_delete=models.CASCADE,
                                    db_index=True)
    user = models.ForeignKey(User, blank=False, verbose_name='Пользователь', on_delete=models.CASCADE,
                             db_index=True)
    name = models.CharField('Название товара', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    description = models.TextField('Описание товара', blank=True, null=True)
    address = models.CharField('Местоположение', max_length=255, null=True)
    added = models.DateTimeField('Добавлен', auto_now_add=True)
    price = models.IntegerField(default=0)
    otherChoice = models.CharField('Альтернативный выбор', max_length=255, blank=True, null=True)
    isService = models.BooleanField('Услуга?', default=False)
    isActive = models.BooleanField('Отображается?', default=True)
    isSold = models.BooleanField('Продан?', default=False)


    def __str__(self):
        return '%s ' % self.name

    def save(self, *args, **kwargs):
        print('save')
        slug = slugify(self.name)
        testSlug = Item.objects.filter(name_slug=slug)
        slugRandom = ''
        if not self.name_slug:
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug
        self.name_lower = self.name.lower()
        super(Item, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class ItemImage(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField('Изображение товара', upload_to='items', blank=False)
    image_small = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return '%s Изображение для товара : %s ' % (self.id, self.item.name)

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image_small:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image_small))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Картинка'

    def save(self, *args, **kwargs):
        fill_color = '#fff'
        image = Image.open(self.image).convert('RGB')


        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, fill_color)
            background.paste(image, image.split()[-1])
            image = background
        image.thumbnail((270, 270), Image.ANTIALIAS)
        small_name = 'media/items/{}/{}'.format(self.item.id, str(uuid.uuid4()) + '.jpg')
        if settings.DEBUG:
            os.makedirs('media/items/{}'.format(self.item.id), exist_ok=True)
            image.save(small_name, 'JPEG', quality=100)
        else:
            os.makedirs('C:\inetpub\wwwroot\charity/media/items/{}'.format(self.item.id), exist_ok=True)
            image.save('charity/' + small_name, 'JPEG', quality=100)
        self.image_small = '/' + small_name

        super(ItemImage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Изображение для товара"
        verbose_name_plural = "Изображения для товара"

class UserBuys(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)

class UserFavorites(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)


class Order(models.Model):
    seller = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, related_name='buyer')
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE)
    pay_by = models.CharField('Оплата через', max_length=100, blank=True, null=True)
    isPayed = models.BooleanField('Оплачен?', default=False)
    createdAt = models.DateField(auto_now_add=True)
    sber_orderID = models.CharField('sber_orderID', max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Заказ {self.id}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


def itemPostSave(sender, instance, created,**kwargs):
    if created and instance.otherChoice:
        instance.isActive = False
        instance.save()


post_save.connect(itemPostSave, sender=Item)