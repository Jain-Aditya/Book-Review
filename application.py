import os
from flask import Flask,render_template,request,session,redirect,url_for
from models import *
import sqlalchemy
import requests
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key='fiwgcbbkdvjakbvufdbj'
db.init_app(app)
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method=="POST":               #Create an account
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template("index.html")
        except sqlalchemy.exc.IntegrityError:
            return "user name already exists"
    else:
        if 'user_id' in session:
            session.pop('user_id',None)
        return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    searched_user = User.query.get(username)
    if searched_user is None:
        return "User does not exist"
    if searched_user.password == password: 
        session['user_id']=username
        return redirect(url_for('dashboard'))    
    else:
        return "Password or Username is incorrect"

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    return render_template("dashboard.html",username=session['user_id'])       

@app.route("/dashboard/books", methods=["POST"])
def books():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    isbn=request.form.get("isbn")
    author=request.form.get("author")

    fetched_book = Book.query.get(isbn)
    fetched_books = Book.query.filter_by(author=author).all()
    if not fetched_books and fetched_book is None:
        return "We can not find any books"
    elif fetched_book is not None:
        return render_template("books.html",book_list=fetched_books,book_by_isbn=fetched_book)
    else:
        return render_template("books.html",book_list=fetched_books) 

@app.route("/dashboard/books/<string:isbn>", methods=["GET","POST"])
def details(isbn):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    if(request.method=="POST"):
        review=request.form.get("review")
        new_review= Reviews(review_text=review,book_isbn=isbn)
        db.session.add(new_review)
        db.session.commit()
    
    res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":"wb8xMHRzeWVPoKgjvvdw", "isbns":isbn})
    data = res.json()
    

    fetched_book=Book.query.get(isbn)
    fetched_reviews=Reviews.query.filter_by(book_isbn=isbn).all()
    return render_template("details.html",book=fetched_book,reviews=fetched_reviews,avg_rating=data['books'][0]['average_rating'],num_ratings=data['books'][0]['work_ratings_count'])
 
if __name__ == "__main__":
    app.run(debug=True)