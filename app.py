from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            book_title = request.form.get("title")
            if book_title:
                book = Book(title=book_title)
                db.session.add(book)
                db.session.commit()
        except Exception as e:
            print("Failed to add book:", e)

    books = Book.query.all()
    return render_template("index.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        new_title = request.form.get("newtitle")
        old_title = request.form.get("oldtitle")
        book = Book.query.filter_by(title=old_title).first()
        if book:
            book.title = new_title
            db.session.commit()
        else:
            print("Book not found")
    except Exception as e:
        print("Couldn't update book title:", e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    if book:
        db.session.delete(book)
        db.session.commit()
    else:
        print("Book not found")
    return redirect("/")

@app.route("/animal/<title>", methods=["GET"])
def animal(title):
    book = Book.query.filter_by(title=title).first()
    if book:
        return render_template("animal.html", book=book)
    else:
        return "Animal não encontrado", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

    books = {
    "Old Name": {"title": "Old Name", "description": "Um animal incrível!", "species": "Alguma", "habitat": "Florestas e savanas"}
}

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/animal/<title>')
def animal_details(title):
    book = books.get(title)
    return render_template('animal_details.html', book=book)

@app.route('/update', methods=['POST'])
def update_name():
    old_title = request.form['oldtitle']
    new_title = request.form['newtitle']

    if old_title in books:
        books[new_title] = books.pop(old_title)
        books[new_title]['title'] = new_title

    return redirect(url_for('animal_details', title=new_title))

if __name__ == '__main__':
    app.run(debug=True)
