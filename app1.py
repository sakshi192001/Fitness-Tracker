from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors
import re
import datetime
from datetime import datetime
from datetime import date
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'miniproject'

# Intialize MySQL
mysql = MySQL(app)
plan={
    "arm":{
        "barm":{
           "name":["JUMPING JACK","INCLINE PUSH-UPS","BOX PUSH-UPS","PUSH-UPS","DECLINE PUSH-UPS","KNEE PUSH-UPS","SHOULDER STRETCH","COBRA STRETCH"],
           "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8"],
           "imgs" :["/static/img/Jumping Jacks.png","/static/img/Incline push up.png","/static/img/box push up.jpg","/static/img/push up.png","/static/img/decline push ups.jpg","/static/img/knee push ups.png","/static/img/shoulder stretch.jpg","/static/img/cobra stretch.jpg"]
        },
        "iarm":{
           "name":["JUMPING JACK","INCLINE PUSH-UPS","WIDE ARM PUSH-UPS","PUSH-UPS & ROTATION","STAGGERED PUSH-UPS","DECLINE PUSH-UPS","WIDE ARM PUSH-UPS","PUSH-UPS & ROTATION","STAGGERED PUSH-UPS","DECLINE PUSH-UPS","COBRA STRETH","CHEST STRETCH"],
           "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12"],
           "imgs" :["/static/img/Jumping Jacks.png","/static/img/Incline push up.png","/static/img/wide arm push ups.jpg","/static/img/push up and rotation.jpg","/static/img/staggered push ups.jpg","/static/img/decline push ups.jpg","/static/img/wide arm push ups.jpg","/static/img/push up and rotation.jpg","/static/img/staggered push ups.jpg","/static/img/decline push ups.jpg","/static/img/cobra stretch.jpg","/static/img/chest stretch.jpg"]
        },
        "aarm":{
           "name":["JUMPING JACKS","ARM CIRCLES","SHOULDER STRETCH","BURPEES","PUSH-UPS","PUSH-UPS & ROTATION","DIAMOND PUSH-UPS","SPIDERMAN PUSH-UPS","PUSH-UPS","PUSH-UPS & ROTATION","DECLINE PUSH-UPS","HINDU PUSH-UPS","DIAMOND PUSH-UPS","SPIDERMAN PUSH-UPS","SHOULDER STRETCH","COBRA STRETCH","CHEST STRETCH"],
           "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12","ex13","ex14","ex15","ex16","ex17"],
           "imgs" :["/static/img/Jumping Jacks.png","/static/img/arm circles.jpg","/static/img/shoulder stretch.jpg","/static/img/burpees.png","/static/img/push up.png","/static/img/push up and rotation.jpg","/static/img/diamond push ups.png","/static/img/spiderman push ups.jpg","/static/img/push up.png","/static/img/push up and rotation.jpg","/static/img/decline push ups.jpg","/static/img/hindu push ups.jpg","/static/img/diamond push ups.png","/static/img/spiderman push ups.jpg","/static/img/shoulder stretch.jpg","/static/img/cobra stretch.jpg","/static/img/chest stretch.jpg"]
        }
    },
    "abs":{
        "babs":{
            "name":["JUMPING JACKS","ABDOMINAL CRUNCHES","MOUNTAIN CLIMBER","HEEL TOUCH","PLANK","COBRA STRETCH","SPINE LUMBAR STRETCH LEFT","SPINE LUMBAR STRETCH RIGHT"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/abdominal crutch.jpg","/static/img/mountain climbers.png","/static/img/heel touches.png","/static/img/plank.png","/static/img/cobra stretch.jpg","/static/img/spine lumbar stretch.jpg","/static/img/spine lumbar stretch.jpg"]
        },
        "iabs":{
            "name":["JUMPING JACKS","ABDOMINAL CRUNCHES","RUSSIAN TWIST","PLANK","BUTT BRIDGE","CROSSOVER CRUNCHES","SIDE BRIDGE LEFT","SIDE BRIDGE RIGHT","BICYCLE CRUNCHES","ABDOMINAL CRUNCHES","RUSSIAN TWIST","PLANK","SIDE BRIDGE RIGHT","SIDE BRIDGE LEFT","BICYCLE CRUNCHES","PUSH-UPS & ROTATION","COBRA STRETCH","SPINE LUMBAR STRETCH LEFT","SPINE LUMBAR STRETCH RIGHT"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12","ex13","ex14","ex15","ex16","ex17","ex18","ex19"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/abdominal crutch.jpg","/static/img/russian twist.jpg","/static/img/plank.png","/static/img/butt bridge.jpg","/static/img/crossover crunches.jpg","/static/img/side bridge.jpg","/static/img/side bridge.jpg","/static/img/bicycle crutches.png","/static/img/abdominal crutch.jpg","/static/img/russian twist.jpg","/static/img/plank.png","/static/img/side bridge.jpg","/static/img/side bridge.jpg","/static/img/bicycle crutches.png","/static/img/push up and rotation.jpg","/static/img/cobra stretch.jpg","/static/img/spine lumbar stretch.jpg","/static/img/spine lumbar stretch.jpg"]
        },
        "aabs":{
            "name":["JUMPING JACKS","SIT-UPS","RUSSIAN TWIST","PLANK","CROSSOVER CRUNCH","SIDE BRIDGE RIGHT","SIDE BRIDGE LEFT","BICYCLE CRUNCHES","V-UPS","RUSSIAN TWIST","PLANK","BUTT BRIDGE","CROSSOVER CRUNCH","SIDE BRIDGE RIGHT","SIDE BRIDGE LEFT","BICYCLE CRUNCHES","V-UPS","PUSH-UPS & ROTATION","COBRA STRETCH","SPINE LUMBAR STRETCH RIGHT","SPINE LUMBAR STRETCH LEFT"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12","ex13","ex14","ex15","ex16","ex17","ex18","ex19","ex20","ex21"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/crunches.png","/static/img/russian twist.jpg","/static/img/plank.png","/static/img/crossover crunches.jpg","/static/img/side bridge.jpg","/static/img/side bridge.jpg","/static/img/bicycle crutches.png","/static/img/v ups.jpg","/static/img/russian twist.jpg","/static/img/plank.png","/static/img/butt bridge.jpg","/static/img/crossover crunches.jpg","/static/img/side bridge.jpg","/static/img/side bridge.jpg","/static/img/bicycle crutches.png","/static/img/v ups.jpg","/static/img/push up and rotation.jpg","/static/img/cobra stretch.jpg","/static/img/spine lumbar stretch.jpg","/static/img/spine lumbar stretch.jpg"]
        }
    },
    "back":{
        "bback":{
            "name":["JUMPING JACKS","ARM RAISES","RHOMBOID PULLS","SIDE ARM RAISE","KNEE PUSH-UPS","SIDE-LYING STRETCH LEFT","SIE-LYING STRETCH RIGHT","CAT COW POSE","CHILD'S POSE"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png"]
        },
        "iback":{
            "name":["JUMPING JACKS","SIDE ARM RAISE","TRICEP KICKBACKS","INCLINE PUSH-UPS","HYPEREXTENSION","SIDE-LYING STRETCH LEFT","SIDE-LYING STRETCH RIGHT","SIDE ARM RAISE","INCHWORMS","TRICEP KICKBACKS","INCLINE PUSH-UPS","HYPEREXTENSION","CAT COW POSE","RECLINED RHOMBOID SQUEEZES","SUPINE PUSH-UPS","RECLINED RHOMBOID SQUEEZES","SUPINE PUSH-UPS","CHILD'S POSE"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12","ex13","ex14","ex15","ex16","ex17","ex18"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png"]
        },
        "aback":{
            "name":["JUMPING JACKS","FLOOR TRICEP DIPS","PIKE PUSH-UPS","REVERSE PUSH-UPS","SIDE-LYING STRETCH LEFT","SIDE-LYING STRETCH RIGHT","FLOOR TRICEP DIPS","PIKE PUSH-UPS","REVERSE PUSH-UPS","CAT COW POSE","SUPINE PUSH-UPS","HYPEREXTENSION","HOVER PUSH-UPS","REVERSE SNOW ANGELS","SUPINE PUSH-UPS","HYPEREXTENSION","HOVER PUSH-UPS","REVERSE SNOW ANGELS","CHILD'S POSE"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12","ex13","ex14","ex15","ex16","ex17","ex18","ex19"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png"]
        }
    },
    "legs":{
        "blegs":{
            "name":["JUMPING JACKS","SQUATS","SIDE-LYING LEG LIFT LEFT","SIDE-LYING LEG LIFT RIGHT","SIDE LUNGES","DONKEY KICKS LEFT","DONKEY KICKS RIGHT","LEFT QUAD STRETCH","RIGHT QUAD STRETCH","CALF RAISES","CALF STRETCH LEFT","CALF STRETCH RIGHT"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png"]
        },
        "ilegs":{
            "name":["HIGH STEPPING","SQUATS","DONKEY KICK LEFT","DONKEY KICK RIGHT","PILE SQUATS","SIDE-LEG CIRCLES LEFT","SIDE-LEG CIRCLES RIGHT","LEFT QUAD STRETCH","RIGHT QUAD STRETCH","LYING BUTTERFLY STRETCH","CALF RAISES","SINGLE LEG CALF HOP LEFT","SINGLE CALF HOP RIGHT","CALF STRETCH LEFT","CALF STRETCH RIGHT"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12","ex13","ex14","ex15"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png"]
        },
        "alegs":{
            "name":["HIGH STEPPING","PILE SQUATS","SIDE LEG CIRCLES LEFT","SIDE LEG CIRCLES RIGHT","SUMO SQUATS","FIRE HYDRANT","BURPEES","JUMPING SQUATS","GLUTE KICK BACK LEFT","GLUTE KICK BACK RIGHT","WALL SIT","ADDUCTOR STRETCH","LEFT QUAD STRETCH","RIGHT QUAD STRETCH","LYING BUTTERFLY STRETCH","CALF RAISE WITH SPLAYED FOOT","CALF RAISE WITH PIGEON-TOED FOOT","CALF STRETCH LEFT","CALF STRETCH RIGHT"],
            "links":["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10","ex11","ex12","ex13","ex14","ex15","ex16","ex17","ex18","ex19"],
            "imgs" :["/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png","/static/img/Jumping Jacks.png"]
        }
    }
}

food = {
  "egg omelette": 207,
  "besan oats chilla": 99,
  "maggi": 296,
  "vegetable sandwich": 220,
  "masala oats": 119,
  "poha": 195,
  "cornflakes": 114,
  "oatmeal": 250,
  "dosa": 154,
  "idli": 78,
  "uttapa": 226,
  "bread pakoda": 282,
  "tofu scramble": 173,
  "upma": 171,
  "half fry": 127,
  "chickoo": 58,
  "banana": 54 ,
  "orange": 31 ,
  "coffee with milk": 135,
  "black coffee": 30 ,
  "toned milk": 92,
  "watermelon juice": 80,
  "watermelon": 24 ,
  "mango": 122,
  "protein shake": 250,
  "kelloggs cornflakes":114 ,
  "soya sticks": 67 ,
  "chocolate":100 ,
  "aloo bhujia": 98,
  "potato chips":120 ,
  " tur daal":134,
  "white rice ":120 ,
  "brown rice":80 ,
  "wheat roti ":85 ,
  "maida poori":196 ,
  "vegetable pulav": 133,
  "raita": 67,
  "aloo paratha":220 ,
  "cucumber salad":40 ,
  "aloo matar sabzi": 129,
  "paneer sabzi": 160,
  "karela sabzi":70,
  "ladyfinger sabzi":98 ,
  "curd": 50,
  "papad ":30 ,
}
run_with_ngrok(app)
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('signup'))

@app.route('/', methods=["GET","POST"])
def signup():
    msg=''
    if request.method=="POST" and request.form['sign-in'] == 'Sign Up':
        if 'username' in request.form and 'password' in request.form and 'email' in request.form and 'age' in request.form and 'height' in request.form and 'weight' in request.form and 'target' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            age = request.form['age']
            height = request.form['height']
            weight = request.form['weight']
            target = request.form['target']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM entries WHERE username = %s', [username])
            account = cursor.fetchone()
            if target=="Weight Gain":
                total_c=2400
                brk_cal=600
                snack_cal=300
            elif target=="Weight Loss":
                total_c=1600
                brk_cal=400
                snack_cal=200
            else:
                total_c=2000
                brk_cal=500
                snack_cal=250
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO entries VALUES (%s, %s, %s, %s, %s, %s, %s)', (username, email, password, age, height, weight, target))
                cursor.execute('INSERT INTO calories (Username) SELECT Username FROM entries WHERE Username=%s', [username])
                cursor.execute('INSERT INTO total_calories (Username) SELECT Username FROM entries WHERE Username=%s', [username])
                cursor.execute('UPDATE total_calories SET Total_Calories=%s WHERE Username=%s', [total_c,username])
                cursor.execute('UPDATE calories SET total_breakfast=%s, total_morning_snack=%s, total_lunch=%s,total_evening_snack=%s, total_dinner=%s WHERE Username=%s', [brk_cal,snack_cal,brk_cal,snack_cal,brk_cal,username])
                # cursor.execute('INSERT INTO details (Age, Height, Weight, Target) VALUES (%s, %s, %s, %s) WHERE Username=%s', (age,height,weight,target,username))
                mysql.connection.commit()
                session['loggedin'] = True
                session['Username'] = username
                msg = 'You have successfully registered!'
                return redirect(url_for('home'))
        else:
            msg='Fill out the form!'
    elif request.method=="POST" and request.form['sign-in'] == 'Sign In':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM entries WHERE Username = %s AND Password = %s', [username, password])
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['Username'] = account['Username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
    return render_template("signup.html",msg=msg)

@app.route('/profile', methods=["GET","POST"])
def profile():
    uid=session['Username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM entries WHERE Username = %s', [uid])
    details=cursor.fetchone()
    weight=details['Weight']
    height=details['Height']
    goal=details['Target']
    email=details['Email']
    BMI1 =weight*10000/(height**2)
    BMI = round(BMI1,2)
    if request.method=="POST":
        if "weight" in request.form:
            upweight=request.form["weight"]
            weight=details['Weight']
            height=details['Height']
            goal=details['Target']
            email=details['Email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE entries SET Weight=%s,Height=%s,Email=%s,Target=%s WHERE Username=%s',[upweight,height,email,goal,uid])
            mysql.connection.commit()
            print(upweight,height,email,goal,uid)
        if "height" in request.form:
            upheight=request.form["height"]
            weight=details['Weight']
            height=details['Height']
            goal=details['Target']
            email=details['Email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE entries SET Weight=%s,Height=%s,Email=%s,Target=%s WHERE Username=%s',[weight,upheight,email,goal,uid])
            mysql.connection.commit()
        if "goal" in request.form:
            upgoal=request.form["goal"]
            weight=details['Weight']
            height=details['Height']
            goal=details['Target']
            email=details['Email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE entries SET Weight=%s,Height=%s,Email=%s,Target=%s WHERE Username=%s',[weight,height,email,upgoal,uid])
            mysql.connection.commit()
        if "email" in request.form:
            upemail=request.form["email"]
            weight=details['Weight']
            height=details['Height']
            goal=details['Target']
            email=details['Email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE entries SET Weight=%s,Height=%s,Email=%s,Target=%s WHERE Username=%s',[weight,height,upemail,goal,uid])
            mysql.connection.commit()
            print(weight,height,upemail,goal,uid)
    return render_template("profile.html",uid=uid,weight=weight,height=height,goal=goal,email=email,BMI=BMI)


@app.route('/home', methods=["GET","POST"])
def home():
    levels=["Nutrition", "Workout", "Blogs"]
    links=["/nutrition", "/workout", "/blogs"]
    imgs=["/static/img/images.jpg", "/static/img/fit.jpg", "/static/img/blogs.jpg"]
    return render_template("home.html",links_imgs=zip(links,imgs,levels))

@app.route('/workout', methods=["GET","POST"])
def workout():
    return render_template("workout.html")

@app.route('/brkfast', methods=["GET","POST"])
def hello():
    tdate = date.today()
    total_calo=0
    brk=food
    if request.method=="POST":
        lst=request.form.getlist('food')
        for i,j in enumerate(lst):
            if j!="0":
                num=lst[i]
                calo=list(food.values())[i]
                total_calo+=int(num)*int(calo)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE calories SET breakfast=%s,date_=%s WHERE Username=%s', [total_calo,tdate,session['Username']])
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT calories FROM total_calories WHERE Username=%s', [session['Username']])
        abc=list(cursor.fetchone().values())[0]
        if abc==None:
            abc=0
        abc=int(abc)+total_calo
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE total_calories SET calories=%s WHERE Username=%s', [abc,session['Username']])
        mysql.connection.commit()
        return redirect(url_for('nutrition'))
    return render_template("food.html",brk=brk)

@app.route('/mornsnack', methods=["GET","POST"])
def mornsnack():
    total_calo=0
    brk=food
    if request.method=="POST":
        lst=request.form.getlist('food')
        for i,j in enumerate(lst):
            if j!="0":
                num=lst[i]
                calo=list(food.values())[i]
                total_calo+=int(num)*int(calo)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE calories SET morning_snack=%s WHERE Username=%s', [total_calo,session['Username']])
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT calories FROM total_calories WHERE Username=%s', [session['Username']])
        abc=list(cursor.fetchone().values())[0]
        if abc==None:
            abc=0
        abc=int(abc)+total_calo
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE total_calories SET calories=%s WHERE Username=%s', [abc,session['Username']])
        mysql.connection.commit()
        return redirect(url_for('nutrition'))
    return render_template("food.html",brk=brk)

@app.route('/lunch', methods=["GET","POST"])
def lunch():
    total_calo=0
    brk=food
    if request.method=="POST":
        lst=request.form.getlist('food')
        for i,j in enumerate(lst):
            if j!="0":
                num=lst[i]
                calo=list(food.values())[i]
                total_calo+=int(num)*int(calo)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE calories SET lunch=%s WHERE Username=%s', [total_calo,session['Username']])
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT calories FROM total_calories WHERE Username=%s', [session['Username']])
        abc=list(cursor.fetchone().values())[0]
        if abc==None:
            abc=0
        abc=int(abc)+total_calo
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE total_calories SET calories=%s WHERE Username=%s', [abc,session['Username']])
        mysql.connection.commit()
        return redirect(url_for('nutrition'))
    return render_template("food.html",brk=brk)

@app.route('/evesnack', methods=["GET","POST"])
def evesnack():
    total_calo=0
    brk=food
    if request.method=="POST":
        lst=request.form.getlist('food')
        for i,j in enumerate(lst):
            if j!="0":
                num=lst[i]
                calo=list(food.values())[i]
                total_calo+=int(num)*int(calo)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE calories SET evening_snack=%s WHERE Username=%s', [total_calo,session['Username']])
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT calories FROM total_calories WHERE Username=%s', [session['Username']])
        abc=list(cursor.fetchone().values())[0]
        if abc==None:
            abc=0
        abc=int(abc)+total_calo
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE total_calories SET calories=%s WHERE Username=%s', [abc,session['Username']])
        mysql.connection.commit()
        return redirect(url_for('nutrition'))
    return render_template("food.html",brk=brk)

@app.route('/dinner', methods=["GET","POST"])
def dinner():
    total_calo=0
    brk=food
    if request.method=="POST":
        lst=request.form.getlist('food')
        for i,j in enumerate(lst):
            if j!="0":
                num=lst[i]
                calo=list(food.values())[i]
                total_calo+=int(num)*int(calo)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE calories SET dinner=%s WHERE Username=%s', [total_calo,session['Username']])
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT calories FROM total_calories WHERE Username=%s', [session['Username']])
        abc=list(cursor.fetchone().values())[0]
        if abc==None:
            abc=0
        abc=int(abc)+total_calo
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE total_calories SET calories=%s WHERE Username=%s', [abc,session['Username']])
        mysql.connection.commit()
        return redirect(url_for('nutrition'))
    return render_template("food.html",brk=brk)

@app.route('/nutrition', methods=["GET","POST"])
def nutrition():
    tdate = date.today()
    meals=["breakfast","morning snack","lunch", "evening snack","dinner"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
    cursor.execute('SELECT breakfast,morning_snack,lunch, evening_snack,dinner FROM calories WHERE Username = %s', [session['Username']])  
    cal=cursor.fetchone().values()
    cursor.execute('SELECT total_breakfast,total_morning_snack,total_lunch, total_evening_snack,total_dinner FROM calories WHERE Username = %s', [session['Username']])
    rem_cal=cursor.fetchone().values()
    cursor.execute('SELECT date_ FROM calories WHERE Username = %s', [session['Username']])
    db_date=cursor.fetchone()
    con_cal=0
    cursor.execute('SELECT Total_Calories FROM total_calories WHERE Username = %s', [session['Username']])
    total_cal=cursor.fetchone().values()
    if db_date['date_']==tdate:    
        for i in cal:
            if i == None:
                con_cal+=0
            else:
                con_cal+=int(i)  
    else:
        con_cal=0
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE calories SET date_=%s WHERE Username = %s', [tdate,session['Username']])
        mysql.connection.commit()
    rem=list(total_cal)[0]-con_cal
    links=["http://127.0.0.1:5000/brkfast","http://127.0.0.1:5000/mornsnack","http://127.0.0.1:5000/lunch","http://127.0.0.1:5000/evesnack","http://127.0.0.1:5000/dinner"]
    return render_template("meal.html", rem=rem,con_cal=con_cal,meals=zip(meals,cal,rem_cal,links))

@app.route('/blogs', methods=["GET","POST"])
def blog():
    return render_template("blog.html")

@app.route('/workout/<bodypart>', methods=["GET","POST"])
def bodypart(bodypart):
    title=bodypart
    levels=["Beginner","Intermediate","Advance"]
    links=["/"+bodypart+"/b"+bodypart,"/"+bodypart+"/i"+bodypart,"/"+bodypart+"/a"+bodypart]
    imgs=["/static/img/beginner.jpg","/static/img/inter.jpg","/static/img/adv.png"]
    return render_template("bodypart.html",title=title,links_imgs=zip(links,imgs,levels))


#arm
@app.route('/workout/arm/<exs>', methods=["GET","POST"])
def exercisesarm(exs):
    part=exs[1:]
    nam=plan["arm"][exs]["name"]
    link= plan["arm"][exs]["links"]
    imgs=plan["arm"][exs]["imgs"]
    return render_template("exercises.html",part=part,exercises_abcs=zip(nam,link,imgs),exs=exs)
#beginner arm
@app.route('/workout/arm/barm/<ex>', methods=["GET","POST"])
def exercisebarm(ex):
    status=""
    index=plan["arm"]["barm"]["links"].index(ex)
    nam=plan["arm"]["barm"]["name"][index]
    img=plan["arm"]["barm"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["arm"]["barm"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/arm/barm/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["arm"]["barm"]["links"][index+1]
            level="barm"
            part="arm"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# intermediate arm
@app.route('/workout/arm/iarm/<ex>', methods=["GET","POST"])
def exerciseiarm(ex):
    status=""
    index=plan["arm"]["iarm"]["links"].index(ex)
    nam=plan["arm"]["iarm"]["name"][index]
    img=plan["arm"]["iarm"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:                    
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["arm"]["iarm"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/arm/iarm/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["arm"]["iarm"]["links"][index+1]
            level="iarm"
            part="arm"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# advance arm
@app.route('/workout/arm/aarm/<ex>', methods=["GET","POST"])
def exerciseaarm(ex):
    status=""
    index=plan["arm"]["aarm"]["links"].index(ex)
    nam=plan["arm"]["aarm"]["name"][index]
    img=plan["arm"]["aarm"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["arm"]["aarm"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/arm/aarm/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["arm"]["aarm"]["links"][index+1]
            level="aarm"
            part="arm"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)

#abs
@app.route('/workout/abs/<exs>', methods=["GET","POST"])
def exercisesabs(exs):
    part=exs[1:]
    nam=plan["abs"][exs]["name"]
    link= plan["abs"][exs]["links"] 
    img=plan["abs"][exs]["imgs"]    
    return render_template("exercises.html",part=part,exercises_abcs=zip(nam,link,img),exs=exs)
#beginner abs
@app.route('/workout/arm/babs/<ex>', methods=["GET","POST"])
def exercisebabs(ex):
    status=""
    index=plan["abs"]["babs"]["links"].index(ex)
    nam=plan["abs"]["babs"]["name"][index]
    img=plan["abs"]["babs"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["arm"]["barm"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/abs/babs/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["abs"]["babs"]["links"][index+1]
            level="babs"
            part="abs"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# intermediate abs
@app.route('/workout/abs/iabs/<ex>', methods=["GET","POST"])
def exerciseiabs(ex):
    status=""
    index=plan["abs"]["iabs"]["links"].index(ex)
    nam=plan["abs"]["iabs"]["name"][index]
    img=plan["abs"]["iabs"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:                    
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["arm"]["iarm"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/abs/iabs/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["abs"]["iabs"]["links"][index+1]
            level="iabs"
            part="abs"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# advance abs
@app.route('/workout/abs/aabs/<ex>', methods=["GET","POST"])
def exerciseaabs(ex):
    status=""
    index=plan["abs"]["aabs"]["links"].index(ex)
    nam=plan["abs"]["aabs"]["name"][index]
    img=plan["abs"]["aarm"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["abs"]["aabs"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/abs/aabs/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["abs"]["aabs"]["links"][index+1]
            level="aabs"
            part="abs"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
#back
@app.route('/workout/back/<exs>', methods=["GET","POST"])
def exercisesback(exs):
    part=exs[1:]
    nam=plan["back"][exs]["name"]
    link= plan["back"][exs]["links"] 
    img=plan["back"][exs]["imgs"]    
    return render_template("exercises.html",part=part,exercises_abcs=zip(nam,link,img),exs=exs)
#beginner back
@app.route('/workout/back/bback/<ex>', methods=["GET","POST"])
def exercisebback(ex):
    status=""
    index=plan["back"]["bback"]["links"].index(ex)
    nam=plan["back"]["bback"]["name"][index]
    img=plan["back"]["bback"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["back"]["bback"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/back/bback/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["back"]["bback"]["links"][index+1]
            level="bback"
            part="back"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# intermediate back
@app.route('/workout/back/iback/<ex>', methods=["GET","POST"])
def exerciseiback(ex):
    status=""
    index=plan["back"]["iback"]["links"].index(ex)
    nam=plan["back"]["iback"]["name"][index]
    img=plan["back"]["iback"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:                    
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["back"]["iback"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/back/iback/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["back"]["iback"]["links"][index+1]
            level="iback"
            part="back"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# advance back
@app.route('/workout/back/aback/<ex>', methods=["GET","POST"])
def exerciseaback(ex):
    status=""
    index=plan["back"]["aback"]["links"].index(ex)
    nam=plan["back"]["aback"]["name"][index]
    img=plan["back"]["aback"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["back"]["aback"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/back/aback/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["back"]["aback"]["links"][index+1]
            level="aback"
            part="back"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
#legs
@app.route('/workout/legs/<exs>', methods=["GET","POST"])
def exerciseslegs(exs):
    part=exs[1:]
    nam=plan["legs"][exs]["name"]
    link= plan["legs"][exs]["links"]
    img=plan["legs"][exs]["imgs"]    
    return render_template("exercises.html",part=part,exercises_abcs=zip(nam,link,img),exs=exs)
#beginner legs
@app.route('/workout/legs/blegs/<ex>', methods=["GET","POST"])
def exerciseblegs(ex):
    status=""
    index=plan["legs"]["blegs"]["links"].index(ex)
    nam=plan["legs"]["blegs"]["name"][index]
    img=plan["legs"]["blegs"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["legs"]["blegs"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/legs/blegs/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["legs"]["blegs"]["links"][index+1]
            level="blegs"
            part="legs"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# intermediate legs
@app.route('/workout/legs/ilegs/<ex>', methods=["GET","POST"])
def exerciseilegs(ex):
    status=""
    index=plan["legs"]["ilegs"]["links"].index(ex)
    nam=plan["legs"]["ilegs"]["name"][index]
    img=plan["legs"]["ilegs"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:                    
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["legs"]["ilegs"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/legs/ilegs/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["legs"]["ilegs"]["links"][index+1]
            level="ilegs"
            part="legs"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)
# advance legs
@app.route('/workout/legs/alegs/<ex>', methods=["GET","POST"])
def exercisealegs(ex):
    status=""
    index=plan["legs"]["alegs"]["links"].index(ex)
    nam=plan["legs"]["alegs"]["name"][index]
    img=plan["legs"]["alegs"]["imgs"][index]
    if ex=="ex1":
        status="disabled"
    else:
        status=""
    if request.method=="POST":
        if request.form['submit_button'] == 'prev' and ex!="ex1":
            ppg=plan["legs"]["alegs"]["links"][index-1]
            return redirect("http://127.0.0.1:5000/workout/legs/alegs/"+ppg)
        elif request.form['submit_button'] == 'next' and ex!="ex8":
            npg=plan["legs"]["alegs"]["links"][index+1]
            level="alegs"
            part="legs"
            return render_template("rest.html",next=npg,level=level,part=part)
        elif request.form['submit_button'] == 'next' and ex=="ex8":
            return render_template("completed.html")
    return render_template("exercise.html",img=img,nam=nam,status=status)

@app.route('/rest', methods=["GET","POST"])
def rest():
    return render_template("rest.html")

@app.route('/completed', methods=["GET","POST"])
def completed():
    return render_template("completed.html")

if __name__=="__main__":
    app.run()