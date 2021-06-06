from re import M
from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import os
from flask_mail import Mail,Message
from decouple import config

app = Flask(__name__)
picFolder= os.path.join('static','image')

# below connection (4 lines) are used in xampp server running on MySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "users_db"
app.config['UPLOAD_FOLDER'] = picFolder
app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "rakeshofficial22@gmail.com"
app.config['MAIL_PASSWORD'] = config('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)

@app.route('/')
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'images.png')
    return render_template("index.html", user_image=pic1)

@app.route('/send_message', methods=['GET','POST'])
def send_message(): 

    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']

        # below cur are used for connection in xampp server running on MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_data (Username,Email_ID) VALUES (%s,%s)",(username,email))
        mysql.connection.commit()
        cur.close()
        
        subject = ' Hello ' +username
       # msg = 'hi' +username
        html  =  """<!DOCTYPE html>
                <html lang="en">
                <head>
                    <title>wel</title>
                </head>
                <body>
                    <h1> welcome to my new python project  </h1>
                    <h2>
                    <p> hey there, i just created my new python project  <br>
                    </p>
                    </h2>

                </body>
                </html>
             """
        message = Message(subject,recipients=[email], html=html, sender="rakeshofficial22@gmail.com",)
        mail.send(message)
        success = "thank you, Check your gmail inbox"
        return render_template("result.html",success=success)

if __name__ == '__main__':
    app.run(debug=True)
