from django.db import models

# Create your models here.

class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to="media",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return (f"Nombre: {self.name}\nPrecio: {self.price}\nDescripcion: {self.description}\n Cantidad: {self.quantity}")

    def get_image(self):
        if self.image:
            return self.image.url
        return ''


    class Meta():
        verbose_name = 'product'
        verbose_name_plural = 'products'