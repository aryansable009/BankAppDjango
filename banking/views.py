from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from banking.models import *

from django.db.models import Q

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)    
            return redirect('accounts')      
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html', {})

def register_view(request):
    return render(request, 'register.html', {})

def accounts(request):
    data = {}
    data['Request_Account'] = Account.objects.get(AC_user = UserProfiles.objects.get(UP_user = request.user))
    data['account_transactions'] = Transactions.objects.filter(Q(TC_sender_account = data['Request_Account']) | Q(TC_receiver_account = data['Request_Account'])).order_by('-TC_date')
    return render(request, 'accounts.html', data)

def deposit_view(request):
    return render(request, 'deposit.html',{})

def withdraw_view(request):
    return render(request, 'withdraw.html',{})

def transfer_view(request):
    return render(request, 'transfer.html',{})

def submit_transfer(request):
    if request.method == "POST":
        print(request.user)
        print(Account.objects.filter(AC_user = UserProfiles.objects.filter(UP_user = request.user).first()).first().AC_balance)
        account_number = request.POST.get('account-number')
        account_name = request.POST.get('account-name')
        transfer_amount = request.POST.get('transfer-amount')
        recevier_accounts = Account.objects.filter(AC_AccoutNumber = account_number , AC_user__UP_UserName = account_name)
        sender_accounts = Account.objects.filter(AC_user = UserProfiles.objects.filter(UP_user = request.user).first())
        if recevier_accounts.exists():
            recevier_account = recevier_accounts.first()
            sender_account = sender_accounts.first()
            if recevier_account != sender_account:
                if float(sender_account.AC_balance) >= float(transfer_amount):
                    print('yo')
                    sender_account.AC_balance = float(sender_account.AC_balance) - float(transfer_amount)
                    recevier_account.AC_balance = float(recevier_account.AC_balance) + float(transfer_amount)
                    sender_account.save()
                    recevier_account.save()
                    transaction = Transactions(
                        TC_sender_account = sender_account,
                        TC_amount = transfer_amount,
                        TC_type = 'transfer',
                        TC_receiver_account = recevier_account
                    )
                    transaction.save()
                    return render(request, 'transfer.html', {'success': 'Transfer Sucessfull'})
                else:
                    return render(request, 'transfer.html', {'error': 'Insufficient funds'})
            else:
                return render(request, 'transfer.html', {'error': 'Cannot trsfer to your account'})
        else:
            return render(request, 'transfer.html', {'error': 'Account details doesnt match'})

    return render(request, 'transfer.html', {'error': 'Invalid credentials'})
    
def submit_withdraw(request):
    if request.method == "POST":
        withdrawal_amount = request.POST.get('withdraw-amount')
        withdrawal_account = Account.objects.filter(AC_user = UserProfiles.objects.filter(UP_user = request.user).first()).first()
        if float(withdrawal_account.AC_balance) >= float(withdrawal_amount):
            withdrawal_account.AC_balance = float(withdrawal_account.AC_balance) - float(withdrawal_amount)
            withdrawal_account.save()
            transaction = Transactions(
                        TC_sender_account = withdrawal_account,
                        TC_amount = withdrawal_amount,
                        TC_type = 'withdraw',
                    )
            transaction.save()
            return render(request, 'withdraw.html', {'success': 'Withdrawal Sucessfull'})
        else:
            return render(request, 'withdraw.html' , {'error': 'Insufficient funds'})
        
def submit_deposit(request):
    if request.method == "POST":
        deposit_amount = request.POST.get('deposit-amount')
        deposit_account = Account.objects.filter(AC_user = UserProfiles.objects.filter(UP_user = request.user).first()).first()
        deposit_account.AC_balance = float(deposit_account.AC_balance) + float(deposit_amount)
        deposit_account.save()
        transaction = Transactions(
                    TC_sender_account = deposit_account,
                    TC_amount = deposit_amount,
                    TC_type = 'deposit',
                )
        transaction.save()
        return render(request, 'deposit.html', {'success': 'Deposit Sucessfull'})

