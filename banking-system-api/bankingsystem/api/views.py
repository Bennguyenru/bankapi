from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BankSerializer, AccountSerializer, TransactionSerializer, UserSerializer
from .models import Bank, Account, Transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
import datetime


class Banks(APIView):
    def get(self, request):
        banks_list = Bank.objects.all()
        serializer = BankSerializer(banks_list, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

class BankDetail(APIView):
    def get(self, request, pk):
        bank = Bank.objects.get(pk=pk)
        serializer = BankSerializer(bank)
        return Response(serializer.data)
    def delete(self, request, pk):
        bank = Bank.objects.get(pk=pk)
        bank.delete()
        return Response(status=204)
    
class Accounts(APIView):
    def get(self, request):
        accounts_list = Account.objects.all()
        serializer = AccountSerializer(accounts_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

        
class AccountDetail(APIView):
    def get(self, request, pk):
        account = Account.objects.get(account_number=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    def delete(self, request, pk):
        account = Account.objects.get(pk=pk)
        account.delete()
        return Response(status=204)


class Transactions(APIView):
    def get(self, request):
        transactions_list = Transaction.objects.all()
        serializer = TransactionSerializer(transactions_list, many=True)
        return Response(serializer.data)
    def put(self, request):
        action = request.data['transaction_type']
        amount = int(request.data['amount'])
        account_id = request.data['account_id']
        account = Account.objects.get(account_id=account_id)
        if action == 'Deposit':
            transaction = Transaction(account=account, transaction_type='Deposit', amount=amount)
        elif action == 'Withdrawal':
            if account.balance < amount:
                return Response({'error': 'Insufficient balance'}, status=400)
            transaction = Transaction(account=account, transaction_type='Withdrawal', amount=amount)
        else:
            return Response({'error': 'Invalid transaction type'}, status=400)
        transaction.save()
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    def delete(self, request):
        transaction_id = request.data['transaction_id']
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        transaction.delete()
        return Response(status=204)
    

class PendingTransactions(APIView):
    def get(self, request):
        transactions_list = Transaction.objects.filter(pending=True)
        serializer = TransactionSerializer(transactions_list, many=True)
        return Response(serializer.data)
class Users(APIView):
    def get(self, request):
        users_list = User.objects.all()
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data)
    def post(self, request):
        data = request.data.copy()
        print(data)
        print(request.data['password'], 'x')
        data['password'] = make_password(request.data['password'])
        data['is_active'] = True
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
    
    
class UserAuthentication(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'Username or Password is incorrect'}, status=400)

class AuthenticateAccount(APIView):
    def post(self, request):
        account_number = request.data['account_number']
        password = request.data['password']
        account = Account.objects.get(account_number=account_number)
        if account.password == password:
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        return Response({'error': 'Account number or Password is incorrect'}, status=400)
    
class AccountTransactions(APIView):
    def get(self, request, pk):
        account = Account.objects.get(account_id=pk)
        transactions = Transaction.objects.filter(account=account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    

class MakeTransaction(APIView):
    def put(self, request):
        transaction_id = request.data['transaction_id']
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        account = Account.objects.get(account_id=transaction.account.account_id)
        if transaction.transaction_type == 'Deposit':
            account.balance += transaction.amount
        elif transaction.transaction_type == 'Withdrawal':
            if account.balance < transaction.amount:
                return Response({'error': 'Insufficient balance'}, status=400)
            account.balance -= transaction.amount
        transaction.pending = False                
        account.save()
        transaction.save()
        return Response(status=200)

class DeleteTransaction(APIView):
    def post(self, request):
        transaction_id = request.data['transaction_id']
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        transaction.delete()
        return Response(status=204)