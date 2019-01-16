import csv
from models import Book,db
from application import app

def main():
    f=open('books.csv')
    reader=csv.reader(f)
    for isbn,title,author,year in reader:
        new_book = Book(isbn=isbn,title=title,author=author,year=year)
        db.session.add(new_book)
        db.session.commit()

if __name__=="__main__":
    with app.app_context():
        main()

    