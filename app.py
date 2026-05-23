from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import csv

app = Flask(__name__)

DB_NAME = "database.db"


def create_table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():

    search = request.args.get("search", "")

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    query = """
        SELECT * FROM expenses
        WHERE title LIKE ?
        OR category LIKE ?
        ORDER BY date DESC
    """

    cursor.execute(query, (f"%{search}%", f"%{search}%"))
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    category_data = cursor.fetchall()

    connection.close()

    if total is None:
        total = 0

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_data=category_data
    )


@app.route("/add", methods=["POST"])
def add_expense():

    title = request.form["title"]
    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (title, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

    connection.commit()
    connection.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_expense(id):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


@app.route("/export")
def export_csv():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    connection.close()

    response = make_response()

    response.headers["Content-Disposition"] = "attachment; filename=expenses.csv"
    response.headers["Content-type"] = "text/csv"

    writer = csv.writer(response.stream)

    writer.writerow([
        "ID",
        "Title",
        "Amount",
        "Category",
        "Date"
    ])

    for expense in expenses:
        writer.writerow(expense)

    return response


if __name__ == "__main__":
    create_table()
    app.run(debug=True)