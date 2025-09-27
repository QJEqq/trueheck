import datetime
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Brand(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.CharField(max_length=25, unique=True)
    logo = models.ImageField(upload_to='brands-logo/')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Transmission(models.Model):
    type = models.CharField(max_length=35)
    
    def __str__(self):
        return self.type
    
class DriveType(models.Model):
    type = models.CharField(max_length=35)
    
    def __str__(self):
        return self.type
    
class FuelType(models.Model):
    type = models.CharField(max_length=35)
    
    def __str__(self):
        return self.type
    
class ModelAuto(models.Model):
    
    CURRENT_YEAR = datetime.datetime.now().year
    YEAR_CHOICES = [(year, str(year)) for year in range(2000, CURRENT_YEAR + 1)]
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Марка авто" , related_name='models')
    name = models.CharField(max_length=125, unique=True)
    slug = models.CharField(max_length=125, unique=True)
    main_image = models.ImageField(upload_to="ModelAuto/main/")
    year = models.IntegerField(verbose_name="Год выпуска",
                                choices=YEAR_CHOICES,
                                default=CURRENT_YEAR,
                                db_index=True
                                )
    mileage = models.IntegerField(verbose_name="Пробег",
                                  validators=[MinValueValidator(0)],
                                  default=0
                                 )
    
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE, verbose_name="Трансмиссия", related_name='cars')
    drive_type = models.ForeignKey(DriveType, on_delete=models.CASCADE , verbose_name="Привод", related_name='cars')
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE, verbose_name="Тип Топлива", related_name='cars')
    
    engine_volume = models.DecimalField(max_digits=3,           
                                        decimal_places=1,       
                                        validators=[
                                            MinValueValidator(0),
                                            MaxValueValidator(12.5)
                                        ],
                                        verbose_name="Объем двигателя",
                                        help_text="Объем в литрах (от 0.1 до 12.5 л)",
                                        blank=True,
                                        null=True)
    horse_power = models.IntegerField(verbose_name="Лошадиные силы",
                                      validators=[MinValueValidator(0)],
                                      default=0)
    price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                validators=[MinValueValidator(0)],
                                default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.fuel_type and self.fuel_type.type.lower() == 'электро':
            self.engine_volume = 0.0
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['-created_at']  
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'   
        
    def __str__(self):
        return self.name
    
class ModelAutoImage(models.Model):
    modelauto = models.ForeignKey(ModelAuto, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="ModelAuto/extra")
