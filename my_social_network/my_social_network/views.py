from . import db
import django
from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse, JsonResponse
from django.db import DatabaseError
from enum import Enum
from datetime import datetime
import os
import asyncpg
import bcrypt

def mainpage(request):
    return render(request, 'mainpage.html')

def login(request):
    try:
        if request.method == 'GET':
            return render(request, 'login.html')
        elif request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username)
            print(password)
            sql_request = db.execute_query_sync('SELECT password_hash FROM userprofile WHERE username = $1', *[username])
            if len(sql_request) == 0:
                return HttpResponse('User with this username was not found', status=400)

            print(sql_request)
        else:
            return HttpResponse(f"Bad request method: {request.method} method is not supported!", status=400)
    except asyncpg.PostgresError as e:
        return HttpResponse(f"Postgres database error: {e}", status=500)
    except Exception as e:
        return HttpResponse(f"Unexpected error: {e}", status=500)

def registration(request):
    try:
        if request.method == 'GET':
            return render(request, 'registration.html')
        elif request.method == 'POST':
            username = request.POST.get('username')
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            password = request.POST.get('password')
            birth_date = request.POST.get('birth_date')
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashed_password = hashed_password.decode('utf-8')
            parameters = [username, hashed_password, name, surname, birth_date]
            # Check for uniqueness of username
            sql_result = db.execute_query_sync("SELECT * FROM UserProfile WHERE username = $1", *[username])
            if len(sql_result) > 0:
                return HttpResponse(f"User with username {username} does already exists", status=400)
            #
            db.execute_query_sync("INSERT INTO UserProfile (username, password_hash, name, surname, birth_date) VALUES ($1, $2, $3, $4, $5)",
            *parameters
            )
            return HttpResponse("", status=200)
        else:
            return HttpResponse(f"Bad request method: {request.method} method is not supported!", status=400)
    except asyncpg.PostgresError as e:
        print(f"Postgres database error: {e}")
        return HttpResponse(f"Internal server error has occured.", status=500)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return HttpResponse(f"Internal server error has occured.", status=500)

def redirect_to_main(request):
    return redirect('mainpage')
