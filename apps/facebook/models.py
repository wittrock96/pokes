# -*- coding: utf-8 -*-
from __future__ import unicode_literals




from django.db import models
import re
import bcrypt
email_val = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_val = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors={}
		if len(postData['first_name']) < 2:
			errors['first_name'] = "first name must have more than two characters"
		if len(postData['last_name']) < 2:
			errors['last_name'] = "last name must have more the two characters"
		if len(postData['email']) < 1 :
			errors['email'] = 'email cannot be empty'
		elif not email_val.match(postData['email']):
			errors['email'] = 'email is not valid'
		if len(postData['password']) < 8:
			errors['password'] = 'password must be at least 8 characts'
		if postData['confirm_password'] != postData['password']:
			errors['confirm_password'] = 'passwords must match'
	
		return errors
	def loginval(self, postData):
		loginerrors={}
		if len(postData['email']) < 1:
			loginerrors['email'] = 'email cannnot be empty'
			return loginerrors
		dbcheck=User.objects.filter(email=postData['email'])
		pwcheck=User.objects.filter(password=postData['password'])
		

		if not bcrypt.checkpw(postData['password'].encode(), dbcheck[0].password.encode()):
			loginerrors['failed'] = 'pass word is incorrect'
		return loginerrors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now=True)
	pokes= models.ManyToManyField('self', through='Poking', symmetrical=False, related_name='pokers')
	objects=UserManager()
class Poking(models.Model):
	from_user=models.ForeignKey(User, related_name='from_users')
	to_person=models.ForeignKey(User, related_name='to_people')
	
# Create your models here.
