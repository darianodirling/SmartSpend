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


@views.route("/create-expense", methods=['GET', 'POST'])
@login_required
def create_expense():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Expense cannot be empty', category='error')
        else:
            expense = Expense(text=text, author=current_user.id)
            db.session.add(expense)
            db.session.commit()
            flash('Expense created!', category='success')
            return redirect(url_for('views.home'))

    # Change html template file name when new one is created
    return render_template('create_post.html', user=current_user)


@views.route("/delete-expense/<id>")
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()

    if not expense:
        flash("Expense does not exist.", category='error')
    elif current_user.id != expense.id:
        flash('You do not have permission to delete this expense.', category='error')
    else:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/expenses/<username>")
@login_required
def expenses(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    expenses = user.expenses
    # Change html template file name to new one once completed
    return render_template("posts.html", user=current_user, expenses=expenses, username=username)

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

@views.route("/expense-data")
@login_required
def expense_data():
    # Querying expenses and grouping them by category with the sum of amounts
    expenses = db.session.query(
        Expense.category,
        db.func.sum(Expense.amount).label('total')
    ).group_by(Expense.category).all()

    data = [{"category": exp.category, "amount": float(exp.total)} for exp in expenses]
    return jsonify(data)

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

# @views.route("/create-comment/<post_id>", methods=['POST'])
# @login_required
# def create_comment(post_id):
#     text = request.form.get('text')

#     if not text:
#         flash('Comment cannot be empty.', category='error')
#     else:
#         post = Post.query.filter_by(id=post_id)
#         if post:
#             comment = Comment(
#                 text=text, author=current_user.id, post_id=post_id)
#             db.session.add(comment)
#             db.session.commit()
#         else:
#             flash('Post does not exist.', category='error')

#     return redirect(url_for('views.home'))


# @views.route("/delete-comment/<comment_id>")
# @login_required
# def delete_comment(comment_id):
#     comment = Comment.query.filter_by(id=comment_id).first()

#     if not comment:
#         flash('Comment does not exist.', category='error')
#     elif current_user.id != comment.author and current_user.id != comment.post.author:
#         flash('You do not have permission to delete this comment.', category='error')
#     else:
#         db.session.delete(comment)
#         db.session.commit()

#     return redirect(url_for('views.home'))


# @views.route("/like-post/<post_id>", methods=['POST'])
# @login_required
# def like(post_id):
#     post = Post.query.filter_by(id=post_id).first()
#     like = Like.query.filter_by(
#         author=current_user.id, post_id=post_id).first()

#     if not post:
#         return jsonify({'error': 'Post does not exist.'}, 400)
#     elif like:
#         db.session.delete(like)
#         db.session.commit()
#     else:
#         like = Like(author=current_user.id, post_id=post_id)
#         db.session.add(like)
#         db.session.commit()

#     return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})
