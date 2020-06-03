  
import os, sys, logging, time
import calendar
import time
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from bookpage import getbook
# from flask_marshmallow import Marshmallow
# from flask import Flask, request, jsonify
import models
from models import BOOK, USER, Base, RATING

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Base.query = db.query_property()
Base.metadata.create_all(bind=engine)

@app.route("/")
def index():
    if request.method == "GET":
        if session.get("username") is not None:
            return render_template("registration.html", headline= session["username"])
        return render_template("registration.html",headline="")


@app.route("/register", methods=["GET","POST"])
def response():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        info = USER(username=username,password=password,timestamp=calendar.timegm(time.gmtime()))
        try:
            db.add(info)
            db.commit()
            username += " registered. Please login."
            return render_template("registration.html",headline=username)
        except:
            text ="Account already exists!please try again with new account or login"
            return render_template("registration.html",headline=text)

    elif request.method == "GET":
        return render_template("registration.html",headline="")



@app.route("/search", methods=["GET","POST"])
def search():    
    if request.method == "POST":
        word = request.form['searchbox']
        choice = request.form['choice']
        if choice == "isbn":
            query = BOOK.query.filter(BOOK.isbn.like(f'%{word}%'))
        elif choice == "bname":
            query = BOOK.query.filter(BOOK.bname.like(f'%{word}%'))
        else:
            query = BOOK.query.filter(BOOK.author.like(f'%{word}%'))
        isbn = []
        bname = []
        author = []
        year = []
        for row in query:
            isbn.append(row.isbn)
            bname.append(row.bname)
            author.append(row.author)
            year.append(row.year)
        return render_template("results.html", isbn=isbn,bname=bname,author=author,year=year,length=len(isbn))
        
    elif request.method == "GET":
        return render_template("registration.html",headline="")


# @app.route("/bookpage", methods=["GET","POST"])
# def bookpage():
    # result = request.args.get('values')
    # # search = "%{}%".format(result)
    # search = BOOK.query.filter(BOOK.isbn.like(result))
    # isbn = []
    # bname = []
    # author = []
    # year = []
    # for row in search:
    #     isbn.append(row.isbn)
    #     bname.append(row.bname)
    #     author.append(row.author)
    #     year.append(row.year)
    # # query1 = RATING.query.filter_by(RATING.isbn=result)
    # query1=db.query(RATING).all()
    # print(result)
    # print(query1)
    # # print(query1[1].isbn)
    # isbn = []
    # # id=[]
    # username = []
    # rating = []
    # review = []
    # for row in query1:
    #     if row.isbn==result:
    #         # id.append(row.id)
    #         isbn.append(row.isbn)
    #         username.append(row.username)
    #         rating.append(row.rating)
    #         review.append(row.review)
    # return render_template("bookpage.html", isbn=isbn,bname=bname,author=author,year=year,rating=rating,review=review,username=username,length=len(isbn),length1=len(rating))

@app.route("/api/bookpage",methods = ["POST"])
def apibookpage():
    isbn = request.form.get("isbn")
    bookreturned = getbook(isbn) 
    Bookdetails = {}
    Bookdetails["isbn"] = bookreturned[0].isbn
    Bookdetails["title"] = bookreturned[0].title
    Bookdetails["author"] = bookreturned[0].author
    Bookdetails["year"] = bookreturned[0].year
    return jsonify({"bookinfo":Bookdetails})

@app.route("/api/review",methods = ["POST"])
def apibookpagereview():
   username = session["username"]
   isbn = request.form.get("isbn")
   query = db.query(RATING).filter_by(isbn=isbn).first()
   tot_reviews = {}
   for i in query:
       tot_reviews[i.username] = [i.isbn,i.review,i.rating] 
   print(tot_reviews)
   return jsonify({'total_review': tot_reviews})

# @app.route("/rating", methods=["GET","POST"])
# def rating():     
    # # review = request.form['message']
    # # rating = request.form['choice']
    # username = session["username"]
    # result = request.args.get('values')
    # # return review
    # query = db.query(RATING).filter_by(isbn=result, username=username).first()
    # session["isbn"]=result
    # # query = RATING.query.filter(RATING.isbn.like(f'%{result}%'),RATING.username.like(f'%{session["username"]}%'))
    # if query is not None:
    #     select = RATING.query.filter(RATING.isbn.like(f'%{result}%'),RATING.username.like(f'%{session["username"]}%'))
    #     isbn = []
    #     username = []
    #     rating = []
    #     review = []
    #     for row in select:
    #         isbn.append(row.isbn)
    #         username.append(row.username)
    #         rating.append(row.rating)
    #         review.append(row.review)
    #     return render_template("review.html", isbn=isbn,username=username,rating=rating,review=review,length=len(isbn))
    # else:
    #     query = BOOK.query.filter(BOOK.isbn.like(f'%{result}%'))
    #     isbn = []
    #     bname = []
    #     author = []
    #     year = []
    #     for row in query:
    #         isbn.append(row.isbn)
    #         bname.append(row.bname)
    #         author.append(row.author)
    #         year.append(row.year)
    #     return render_template("rating.html", isbn=isbn,bname=bname,author=author,year=year,length=len(isbn))

        
        
# @app.route("/review", methods=["GET","POST"])
# def review():
    # review = request.form['message']
    # rating = request.form['choice']
    # username = session["username"]
    # result = request.args.get('values')
    # # return result      
    # info = RATING(isbn=result,username=username,rating=rating,review=review)
    # db.add(info)
    # db.commit()
    # headline="Successfully added your review"
    # return render_template("search.html", headline = headline)
        

@app.route("/auth", methods=["GET","POST"])
def authentication():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        query = db.query(USER).filter_by(username=username, password=password).first()
        if query is None:
            return render_template("registration.html", headline="WRONG CREDENTIALS")
        else:
            print(query)
            session["username"] = username
            return render_template("search.html", headline=" welcome "+session["username"])
        

    elif request.method == "GET":
        return redirect("register")

@app.route("/admin")
def database():
    users = USER.query.order_by(USER.timestamp).all()
    username = []
    password = []
    stamps = []
    for i in users:
        username.append(i.username)
        password.append(i.password)
        stamps.append(time.ctime(i.timestamp))
    return render_template("database.html", username=username,password=password,stamps=stamps,length=len(username))



@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/")


