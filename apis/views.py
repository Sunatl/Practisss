from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now, timedelta
from rest_framework.response import Response
from django.db.models import Sum
from .models import Wallet, Income, Expense
from .serialaizer import WalletSerializer, IncomeSerializer, ExpenseSerializer

# Wallet Views
class WalletListCreateView(ListCreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(customer=self.request.user)

# Income Views
class IncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(customer=self.request.user)

# Expense Views
class ExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(wallet__customer=self.request.user)

# Recent Activity View
class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        incomes = Income.objects.filter(customer=user).order_by('-time')[:10]
        expenses = Expense.objects.filter(wallet__customer=user).order_by('-time')[:10]

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        balance = Wallet.objects.get(customer=user).balance

        return Response({
            'recent_incomes': IncomeSerializer(incomes, many=True).data,
            'recent_expenses': ExpenseSerializer(expenses, many=True).data,
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance
        })

# Filtered Activity View (Daily, Monthly, Yearly)
class FilteredActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        period = request.query_params.get('period', 'daily')

        if period == 'daily':
            start_date = now().date()
        elif period == 'monthly':
            start_date = now().replace(day=1).date()
        elif period == 'yearly':
            start_date = now().replace(month=1, day=1).date()
        else:
            return Response({"error": "Invalid period"}, status=400)

        incomes = Income.objects.filter(customer=user, time__date__gte=start_date)
        expenses = Expense.objects.filter(wallet__customer=user, time__date__gte=start_date)

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            'period': period,
            'incomes': IncomeSerializer(incomes, many=True).data,
            'expenses': ExpenseSerializer(expenses, many=True).data,
            'total_income': total_income,
            'total_expense': total_expense
        })
