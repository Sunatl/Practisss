from django.contrib import admin
from .models import Customer, Wallet, Income, Expense


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'full_name', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('username',)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('customer', 'balance')
    search_fields = ('customer__username', 'customer__email', 'customer__full_name')
    list_filter = ('customer',)
    ordering = ('customer',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'amount', 'customer', 'time')
    search_fields = ('title', 'customer__username', 'customer__email', 'customer__full_name')
    list_filter = ('customer', 'time')
    ordering = ('-time',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('get_customer', 'description', 'amount', 'time')
    search_fields = ('wallet__customer__username', 'wallet__customer__email', 'wallet__customer__full_name')
    list_filter = ('wallet__customer', 'time')
    ordering = ('-time',)

    def get_customer(self, obj):
        """Барои гирифтани истифодабаранда аз Wallet"""
        return obj.wallet.customer.username
    get_customer.short_description = 'Customer'
