from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import string
import random

# CONNECTING TO URLS DATABASE
app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="harshildave",
    password="Database1",
    hostname="harshildave.mysql.pythonanywhere-services.com",
    databasename="harshildave$urls",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# URL CLASS
class Url(db.Model):
    __tablename__ = "urls"
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long_ = db.Column("long_", db.String(512))
    short = db.Column("short", db.String(3))

    def __init__(self, long_, short):
        self.long_ = long_
        self.short = short

# FUNCTION THAT SHORTENS THE URL
def shorten_url():
    letters = string.ascii_letters
    while True:
        random_letters = random.choices(letters, k=3)
        random_letters = "".join(random_letters)
        short_url = Url.query.filter_by(short=random_letters).first()
        if not short_url:
            return random_letters

# POST/GET METHOD
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        original_url = request.form["nm"]
        url_found = Url.query.filter_by(long_= original_url).first()

# CHECKS IF URL IS ALREADY IN DATABASE AND RETURNS IF IT IS FOUND
        if url_found:
            return f"{url_found.short}"

# IF URL IS NOT IN DATABASE, CREATE A NEW SHORTENED URL
        else:
            shortened_url = shorten_url()
            print(shortened_url)
            new_url = Url(original_url, shortened_url)
            db.session.add(new_url)
            db.session.commit()
            return shortened_url
    else:
        return render_template("main_page.html", urls=Url.query.all())

# REDIRECTING TO ORIGINAL LINK
@app.route('/<shortened_url>')
def redirection(shortened_url):
    long_url = Url.query.filter_by(short=shortened_url).first()
    if long_url:
        return redirect(long_url.long_)
    else:
        return f'<h1>URL DOES NOT EXIST</h1>'
