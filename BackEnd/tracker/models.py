from django.db import models
from django.contrib.auth.models import User

# كلاس الفئات (مثل: أكل، مواصلات، ترفيه)
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# كلاس المعاملات المالية (الدخل والمصاريف)
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INC', 'Income'),
        ('EXP', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ربط العملية بمستخدم معين
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.amount}"

# كلاس الأهداف المالية (US #6)
class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()

    def __str__(self):
        return self.name