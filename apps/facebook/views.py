# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt


def index(request):
	all_users=User.objects.all()
	context = {
		'all': all_users
	}
	
	return render(request, 'facebook/index.html', context)
def new(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):	
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		
		if request.method=="POST":
			print request.POST
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']
			password = request.POST['password']
			hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

			user=User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
			print user.id
			request.session['id']=user.id
			return redirect("/friends/")
		else:
			return redirect('/')
def login(request):
	loginerrors= User.objects.loginval(request.POST)


	if len(loginerrors):
		for tag, error in loginerrors.iteritems():
			messages.error(request, error, extra_tags=tag)
			
			return redirect('/')
	else:
		if request.method=="POST":
			user= User.objects.get(email = request.POST['email'])
			print request.POST
			email=request.POST['email']
			password=request.POST['password']
			request.session['id']=user.id
			# if bcrypt.checkpw(password.encode(), hashed.encode()) == hashed:
			return redirect("friends/")
		else:
			return redirect('/')
def friends(request):
	user=User.objects.get(id=request.session['id'])
	table=User.objects.exclude(id=request.session['id'])
	overall=user.pokers.count()

	
	data = {
		'session':user,
		'all_users':table,
		'total':overall
		
	}
	return render(request, "facebook/friends.html", data)
def poke(request, id):
	this_user=User.objects.get(id=id)
	user=User.objects.get(id=request.session['id'])
	poking = Poking.objects.create(from_user=this_user, to_person=user)

	return redirect('/friends')
def logout(request):
	request.session.pop('id')
	return redirect('/')

# Create your views here.
