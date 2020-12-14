from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///friends.db'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:ssss1234@localhost/new_db'
db = SQLAlchemy(app)
app.debug = True


# create database model with 2 columns
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # nullable = False means cannot enter blank name
    date_created = db.Column(db.DateTime, default=datetime.utcnow())


@app.route('/', methods=['GET', 'POST'])
def hello():
    return redirect('/friends')


@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if request.method == 'POST':
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except Exception as e:
            return str(e)

    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('index.html', friends=friends)


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except Exception as e:
            return str(e)
    else:
        return render_template('update.html', friend_to_update=friend_to_update)


@app.route('/delete/<id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
