import segno
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

class Category(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=True,related_name='subcategories')
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class Izdelie(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=False, null=True)
    izdelie = models.ForeignKey(Izdelie, on_delete=models.CASCADE, blank=False, null=True)
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    sku = models.CharField('Артикул', max_length=255, blank=False, null=True)
    serial_number = models.CharField('Серийный номер', max_length=255, blank=False, null=True)
    amount = models.IntegerField('Кол-во на остатке', blank=True, default=0)
    image = models.FileField(upload_to='product/', blank=True, null=True)
    qr = models.FileField(upload_to='product/qr/', blank=True, null=True)
    qr_scan = models.FileField(upload_to='product/qrscan/', blank=True, null=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def save(self, *args, **kwargs):
        if not self.qr:
            qr = segno.make_qr(f'/qr/{self.uuid}', version=23, error='L', mask=3)
            path = f'{settings.MEDIA_ROOT}/product/qr/{self.uuid}.png'
            qr.save(path, scale=10, dark=(0,0,0,), light=(240, 240, 240), border=0)
            self.qr = f'product/qr/{self.uuid}.png'
        if not self.qr_scan:


            image = Image.open(self.qr)

            # Define the text and font for each line
            text1 = self.name
            font1 = ImageFont.truetype("arial.ttf", 24)

            text2 = self.sku
            font2 = ImageFont.truetype("arial.ttf", 18)


            # Define the desired padding
            padding_top = 50
            padding_bottom = 100
            padding_left = 50
            padding_right = 50

            # Define the desired image size
            new_width = 300
            new_height = 300

            # Scale the image to fit within the desired width and height
            image.thumbnail((new_width, new_height))

            # Get the size of the scaled image
            imagewidth, imageheight = image.size

            # Calculate the size of the new image with padding
            new_width = imagewidth + padding_left + padding_right
            new_height = imageheight + padding_top + padding_bottom

            # Create a new image with a white background
            new_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))

            # Paste the scaled image onto the new image with padding
            new_image.paste(image, (padding_left, padding_top))

            # Draw the text on the new image
            draw = ImageDraw.Draw(new_image)

            # Calculate the position of the first line of text
            text1_width, text1_height = draw.textsize(text1, font=font1)
            text1_x = (new_width - text1_width) // 2
            text1_y = padding_top + imageheight + 20

            # Draw the first line of text
            draw.text((text1_x, text1_y), text1, font=font1, fill=(0, 0, 0))

            # Calculate the position of the second line of text
            text2_width, text2_height = draw.textsize(text2, font=font2)
            text2_x = (new_width - text2_width) // 2
            text2_y = text1_y + text1_height + 20

            # Draw the second line of text
            draw.text((text2_x, text2_y), text2, font=font2, fill=(0, 0, 0))



            # Save the new image with the image and text
            new_image.save(f'{settings.MEDIA_ROOT}/product/qrscan/{self.uuid}.jpg')
            self.qr_scan=f'/product/qrscan/{self.uuid}.jpg'


        super().save(*args, **kwargs)




class ProductSupply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=True,related_name='supplies')
    amount = models.IntegerField('Кол-во', blank=True, default=0)
    text = models.TextField('Просхождение', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.date}'

    def save(self, *args, **kwargs):
        self.product.amount += self.amount
        self.product.save()
        super().save(*args, **kwargs)


class ProductRemove(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=True, related_name='removes')
    amount = models.IntegerField('Кол-во', blank=True, default=0)
    text = models.TextField('КУДА СПИСЫВАЕТСЯ', blank=True, null=True)
    is_remove = models.BooleanField('ДА\НЕТ, для списания потерь', default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.date}'

    def save(self, *args, **kwargs):
        self.product.amount -= self.amount
        self.product.save()
        super().save(*args, **kwargs)