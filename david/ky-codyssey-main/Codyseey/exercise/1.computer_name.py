import socket
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
	if app.debug:
		computer_name = 'Compoter name :' + socket.gethostname()
	else:
		computer_name = ''
	return render_template('index.html',computername = computer_name)

if __name__ == ('__main__'):
	app.run(host='0.0.0.0',port=80,debug='True')
