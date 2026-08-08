# Bank Account Transaction Management System

A secure, high-performance Django web application for managing personal banking accounts, transaction processing, and historical data visualization. Built as an academic assignment project.

## 🚀 Features Implemented

### Core Features
*   **Part 1: Secure Authentication:** Complete User Registration, Login, and Logout flows. Access protection enforces data isolation (users can only access their own dashboard and ledger data).
*   **Part 2: Bank Account Management:** Automatic assignment of dedicated Account Numbers (`ACXXXXXX`) tied unique to users, tracking owner details and updating balances live.
*   **Part 3 & 4: Transaction Processing Engine:** Automated validation logic processing real-time Deposits and Withdrawals. Built-in mechanisms safely prevent account overdrafts.
*   **Part 5: Transaction History:** Fast ledger rendering structured to surface transaction details (Type, Amount, Balance Alteration, Timestamp) with newest records displayed first.
*   **Part 6: Search & Filtering Architecture:** Multi-tier server querying allowing filtering by transaction type and exact date parameters simultaneously.
*   **Part 7: Financial Summary Dashboard:** Dynamic data cards highlighting Current Balance, Accumulation Aggregates, Total Transactions, and recent activities.

### 🌟 Bonus Features (+10 Marks)
1.  **Bootstrap UI Integration:** Rendered using crisp, responsive layout components with `django-bootstrap4`.
2.  **Toggleable Dark Mode:** Advanced interface stylesheet syncing theme states across sessions using native browser `localStorage`.
3.  **Matplotlib / Chart.js Visualization:** Responsive front-end data charts built in JavaScript displaying spending vs saving metrics directly on the dashboard.
4.  **Data Export Engine (CSV):** Functional server-side streaming engine saving filter-preserved query matrices into standalone downloaded `.csv` spreadsheets.
5.  **Dynamic Item Pagination:** Clean list segmentation breaking large historical ledgers into standard 10-row navigations to preserve performance.
6.  **Monthly Accumulation Breakdown:** Analytical summary matrices sorting historical spending and income profiles by chronologically stacked calendar months.

---

## 🛠️ System Requirements
*   **Python:** 3.10 or higher
*   **Django Framework:** 4.2+
*   **Database:** SQLite3 (Default for development)

---

## ⚙️ Installation & Local Environment Setup

Follow these sequential terminal commands to initialize the project environment on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com
cd YOUR_REPOSITORY_NAME
```

### 2. Configure a Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Generate and write relational tables locally using native schemas:
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### 5. Create a Superuser (Optional - Admin Portal Access)
```bash
python manage.py createsuperuser
```

### 6. Boot the Local Server
```bash
python manage.py runserver
```
Open your browser and navigate to: `http://127.0.0.1:8000/`

---

## 📁 Repository Structure
```text
bank_project/
│
├── bank_project/           # Core configuration files (settings, root urls)
├── accounts/               # Application-specific architecture
│   ├── migrations/         # Database migration logs
│   ├── templates/          # HTML structures and UI themes
│   │   ├── accounts/       # App view screens (dashboard, history, login)
│   │   └── base.html       # Base Bootstrap layout template and Dark Mode scripts
│   ├── forms.py            # Validation logic schemas
│   ├── models.py           # Relational schema architecture (Account & Transaction)
│   ├── urls.py             # Route routing matrices
│   └── views.py            # Transaction processors and CSV endpoints
│
├── db.sqlite3              # Local relational runtime development database
├── manage.py               # Django orchestrator entry point
└── requirements.txt        # Frozen third-party dependency file
```

---

## 🖼️ User Interface Screenshots


1.  **Registration View:** `docs/screenshots/Registration Screenshot 2026-08-07 221325.png`
2.  **Login Screen Gateway:** `docs/screenshots/Login Screenshot 2026-08-07 221131.png`
3.  **Main Account Dashboard & Charts:** `docs/screenshots/Dashboard Screenshot 2026-08-07 220450.png`
4.  **Transaction Processing (Deposit/Withdrawal Forms):** `docs/screenshots/Deposit Screenshot 2026-08-07 220632.png`
5.  **Historical Ledger (With Pagination, Filtering & CSV Export):** `docs/screenshots/Transaction History Screenshot 2026-08-07 220759.png`


## To populate sample Bank data, run the following command

```bash
python manage.py populate_bank_data
```
Log into your app using the username: testuser   and   password: Password123!