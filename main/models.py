from distutils.command.upload import upload
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import uuid
from django.contrib.auth.models import User 

# Create your models here.
class Product(models.Model):
    name = models.CharField(blank=True, null=True, max_length=150)
    quantity = models.CharField(blank=True, null=True, max_length=10)
    price = models.CharField(blank=True, null=True, max_length=10)
    description = models.CharField(blank=True, null=True, max_length=200)
    product_image = models.FileField(upload_to="uploads/", blank=True, null=True)
    product_link = models.CharField(blank=True, null=True, max_length=200)
    product_qrcode = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, max_length=10)
    created = models.DateTimeField(auto_created=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(f'https://qrcodegenapp.herokuapp.com/productInfo/{self.id}')
        canvas = Image.new('RGB', (500,500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.product_qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['created']

