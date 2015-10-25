from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, default='Default')
    number_of_items = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    length = models.FloatField(null=True, blank=True)
    breadth = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='images')
    thumbnail = models.ImageField(upload_to='images', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def create_thumbnail(self):
        if not self.image:
            return

        from PIL import Image
        import os
        from django.core.files.uploadhandler import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile

        THUMBNAIL_SIZE = (80, 80)
        FULL_SIZE = (760, 950)

        DJANGO_TYPE = self.image.file.content_type

        PIL_TYPE = 'jpeg'
        FILE_EXTENSION = 'jpg'

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        elif DJANGO_TYPE == 'image/gif':
            PIL_TYPE = 'gif'
            FILE_EXTENSION = 'gif'
        elif DJANGO_TYPE == 'image/jpg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'

        r = BytesIO(self.image.read())
        fullsize_image = Image.open(r)
        new_image = fullsize_image.copy()

        fullsize_image.thumbnail(FULL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        fullsize_image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)

        self.image.save('{}.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

        new_image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        new_image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)

        self.thumbnail.save('{}_thumbnail.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self):
        self.create_thumbnail()
        super(Product, self).save()
