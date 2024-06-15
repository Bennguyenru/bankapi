from django.urls import path
from . import views

urlpatterns = [
    path('banks/', views.Banks.as_view(), name='bank_list'),
    path('banks/<int:pk>/', views.BankDetail.as_view(), name='bank_detail'),
    path('accounts/', views.Accounts.as_view(), name='account_list'),
    path('accounts/<int:pk>/', views.AccountDetail.as_view(), name='account_detail'),
    path('transactions/', views.Transactions.as_view(), name='transaction_list'),
    path('pendingtransactions/', views.PendingTransactions.as_view(), name='pending_transaction_list'),
    path('transactions/<int:pk>/', views.AccountTransactions.as_view(), name='AccountTransactions'),
    path('users/', views.Users.as_view(), name='get_users'),
    path('login/', views.UserAuthentication.as_view(), name='login'),
    path('authenticate_account/', views.AuthenticateAccount.as_view(), name='authenticate_account'),
    path('maketransaction/', views.MakeTransaction.as_view(), name='make_transaction'),
    path('deletetransaction', views.DeleteTransaction.as_view(), name='delete_transaction'),
]
'''


path('transactions/', views.TransactionList.as_view(), name='transaction_list'),
path('transactions/<int:pk>/', views.TransactionDetail.as_view(), name='transaction_detail'),
'''