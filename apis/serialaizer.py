from rest_framework import serializers
from .models import Wallet, Income, Expense

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['customer', 'balance']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['title', 'description', 'time', 'amount']

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['wallet', 'description', 'amount', 'time']

    def create(self, validated_data):
        validated_data['wallet'] = Wallet.objects.get(customer=self.context['request'].user)
        return super().create(validated_data)
