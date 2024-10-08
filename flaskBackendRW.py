from flask import Flask, redirect, url_for, render_template, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="srv1356.hstgr.io",
  user="u612285796_root",
  password="ILoveMae123",
  database="u612285796_firstcohort")

@app.route('/')
def home():
  return render_template('HomeRW.html',page='Home')

@app.route('/Our_Program')
def ourProgram():
  return render_template('OurProgram.html',page='About')

@app.route('/Minnpoly')
def minnpoly():
  return render_template('Minnpoly.html',page='About')

@app.route('/Industry_Partners')
def indPart():
  return render_template('Indpart.html',page='About')

@app.route('/Prerequisites/MSU')
def prereqMSU():
  return render_template('prereqMSU.html',page='Preq')

@app.route('/Prerequisites/Courses')
def prereqCourses():
  return render_template('prereq.html',page='Preq')

@app.route('/Apply')
def apply():
  return render_template('Application.html',page='Apply')

@app.route('/Frequently_Asked_Questions')
def faq():
  return render_template('FAQRW.html',page='FAQ')

@app.route('/Calendar')
def calendar():
  return render_template('Calendar.html')

@app.route('/Login')
def login():
  return render_template('LoginRW.html')

@app.route('/SignUp')
def signUp():
  return render_template('SignUpRW.html')

#student submit also add a faculty submit function
@app.route('/Submit', methods=['POST'])
def submit():
  if request.method == 'POST':
    myform = request.form
    firstName = myform['first']
    lastName = myform['last']
    email = myform['email']
    password = myform['password']
    starId = myform['starid']
    phone = myform['phone']
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO student (first_name, last_name, phone, email, starid, password) VALUES (%s,%s,%s,%s,%s,%s)", (firstName, lastName, phone, email, starId, password))
    mydb.commit()
    cursor.close()
    return "Success"
  
if __name__ == '__main__':
  app.run(debug=True)
