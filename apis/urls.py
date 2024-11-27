from django.urls import path
from .views import *

urlpatterns = [
    # Wallet URLs
    path('wallet/', WalletListCreateView.as_view(), name='wallet-list-create'),

    # Income URLs
    path('income/', IncomeListCreateView.as_view(), name='income-list-create'),

    # Expense URLs
    path('expense/', ExpenseListCreateView.as_view(), name='expense-list-create'),

    # Recent Activity
    path('last', RecentActivityView.as_view(), name='recent-activity'),

    # Filtered Activity (daily, monthly, yearly)
    path('filter/', FilteredActivityView.as_view(), name='filtered-activity'),
]
