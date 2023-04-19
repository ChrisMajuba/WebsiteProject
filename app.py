from flask import Flask, request
from flask import render_template
from database import get_trainers,add_applicant_db
#Flask is a web micro framework used to design a website using python

#creating the Flask object
app = Flask("__main__")

#website routes
#**************************************************
#***************************************************
#***************************************************
@app.route("/")
def homepage():
  data_db = get_trainers()
  return render_template("homepage.html",data = data_db)

@app.route("/booking/<info>")
def bookings_page(info):
  return render_template("booking.html",_info=info)

@app.route("/diet")
def diet():
  return render_template("diet.html")

@app.route("/exercise/programs")
def show_programs():
  return render_template("programs.html")

@app.route("/membership")
def membership():
  return render_template("membership.html")

@app.route("/about")
def about():
  return render_template("about.html")
#***************************************************
#***************************************************
#***************************************************


#routes that contain infomation
@app.route("/bookings/apply",methods=["post"])
def applicant_info():
  info = request.form
  applicant_data = dict(info)
  #send applicant to database
  add_applicant_db(applicant_data ,"session")
  return render_template("submitted.html",data=applicant_data,string="session")

@app.route("/membership/apply", methods=["post"])
def membership_applicant():
  info = request.form
  member_applicant = dict(info)
  #send membership applicant to database
  add_applicant_db(member_applicant ,"membership")
  return render_template("submitted.html",data=member_applicant,string="membership")

#since the file main.py will be ran as a script, python will assign __name__ to __main__
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
