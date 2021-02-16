from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy.orm import session

app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)
app.secret_key = "test123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
sa_url = 'sqlite:///todo-list.db'

# Create table class object
class ToDo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(250), unique=False, nullable=False)

   def __repr__(self):
       return '<Item %r>' % self.title


# Adding entry
def add_entry(title):
    all_items = refresh_db()
    new_item = ToDo(id=len(all_items), title=title)
    db.session.add(new_item)
    db.session.commit()

# Update entry
def update_entry(item_id, title=None):
    item_to_update = ToDo.query.get(item_id)
    if title != None: item_to_update.title = title
    db.session.commit()

# Delete entry
def delete_entry(item_id):
    item_to_delete = ToDo.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()

# Get Item from ID
def get_item(item_id):
    item = ToDo.query.get(item_id)
    return item

# {"title": "To-Do Test Item"}
def refresh_db():
    return db.session.query(ToDo).all()

all_items = refresh_db()

@app.route('/')
def home():
    if request.method == "DELETE":
        delete_entry(request.form['id'])
    all_items = refresh_db()
    return render_template('index.html', items=all_items)


@app.route('/delete/<item_id>')
def delete(item_id):
    delete_entry(item_id)
    return redirect(url_for('home'))


@app.route("/add", methods=('GET', 'POST'))
def add():
    msg = ""
    if request.method == "POST":
        print("Test 01")
        item = {
            "title": request.form['title']
        }
        add_entry(request.form['title'])
        all_items = refresh_db()
        msg = f"item {item['title']} was successfully added."
    return render_template('add.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
