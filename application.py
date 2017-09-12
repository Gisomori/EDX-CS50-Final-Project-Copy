from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import pandas as pd
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    # if request.method == "POST":
    session['user_id']
    exis_stocks = db.execute("select symbol, name, sum(shares) shares from transactions where userid = :userid \
                              group by symbol, name",userid=session['user_id'])
    for i in range(len(exis_stocks)):
        cur_price = lookup(exis_stocks[i]['symbol'])
        exis_stocks[i]['price'] = cur_price['price']
        exis_stocks[i]['total'] = exis_stocks[i]['price'] * exis_stocks[i]['shares']

    cash = db.execute('select cash from users where id = :userid',userid=session['user_id'])
    total = pd.DataFrame(exis_stocks)
    print(total)
    print(cash)
    print(exis_stocks)
    if total.empty == False:
        total = total.total.sum() + cash[0]['cash']
        print(total)
        return render_template('index.html',stocks = exis_stocks, cash=cash,total = total)
    else:
        total = cash[0]['cash']
        return render_template('index.html',cash = cash, total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please insert symbol :(")
        data = lookup(request.form.get("symbol"))
        if data is None:
            return apology("INVALID SYMBOL")
        elif not request.form.get("shares"):
            return apology("Please insert share amount")
        elif request.form.get("shares").isnumeric():
            try:
                if int(request.form.get("shares")) < 0:
                    return apology("Positive Amount of shares please")
            except ValueError:
                return apology("damn still invalid :(")

            costs= round(data['price'] * int(request.form.get("shares")),2)
            print(session['user_id'])
            cash =db.execute('select cash from users where id = :id',id = session["user_id"])
            cash = cash[0]['cash']
            if cash >= costs:
                left_over = cash - costs
                db.execute('update users set cash = :cash where id = :id',cash=left_over, id=session["user_id"])
                db.execute('insert into transactions (name, symbol, shares, price, total_transaction,userid,type) \
                            values(:name,:symbol,:shares,:price,:total_transaction,:userid,:type)',name=data['name'],symbol =data['symbol'], \
                            shares = request.form.get('shares'),price = data['price'],total_transaction=costs,userid = session["user_id"],type='buy')
                flash('You bought successfully')
                return index()
            else:
                return apology("Not enough cash : (")
        return apology("Shares should be a positive integer")

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():

    transactions = db.execute('select * from transactions where userid = :userid', userid = session['user_id'])
    return render_template("history.html",transactions =transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        else:
            data = lookup(request.form.get("symbol"))
        if data is None:
            return apology("INVALID SYMBOL")
        else:
            print(data)
            iterator = len(data)
            return render_template("quoted.html",stats=data,ite = iterator)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        existing_users = pd.DataFrame(db.execute('select * from users'))
        if not request.form.get("username"):
            return apology("must provide username")
        if not existing_users.empty:
            if any(existing_users.username==request.form.get("username")):
                return apology("username already in use")
        # ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")
        elif request.form.get("password") != request.form.get("rpassword"):
            return apology("password has to be the same : (")
        else:
            db.execute('insert into users (username, hash) values(:username, :hash)',username=request.form.get("username"),hash=pwd_context.hash(request.form.get("rpassword")))

            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

            # ensure username exists and password is correct
            if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
                return apology("invalid username and/or password")

            # remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # redirect user to home page
            flash("You are registered")
            return redirect(url_for("index"))

    return render_template('register.html')

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":
        exis_stocks = db.execute("select symbol, name, sum(shares) shares from transactions where userid = :userid \
                              group by symbol, name",userid=session["user_id"])
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("No shares or Symbol invalid/empty")
        if request.form.get("shares").isnumeric():
            try:
                if int(request.form.get("shares")) < 0:
                    return apology("Positive Amount of shares please")
            except ValueError:
                return apology("damn still invalid :(")

            exis_stocks_pd = pd.DataFrame(exis_stocks)
            if any(exis_stocks_pd.symbol == request.form.get("symbol")):

                check = exis_stocks_pd.symbol == request.form.get("symbol")
                print("first stage")
                if int(exis_stocks_pd[check]['shares']) >= int(request.form.get('shares')):
                    print("second stage")
                    data = lookup(request.form.get('symbol'))
                    costs= round(data['price'] * int(request.form.get("shares")),2)
                    print("third stage")
                    db.execute('update users set cash = cash + :costs where id = :id',costs=costs, id=session["user_id"])
                    db.execute('insert into transactions (name, symbol, shares, price, total_transaction,userid, type) \
                                values(:name,:symbol,:shares,:price,:total_transaction,:userid,:type)',name=data['name'],symbol =data['symbol'], \
                                shares = -int(request.form.get('shares'))  ,price = data['price'],total_transaction=costs,userid = session["user_id"],type="sell")
                    flash('You sold successfully')
                    return index()
                else:
                    return apology("Not enough shares of symbol" + request.form.get('symbol'))

            else:
                return apology("User does not own this stock")
        else:
            return apology("Shares should be a positive integer")
    return render_template("sell.html")

@app.route('/register_sucess')
def reg_sucess():
    return render_template('register_sucess.html')

@app.route('/quoted')
@login_required
def quoted():
    return render_template('quoted.html')


@app.route('/topup',methods=["GET", "POST"])
@login_required
def topup():
    if request.method == "POST":
        if not request.form.get("balance"):
            return apology("Field should not be empty")
        if request.form.get("balance").isnumeric()==False:
            return apology("Field should be numeric")
        if request.form.get("balance").isnumeric()==True and int(request.form.get("balance")) > 0:
            topup = int(request.form.get("balance"))
            db.execute('update users set cash = cash + :topup where id = :id',topup=topup, id=session["user_id"])
            flash("Balance topped up")
            return index()
        else:
            return apology("Please use positive numbers")

    else:
        return render_template('topup.html')