from flask import Flask, render_template, request, redirect
import csv
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path #os.path

app = Flask(__name__)
#print (__name__)

@app.route('/')
@app.route('/index.html')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == 'POST':
		try:
			data = request.form.to_dict()
			email = EmailMessage() #objeto email
			email['from'] = data["email"]
			email ['to'] = 'carlos.e.carvalho@gmail.com'
			email['subject'] = data["subject"]
			email.set_content(data["message"]+data[email])
			send_email(email)
			return redirect('./thankyou.html')
		except:
			return 'Did not send email'
	else:
		return 'Something went wrong.'

def  write_to_file(data):
	with open('database.txt', mode='a') as database:
		email = data["email"]
		subject = data['subject']
		message = data["message"]
		file = database.write(f'\n{email}, \n{subject}, \n{message}\n\n')

def  write_to_csv(data):
	with open('database.csv', newline='', mode='a') as database2:
		email = data["email"]
		subject = data['subject']
		message = data["message"]
		csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([email,subject,message])



def send_email(email):
	print("WE GOT HERE!!!")
	with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
		smtp.ehlo() #mensagem de olá
		smtp.starttls() #tls é uma forma de criptografia
		smtp.login('portfoliocarloscarvalho@gmail.com', 'AnaC0501')
		smtp.send_message(email)
		print('all good boss!')
