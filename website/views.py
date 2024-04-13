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


@views.route("/create-expense", methods=['POST'])
@login_required
def create_expense():
    if request.method == "POST":
        data = request.json

        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

      
        chartId = data.get('chartId')
        savings = data.get('savings')
        wants = data.get('wants')
        needs = data.get('needs')


        expense = Expense(id=chartId, owner = current_user.id,  savings=savings, wants=wants, needs=needs)
        db.session.add(expense)
        db.session.commit()
        return jsonify({'message': 'Expense created successfully'}), 201

    # Return an error response if the request method is not POST
    return jsonify({'error': 'Method not allowed'}), 405


@views.route("/expenses")
@login_required
def expenses():
    expenses = current_user.expenses

    # Assuming expenses is a list of Expense objects
    expenses_data = [
        {"id": expense.id, "owner": expense.owner, "savings": expense.savings, "wants": expense.wants, "needs": expense.needs}
        for expense in expenses
    ]

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


@views.route("/delete-all-transactions", methods=['POST'])
@login_required
def delete_all_transactions():
    try:
        # Assuming Expense has a foreign key 'owner' referring to 'user.id'
        Expense.query.filter_by(owner=current_user.id).delete()
        db.session.commit()
        return jsonify({"success": "All transactions deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


