from flask import Flask, request , url_for , redirect , render_template

first=Flask(__name__)


@first.route('/')

def index():
    return render_template("doctor.html")

if __name__=="__main__":
    first.run()
