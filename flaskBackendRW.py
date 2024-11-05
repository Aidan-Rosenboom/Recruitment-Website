from flask import Flask, redirect, url_for, render_template, request, flash, redirect, session
from flask_bcrypt import Bcrypt
#import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "Aidan"
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = 'srv1356.hstgr.io'
app.config['MYSQL_USER'] = 'u612285796_root'
app.config['MYSQL_PASSWORD'] = 'ILoveMae123'
app.config['MYSQL_DB'] = 'u612285796_firstcohort'

mydb = MySQL(app)

"""mydb = mysql.connector.connect(
  host="srv1356.hstgr.io",
  user="u612285796_root",
  password="ILoveMae123",
  database="u612285796_firstcohort",
  pool_size= 5)"""

@app.route('/')
def home():
  return render_template('HomeRW.html',page='Home', foot = True)

@app.route('/Our_Program')
def ourProgram():
  return render_template('OurProgram.html',page='About', foot = True)

@app.route('/Minnpoly')
def minnpoly():
  return render_template('Minnpoly.html',page='About', foot = True)

@app.route('/Industry_Partners')
def indPart():
  return render_template('Indpart.html',page='About', foot = True)

@app.route('/Prerequisites/MSU')
def prereqMSU():
  return render_template('prereqMSU.html',page='Preq', foot = True)

@app.route('/Prerequisites/Courses')
def prereqCourses():
  return render_template('prereq.html',page='Preq', foot = True)

@app.route('/Apply')
def apply():
  return render_template('Application.html',page='Apply', foot = True)

@app.route('/Frequently_Asked_Questions')
def faq():
  return render_template('FAQRW.html',page='FAQ', foot = True)

@app.route('/Calendar')
def calendar():
  return render_template('Calendar.html', foot = False)

@app.route('/Profile')
def profile():
    return render_template('profile.html', page='Profile', foot = False)

@app.route('/Settings')
def accntSettings():
  return render_template("Settings.html", foot = False)

@app.route('/Login')
def login():
  foot = False
  return render_template('LoginRW.html', foot = False)

@app.route('/SignUp', methods=['GET','POST'])
def submit():
  foot = False
  cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
  #mydb.cursor()
  if request.method == 'POST':
    myform = request.form
    #gets the data from the signUp form
    firstName = myform['first']
    lastName = myform['last']
    email = myform['email']
    password = myform['password']
    #generates hashcode for the password entered
    hashPass = bcrypt.generate_password_hash(password).decode("utf-8")
    starId = myform['starid']
    phone = myform['phone']
    #cursor finds duplicate entries (if there are any)
    cursor.execute("SELECT email FROM profiles WHERE email = %s", (email,))
    dup = cursor.fetchone()
    #checks for duplicate email entries
    if dup:
      cursor.close()
      flash("You already have an account Please login.")
      return redirect(url_for('login'))
    else:
      #inserts the new entry into the profiles table in MySql
      cursor.execute("INSERT INTO profiles (first_name, last_name, phone, email, starid, password) VALUES (%s,%s,%s,%s,%s,%s)", ( firstName, lastName, phone, email, starId, hashPass))
      mydb.connection.commit()  #mydb.commit()
      #logs the user in, session uses email to identify who is signed in
      session['user'] = email
      session['first'] = firstName
      session['last'] = lastName
      session['phone'] = phone
      session['starId'] = starId
      cursor.close()
      #I want to look into changing the color of the flash box for this statement
      flash("Success: You're all signed up!")
      return redirect(url_for('home'))
  cursor.close()
  return render_template("SignUpRW.html", foot = False)

@app.route('/Logout')
def logout():
  session.pop('user', None)
  session.pop('first', None)
  session.pop('last', None)
  session.pop('phone', None)
  session.pop('starId', None)
  return redirect(url_for('home'))
  
if __name__ == '__main__':
  app.run(debug=True)
  #To show the footer in the template
  foot = True
