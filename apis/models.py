from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom User Manager
class CustomerManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomerManager()

    def __str__(self):
        return self.username

# Wallet Model
class Wallet(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.customer.username} - Balance: {self.balance}"

# Income Model
class Income(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        wallet = Wallet.objects.get(customer=self.customer)
        wallet.balance += self.amount
        wallet.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Income by {self.customer.username}: {self.amount}"

# Expense Model
class Expense(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.wallet.balance >= self.amount:
            self.wallet.balance -= self.amount
            self.wallet.save()
        else:
            raise ValueError("Not enough balance for this expense.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Expense for {self.wallet.customer.username}: {self.amount}"

# Create Wallet Automatically
@receiver(post_save, sender=Customer)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(customer=instance)
