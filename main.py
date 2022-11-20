from flask import render_template, request, redirect, make_response

from init import db, app
from models import *
from functions import Actions


@app.route("/", methods=['POST', 'GET'])
def index():
	try:
		us = Actions().get_user_by_gender(request.cookies.get('username'), Actions().get_gender(request.cookies.get('username')))

		messages = Actions().get_messages(request.cookies.get('username'))
		unchecked_messages = 0

		photo = Actions().get_photo(us.login)

		for message in messages:
			if message.status == 'unchecked':
				unchecked_messages += 1

		return render_template('index.html', username = request.cookies.get('username'), user_name = us.login, information = f'{us.first_name} {us.last_name}, {us.age}', unchecked_messages = unchecked_messages, photo_url = photo.photo_url)
	except AttributeError:
		return render_template('index.html', username = request.cookies.get('username'))
	except IndexError:
		return render_template('index.html', username = request.cookies.get('username'))

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.cookies.get('username'):
		return redirect('/')
	else:
		if request.method == 'POST':
			first_name = str(request.form['first_name'])
			last_name  = str(request.form['last_name'])
			password   = str(request.form['password'])
			login      = str(request.form['login'])
			age        = str(request.form['age'])
			gender     = str(request.form['gender'])

			Actions().create_user(first_name, last_name, login, password, age, gender)

			resp = make_response(redirect('/'))
			resp.set_cookie('username', login)
			return resp

		return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.cookies.get('username'):
		return redirect('/')
	else:
		if request.method == 'POST':
			login = str(request.form['login'])
			password = str(request.form['password'])
			us = Actions().user_login(login, password)

			if us:
				resp = make_response(redirect('/'))
				resp.set_cookie('username', login)
				return resp
			else: 
				return render_template('login.html', error_message = 'Invalid login or password')

		return render_template('login.html')

@app.route('/logout')
def logout():
	if request.cookies.get('username'):
		resp = make_response(redirect('/'))
		resp.delete_cookie('username')
		return resp
	else:
		return redirect('/')

@app.route('/api')
def api():
	user_gender = Actions().get_gender(request.cookies.get('username'))
	us = Actions().get_user_by_gender(request.cookies.get('username'), user_gender)

	photo = Actions().get_photo(us.login)

	return {'string': f'{us.first_name} {us.last_name}, {us.age}', 'username': us.login, 'photo_url': photo.photo_url}

@app.route('/myprofile', methods = ['GET', 'POST'])
def my_profile():
	if request.cookies.get('username'):
		if request.method == 'POST':
			# if user does not select file, browser also
			# submit a empty part without filename
			if len(request.files) == 0:
				return redirect(request.url)

			file = request.files['photo']
			if file:
				file.save(f'{ app.config["UPLOAD_FOLDER"] }/{ request.cookies.get("username")}.png')
				Actions().edit_photo(request.cookies.get('username'), f'{ request.cookies.get("username")}.png')

				return redirect('/myprofile') 

		us       = Actions().get_user(request.cookies.get('username'))
		messages = Actions().get_messages(request.cookies.get('username'))
		photo    = Actions().get_photo(request.cookies.get('username'))

		messages.reverse()

		for message in messages:
			if message.status == 'unchecked':
				message.status = 'checked'
				db.session.commit()

		return render_template('my_profile.html', login = us[0].login, first_name = us[0].first_name, last_name = us[0].last_name, age = us[0].age, messages = messages[:15], photo_url = photo.photo_url)
	else:
		return redirect('/')

@app.route('/profile/<username>')
def profile(username):
	us       = Actions().get_user(username)
	photo    = Actions().get_photo(username)

	return render_template('profile.html', login = us[0].login, first_name = us[0].first_name, last_name = us[0].last_name, age = us[0].age, photo_url = photo.photo_url)

@app.route('/setlike/<username>')
def setlike(username):
	owner_username   = username
	sender_username  = str(request.cookies.get('username'))
	status           = 'unchecked'

	Actions().add_message(owner_username, sender_username, status)

	return 'succes'

if __name__== '__main__':
	app.run(debug = True)