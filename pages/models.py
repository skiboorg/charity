from django.db import models

class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, blank=False, null=True)
    image = models.ImageField('Изображение категории', upload_to='img/', blank=True)
    atIndex = models.BooleanField('На главной?', default=False)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        verbose_name = "Основная категория"
        verbose_name_plural = "Основные категории"

class Banner(models.Model):
    image = models.ImageField('Изображение категории', upload_to='img/', blank=True)

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

class Item(models.Model):
    category = models.ForeignKey(Category, blank=True, verbose_name='Подкатегория',on_delete=models.CASCADE, db_index=True, related_name='items')
    image = models.ImageField('Изображение товара', upload_to='items', blank=False)
    name = models.CharField('Название товара', max_length=255, blank=False, null=True)
    description = models.TextField('Описание товара', blank=True, null=True)
    address = models.CharField('Местоположение', max_length=255, null=True)
    time = models.CharField('Размещено', max_length=255, null=True)
    price = models.IntegerField(default=0)
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"



class ItemImage(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField('Изображение товара', upload_to='items', blank=False)



    def __str__(self):
        return '%s Изображение для товара : %s ' % (self.id, self.item.name)

    class Meta:
        verbose_name = "Изображение для товара"
        verbose_name_plural = "Изображения для товара"

