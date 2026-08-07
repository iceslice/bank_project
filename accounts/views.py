# from django.shortcuts import render

# # Create your views here.

import csv
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models.functions import TruncMonth

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import UserRegisterForm, TransactionForm
from .models import Account, Transaction

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user, holder_name=user.username, account_number=f"AC{user.id:06d}")
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# @login_required
# def dashboard(request):
#     account, _ = Account.objects.get_or_create(user=request.user, defaults={'holder_name': request.user.username, 'account_number': f"AC{request.user.id:06d}"})
#     txns = Transaction.objects.filter(account=account)
#     total_deposits = txns.filter(transaction_type='Deposit').aggregate(Sum('amount'))['amount__sum'] or 0
#     total_withdrawals = txns.filter(transaction_type='Withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0
#     context = {
#         'account': account,
#         'total_deposits': total_deposits,
#         'total_withdrawals': total_withdrawals,
#         'total_transactions': txns.count(),
#         'recent_txns': txns[:5]
#     }
#     return render(request, 'accounts/dashboard.html', context)

@login_required
def dashboard(request):
    account, _ = Account.objects.get_or_create(
        user=request.user, 
        defaults={'holder_name': request.user.username, 'account_number': f"AC{request.user.id:06d}"}
    )
    txns = Transaction.objects.filter(account=account)
    
    # Core Dashboard Aggregations
    total_deposits = txns.filter(transaction_type='Deposit').aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdrawals = txns.filter(transaction_type='Withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # BONUS FEATURE: Monthly Summary Breakdown
    monthly_summary = (
        txns.annotate(month=TruncMonth('timestamp'))
        .values('month', 'transaction_type')
        .annotate(total=Sum('amount'))
        .order_by('-month')
    )

    # BONUS FEATURE: Format Chart Data Safely for JavaScript
    chart_data = {
        'labels': ['Total Deposits', 'Total Withdrawals'],
        'values': [float(total_deposits), float(total_withdrawals)]
    }

    context = {
        'account': account,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_transactions': txns.count(),
        'monthly_summary': monthly_summary,
        'chart_data': chart_data,
        'recent_txns': txns[:5]
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def deposit(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > 0:
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='Deposit', amount=amount, balance_after=account.balance)
                messages.success(request, f"Successfully deposited ${amount}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Amount must be greater than zero.")
    else:
        form = TransactionForm()
    return render(request, 'accounts/deposit.html', {'form': form})

@login_required
def withdraw(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if 0 < amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='Withdrawal', amount=amount, balance_after=account.balance)
                messages.success(request, f"Successfully withdrew ${amount}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid amount or insufficient balance (overdraft prevented).")
    else:
        form = TransactionForm()
    return render(request, 'accounts/withdraw.html', {'form': form})

# @login_required
# def transaction_history(request):
#     account = Account.objects.get(user=request.user)
#     txns = Transaction.objects.filter(account=account)
#     t_type = request.GET.get('type')
#     date_from = request.GET.get('date')
#     if t_type:
#         txns = txns.filter(transaction_type=t_type)
#     if date_from:
#         txns = txns.filter(timestamp__date=date_from)
#     return render(request, 'accounts/history.html', {'transactions': txns})


@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    txns = Transaction.objects.filter(account=account)
    
    # Filter Functionality
    t_type = request.GET.get('type')
    date_from = request.GET.get('date')
    if t_type:
        txns = txns.filter(transaction_type=t_type)
    if date_from:
        txns = txns.filter(timestamp__date=date_from)
        
    # BONUS FEATURE: CSV Export Engine
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="transactions_{account.account_number}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Type', 'Amount', 'Date & Time', 'Balance After'])
        for t in txns:
            writer.writerow([t.transaction_type, t.amount, t.timestamp.strftime('%Y-%m-%d %H:%M'), t.balance_after])
        return response

    # BONUS FEATURE: Pagination (10 records per page)
    paginator = Paginator(txns, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/history.html', {
        'page_obj': page_obj,
        'type': t_type,
        'date': date_from
    })