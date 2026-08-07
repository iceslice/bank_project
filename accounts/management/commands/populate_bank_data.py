import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Account, Transaction

class Command(BaseCommand):
    help = 'Populates the database with sample user, account, and transactional history.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing database population...")

        # 1. Create a baseline Test User
        username = "testuser"
        email = "testuser@securebank.com"
        password = "Password123!"

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created User: {username} (Password: {password})"))
        else:
            self.stdout.write(f"User '{username}' already exists. Skipping user creation.")

        # 2. Setup or fetch the Bank Account
        account, ac_created = Account.objects.get_or_create(
            user=user,
            defaults={
                'holder_name': "John Doe Tester",
                'account_number': "AC000452",
                'balance': 0.00
            }
        )
        
        if ac_created:
            self.stdout.write(self.style.SUCCESS(f"Created Account: {account.account_number}"))
        else:
            # Clear old transactions to cleanly repopulate if run multiple times
            Transaction.objects.filter(account=account).delete()
            account.balance = 0.00
            account.save()
            self.stdout.write("Cleared existing transactions for fresh historical generation.")

        # 3. Generate Historical Transaction Matrix
        # Spreading 25 transactions across the past 90 days to fill charts, summaries, and pagination
        current_balance = 5000.00  # Give them a starting injection
        account.balance = current_balance
        account.save()

        # Establishing a fixed initial deposit to ground the data
        now = timezone.now()
        Transaction.objects.create(
            account=account,
            transaction_type='Deposit',
            amount=5000.00,
            timestamp=now - timedelta(days=90),
            balance_after=5000.00
        )

        transaction_choices = [
            ('Deposit', 200.00, 1500.00),     # Type, Min Amount, Max Amount
            ('Withdrawal', 20.00, 450.00),
            ('Withdrawal', 10.00, 150.00),    # Extra weight to withdrawals for realism
            ('Deposit', 500.00, 2500.00),
        ]

        self.stdout.write("Generating 24 historical ledger records across 90 days...")
        
        for i in range(1, 25):
            t_type, min_amt, max_amt = random.choice(transaction_choices)
            amount = round(random.uniform(min_amt, max_amt), 2)
            
            # Stagger timestamps backward chronologically
            days_ago = random.randint(1, 89)
            hours_ago = random.randint(1, 23)
            txn_time = now - timedelta(days=days_ago, hours=hours_ago)

            if t_type == 'Deposit':
                current_balance += amount
            else:
                # Preventive check so our random generator doesn't drop account under $0
                if current_balance - amount < 0:
                    t_type = 'Deposit'
                    current_balance += amount
                else:
                    current_balance -= amount

            # Create entry
            Transaction.objects.create(
                account=account,
                transaction_type=t_type,
                amount=amount,
                timestamp=txn_time,
                balance_after=round(current_balance, 2)
            )

        # Update final aggregate balances on the main account
        account.balance = round(current_balance, 2)
        account.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully populated ledger! Final account balance: ${account.balance}"))
