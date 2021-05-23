import urllib.request
import json
from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

account = {"admin": "password"}
books = []

def main():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""SELECT * FROM books""")
    book_list = c.fetchall()
    return book_list

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register_form")
def register_form():
    return render_template("registry.html")

@app.route("/search_form")
def search_form():
    book_list = main()
    return render_template("search.html", books=book_list)

@app.route("/register", methods=["POST"])
def register():
    if request.method == 'POST':
        user_name = request.form['create_user_name']
        password = request.form['create_password']
        account[user_name] = password
        return redirect("/")

@app.route('/sign_in', methods=["POST"])
def submit():
    user_name = request.form['fuser_name']
    password = request.form['fpassword']
    key_validation = str(user_name in account)

    if key_validation == 'True':
        if account[user_name] == password:
            return redirect("search_form")
        # return render_template("search.html", username=user_name)
    else:
        return redirect("register_form")

@app.route("/add", methods=["POST"])
def add():
    ISBN = request.form['ISBN']
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    user_input = ISBN.strip()
    # 9781449357351
    with urllib.request.urlopen(api + user_input) as f:
        text = f.read().decode("utf-8")

    obj = json.loads(text)

    title = (obj["items"][0]["volumeInfo"]["title"])
    authors = (obj["items"][0]["volumeInfo"]["authors"])
    pageCount = (obj["items"][0]["volumeInfo"]["pageCount"])
    averageRating = (obj["items"][0]["volumeInfo"]["averageRating"])
    if averageRating is None:
        averageRating = Null

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    sql = "INSERT INTO books (ISBN, Title, Authors, PageCount, AverageRating) VALUES (?, ?, ?, ?, ?)"
    val = (ISBN, str(title), str(authors), str(pageCount), str(averageRating))

    c.execute(sql, val)
    conn.commit()

    return redirect(url_for('search_form'))

@app.route("/delete", methods=["POST"])
def delete():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    ISBN = request.form["Delete_ISBN"]
    sql = "DELETE FROM books WHERE ISBN={}".format(ISBN)
    c.execute(sql)
    conn.commit()
    return redirect(url_for('search_form'))

if __name__ == '__main__':
    app.run(debug=True)
    main()
