# 🎯 Arrow Scorer

**Arrow Scorer** is a lightweight Streamlit web application for marking, tracking, and analyzing archery scores on a **trispot** target. Built for archers and coaches, it helps visualize performance trends and assists in performance evaluations.


## 🚀 Features

- 📌 Mark scores on a trispot archery target
- 📊 View shot-by-shot analytics
- 🧮 Calculate ends and totals in real-time
- 📈 Analyze performance over sessions
- 💾 Save and reload scoring sessions


## 📦 Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for fast dependency management.

### Prerequisites

- Python 3.10+
- `uv` (install with: `pip install uv`)

### Clone and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/arrow_scorer.git
cd arrow_scorer

# Install dependencies using uv
uv pip install -r requirements.txt

# Run the app
uv run streamlit run main.py
```


## ⚙️ App Configuration


### `DATABASE_URL`

Defines the SQLAlchemy-compatible database connection string.
By default, it stores all data in a local SQLite file (`archery.db`). You can override the database backend by setting the `DATABASE_URL`environment variable.


**Examples:**

- **PostgreSQL:**
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```
- **MariaDB/MySQL:**
```bash
export DATABASE_URL="mysql+pymysql://user:password@localhost/dbname"
```
- **SQLite (default):**
```bash
export DATABASE_URL="sqlite:///archery.db"
```


### Alembic Migrations

Create the migration files with:
```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply the migrations with:
```bash
alembic upgrade head
``` 

