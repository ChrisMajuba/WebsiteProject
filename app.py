from flask import Flask, request, jsonify
from flask import render_template
from database import get_experts,add_applicant_db,check_member
#Flask is a web micro framework used to design a website using python

#creating the Flask object
app = Flask("__main__")

#website routes
#**************************************************
#***************************************************
#***************************************************
@app.route("/")
def homepage():
  return render_template("/pages/homepage.html")

@app.route("/parks_page")
def parks():
  return render_template("/pages/parks.html")

@app.route("/experts_page")
def experts():
  #request infomation about the active force experts
  data_db = get_experts()
  return render_template("/pages/experts.html",data = data_db)
  
@app.route("/booking/<info>")
def bookings_page(info):
  return render_template("/pages/park_booking.html",_info=info)

@app.route("/diet")
def diet():
  return render_template("/content/diet.html")

@app.route("/exercise/programs")
def show_programs():
  return render_template("/content/programs.html")

@app.route("/membership")
def membership():
  return render_template("/pages/membership.html")

@app.route("/about")
def about():
  return render_template("/pages/about.html")

@app.route("/login_page")
def login():
  return render_template("/pages/login.html")

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
  return render_template("/forms/submitted.html",data=applicant_data,string="session")

@app.route("/membership/apply", methods=["post"])
def membership_applicant():
  info = request.form
  member_applicant = dict(info)
  #send membership applicant to database
  add_applicant_db(member_applicant ,"membership")
  return render_template("/forms/submitted.html",data=member_applicant,string="membership")

@app.route("/logging_in",methods = ["post"])
def try_to_login():
  info = request.form #request info
  member_login = dict(info) #convert info to dictionary
  verified_member = check_member(member_login)
  if verified_member:
    return jsonify(verified_member)
  else:
    return jsonify("Sorry you are not in the system, have you tried registering first?")
  
  
#since the file main.py will be ran as a script, python will assign __name__ to __main__
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
