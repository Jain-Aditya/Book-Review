# Project 1

Web Programming with Python and JavaScript

1. pip3 install -r requirements.txt
2. Set environment variable:
            export DATABASE_URL = <database_url>
3. to make the database tables go to python shell and do:
            from application import app,db
            with app.app_context():
                db.create_all()
