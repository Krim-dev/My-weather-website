from flask import Flask , render_template , request
import requests
import json
import smtplib

app = Flask(__name__)


@app.route("/" , methods=['POST', 'GET'])
def home():
	return render_template("Home.html")

@app.route("/report", methods=['POST', 'GET'])
def report(): 
	if request.method == "POST": 
		first_name = request.form.get("first_name")
		last_name = request.form.get("last_name")
		report  = request.form.get("report")
		
		if not first_name or not last_name or not report : 
			message = "ALL fields are required"
			return render_template('Report.html', message = message)
		else : 
			subject = "Report for your weather web"
			msg = f"{first_name} {last_name} says : {report}"
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.ehlo()
			server.starttls()
			server.login("devtest2005@gmail.com", "dev_akram@2005")
			message = 'Subject: {}\n\n{}'.format(subject, msg)
			server.sendmail("devtest2005@gmail.com", "krimdev1977@gmail.com", message)
			server.quit()
			message = "Your report has been taken in concideration "
			return render_template("Home.html", message=message)
	else : 
		return render_template("Report.html")

@app.route('/temp' , methods=["GET","POST"])
def temp():
	if request.method == "POST": 
		try : 
			city_name = request.form['city']
			api_request = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=18069b15bde1dadab5b6309c4908075c&units=metric")
			api = json.loads(api_request.content)
			temperature = api["main"]["temp"]
			temperature = int(temperature)
			country = api["sys"]["country"]
			feels_like = api["main"]["feels_like"]
			feels_like = int(feels_like)
			mini_temp = api["main"]["temp_min"]
			max_temp = api["main"]['temp_max']
			return render_template("weather.html" , temperature = temperature , city_name=city_name , 
				country=country , feels_like=feels_like , mini_temp=mini_temp, max_temp = max_temp)
		except : 
			return render_template("fail.html")
	else : 
		return render_template("weather.html")

@app.route("/pos", methods=['POST', 'GET'])
def Position(): 
	if request.method == "POST": 
		try :
			city_name = request.form['city']
			api_request = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=18069b15bde1dadab5b6309c4908075c&units=metric")
			api = json.loads(api_request.content)
			longitude = api["coord"]["lon"]
			latitude = api["coord"]["lat"]
			country = api["sys"]["country"]

			return render_template('Position.html' , longitude=longitude , city_name=city_name , 
				country=country , latitude=latitude)
		except : 
			return render_template("fail.html")
	else : 
		return render_template("Position.html")

@app.route("/air", methods= ['GET', 'POST'])
def air(): 
	if request.method == "POST": 
		try :
			city_name = request.form['city']
			api_request = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=18069b15bde1dadab5b6309c4908075c&units=metric")
			api = json.loads(api_request.content)
			country = country = api["sys"]["country"]
			pressure = api["main"]["pressure"]
			humidity = api["main"]["humidity"]
			wind_speed = api["wind"]["speed"]

			return render_template("Air.html",country=country, pressure=pressure ,
			 humidity=humidity , wind_speed = wind_speed , city_name=city_name)
		except : 
			return render_template("fail.html")
	else : 
		return render_template("Air.html")

