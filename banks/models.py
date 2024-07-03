from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, MinValueValidator

 #Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100, null=False)
    swift_code = models.CharField(max_length=100, null=False)
    inst_num = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100, null=False)
    transit_num = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    email = models.EmailField(default='admin@utoronto.ca', validators=[EmailValidator()])
    capacity = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    last_modified = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, related_name='branches', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
