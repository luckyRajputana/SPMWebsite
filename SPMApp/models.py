from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator
from django.db import models

class  mainpagetable(models.Model):
    id = models.AutoField(primary_key=True)
    ModelNo = models.CharField(max_length=100)
    VendorType = models.CharField(max_length=100)
    CompanyType = models.CharField(max_length=100)
    ItemType = models.CharField(max_length=100)
    HSNCode = models.CharField(max_length=100)
    PriceFromChina = models.FloatField(validators=[MinValueValidator(0)])
    DeclaredCustomPrice = models.FloatField(validators=[MinValueValidator(0)])
    SellingPrice = models.FloatField(validators=[MinValueValidator(0)])
    DateTime = models.DateTimeField()
    objects = models.Manager()

    class Meta:
        # Specify the exact table name for PostgreSQL
        # db_table = 'mainpagetable'
        # Add a unique constrsaint on the combination of 'name' and 'category'
        unique_together = ('ModelNo', 'VendorType')

    def __str__(self):
        return self.ModelNo