from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Expense
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    expenses = Expense.query.all()
    return render_template("home.html", user=current_user, expenses=expenses)

@views.route("/about")
def about():
    return render_template('about.html', user=current_user)

@views.route("/history")
@login_required
def history():
    expenses = Expense.query.all()
    return render_template('history.html', user=current_user)

# @views.route("/save-expense", methods=['POST'])
# @login_required
# def save_expense():
#     text = request.form.get('text')
#     amount = request.form.get('amount')
#     category = request.form.get('category')

#     if not text or not amount or not category:
#         flash('Expense cannot be empty.', category='error')
#     else:
#         expense = Expense(text=text, amount=amount, category=category, author=current_user.id)
#         db.session.add(expense)
#         db.session.commit()
#         flash('Expense created!', category='success')

#     return redirect(url_for('views.home'))

@views.route("/create-expense", methods=['GET', 'POST'])
@login_required
def create_expense():
    if request.method == "POST":
        text = request.form.get('text')
        chartId = request.form.get('chartId')
        savings = request.form.get('savings')
        wants = request.form.get('wants')
        needs = request.form.get('needs')

        if not text:
            flash('Expense cannot be empty', category='error')
        else:
            expense = Expense(text=text, author=current_user.id, chartId=chartId, savings=savings, wants=wants, needs=needs)
            db.session.add(expense)
            db.session.commit()
            flash('Expense created!', category='success')
            return redirect(url_for('views.home'))

    # Change html template file name when new one is created
    return render_template('start.html', user=current_user)


@views.route("/expenses/<username>")
@login_required
def expenses(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    expenses = user.expenses

    # Assuming expenses is a list of dictionaries
    expenses_data = [{"id": expense.id, "amount": expense.amount, "category": expense.category} for expense in expenses]

    return jsonify(expenses_data)

@views.route("/start", methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        names = request.form.getlist('name[]')
        amounts = request.form.getlist('amount[]')
        categories = request.form.getlist('category[]')

        # Create and save new Expense instances for each set of data
        for name, amount, category in zip(names, amounts, categories):
            new_expense = Expense(description=name, amount=float(amount), category=category, owner=current_user.id)
            db.session.add(new_expense)
        db.session.commit()
        flash('Expenses added successfully!', category='success')
        return redirect(url_for('views.start'))
    
    return render_template('start.html', user=current_user)

from flask import jsonify

# @views.route("/expense-data")
# @login_required
# def expense_data():
#     # Querying expenses and grouping them by category with the sum of amounts
#     expenses = db.session.query(
#         Expense.category,
#         db.func.sum(Expense.amount).label('total')
#     ).group_by(Expense.category).all()

#     data = [{"category": exp.category, "amount": float(exp.total)} for exp in expenses]
#     return jsonify(data)

# @views.route("/delete-all-transactions", methods=['POST'])
# @login_required
# def delete_all_transactions():
#     try:
#         # Assuming Expense has a foreign key 'owner' referring to 'user.id'
#         Expense.query.filter_by(owner=current_user.id).delete()
#         db.session.commit()
#         return jsonify({"success": "All transactions deleted successfully"}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


