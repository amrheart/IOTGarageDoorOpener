from flask import Flask
from flask import render_template
from flask import *
from aiocoap import *
from datetime import date
import asyncio

run = asyncio.get_event_loop().run_until_complete
protocol = run(Context.create_client_context())

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def index(name=None):
	# when form is submitted, re fetch the data from the raspberry pi
	#if form.validate_on_submit():
	get_msg = Message(code=GET, uri="coap://10.0.0.75/garage")
	get_response = run(protocol.request(get_msg).response)
	cur_state = str(get_response.payload)
	cur_state = cur_state.strip("b")
	cur_state = cur_state.strip("'")
	opposite_state = "empty"
	if cur_state == "OPENED":
		opposite_state = "CLOSED"
	elif cur_state == "CLOSED":
		opposite_state = "OPENED"

	put_msg = 0
	if request.method == "POST":
		if request.form['state_change'] == 'Open Door':
			put_msg = Message(code=PUT, uri="coap://10.0.0.75/garage", payload=bytes("OPEN", 'utf-8'))
			put_response = run(protocol.request(put_msg).response)
		elif request.form['state_change'] == 'Close Door':
			put_msg = Message(code=PUT, uri="coap://10.0.0.75/garage", payload=bytes("CLOSE", 'utf-8'))
			put_response = run(protocol.request(put_msg).response)
		else:
			pass

	# will get the state every time page is refreshed
	get_msg = Message(code=GET, uri="coap://10.0.0.75/garage")
	get_response = run(protocol.request(get_msg).response)
	response_display = str(get_response.payload)
	response_display = response_display.strip("b")
	response_display = response_display.strip("'")
	state=str(response_display)

	# will get time of last action every time page is refreshed
	get_msg = Message(code=GET, uri="coap://10.0.0.75/timeSince")
	get_response = run(protocol.request(get_msg).response)
	response_display = str(get_response.payload)
	response_display = response_display.strip("b")
	response_display = response_display.strip("'")
	time_of = str(response_display)

	get_msg = Message(code=GET, uri="coap://10.0.0.75/uses")
	get_response = run(protocol.request(get_msg).response)
	response_display = str(get_response.payload)
	response_display = response_display.strip("b")
	response_display = response_display.strip("'")
	uses = str(response_display)

	today_date = date.today()
	today_date = today_date.strftime("%d/%m/%Y")
	print(today_date)

	return render_template("garage_door_app.html",state=state, time_of=time_of, uses=uses, today_date=today_date)