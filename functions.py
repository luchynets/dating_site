from models import *
from init import db 

import random


class Actions:
	def add_message(self, owner_username, sender_username, status):
		message = Message(
			owner_username   = owner_username,
			sender_username  = sender_username,
			status           = status,
		)
		db.session.add(message)
		db.session.commit()

	def get_user(self, username):
		return User.query.filter_by(login = username).all()

	def get_gender(self, username):
		return User.query.filter_by(login = username)[0].gender

	def get_user_by_gender(self, username, user_gender):
		if user_gender == 'male':
			us = random.choice(User.query.filter_by(gender = 'female').all())
		else:
			us = random.choice(User.query.filter_by(gender = 'male').all())

		while us.login == username:
			if user_gender == 'male':
				us = random.choice(User.query.filter_by(gender = 'female').all())
			else:
				us = random.choice(User.query.filter_by(gender = 'male').all())
		return us

	def get_photo(self, username):
		return Profile_Photo.query.filter_by(owner_username = username).first()

	def get_messages(self, owner):
		return Message.query.filter_by(owner_username = owner).all()

	def edit_photo(self, owner, url):
		photo           = Profile_Photo.query.filter_by(owner_username = owner).first()
		photo.photo_url = url
		db.session.commit()

	def user_login(self, username, password):
		return User.query.filter_by(login = username, password = password).all()

	def create_user(self, first_name, last_name, login, password, age, gender):
		user = User(
			first_name = first_name,
			last_name  = last_name,
			password   = password,
			login      = login,
			age        = age,
			gender     = gender
		)

		profile_photo = Profile_Photo(
			photo_url       = 'base_photo/base.png',
			owner_username  = login,
		)

		db.session.add(user)
		db.session.add(profile_photo)
		db.session.commit()