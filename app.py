from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
#initialize the database
db=SQLAlchemy(app)
# Create a model




class Friends(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    # Create a functon to return a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id
@app.route("/")
def index():
    title="Khaled's Portfolio"
    return render_template("index.html",title=title)
    
@app.route("/friends",methods=['POST','GET'])
def friends():
    title="My Friends"
    if request.method == "POST":
        friend_name =request.form['name']
        new_friend=Friends(name=friend_name)
        # push to data base

        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There were an Error in Connecting the database"
           
    else:
        friends=Friends.query.order_by(Friends.date_created)
        return render_template("friends.html",title=title,friends=friends)

#  Updating the data base
@app.route("/update/<int:id>",methods=['POST','GET'])
def update(id):
    title='Update Friend'
    friend_to_update=Friends.query.get(id)
    if request.method=="POST":
        friend_to_update.name=request.form['name']
                
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was a problem updating the DataBase"
    
    else:
        return render_template('update.html',friend_to_update=friend_to_update,title=title)


# Delete an entry
@app.route("/delete/<int:id>")
def delete(id):
    title='Delete Friend'
    friend_to_delete=Friends.query.get_or_404(id)
    
    try:
            db.session.delete(friend_to_delete)
            db.session.commit()
            return redirect('/friends')
    except:
            return "There was a problem updating the DataBase"
    
    
@app.route("/about")
def about():
    names=["Machine Learning","AI","Data visualisation","Data Analytics"]
    title="About Me"
    lan=["Java","Python","R","Tableabu","PowerBI"]
    return render_template("about.html",title=title,names=names,names2=lan)

@app.route("/subscribe")
def subscribe():
    title="Subscribe to my Newsletter"
    return render_template("subscribe.html",title=title)

@app.route("/form_submit",methods=['POST'])
def form_submit():
    title="Form Submit"
    first_name=request.form.get("first_name")
    last_name=request.form.get("last_name")
    email=request.form.get("email")
    message="You have been subscribed to my email newsletter"
    # server=smtplib.SMTP("smtp.gmail.com",587)
    # server.starttls()
    # server.login("mki9910070@gmail.com","Kh@led9910070")
    # server.sendmail("mki9910070@gmail.com",email,message)
    # server.close()

    if not first_name or not last_name or not email:
        error_statement="All Form fields Required!"
        return render_template("subscribe.html",error_statement=error_statement)

    return render_template("form_submit.html",title=title,first_name=first_name,last_name=last_name,email=email)