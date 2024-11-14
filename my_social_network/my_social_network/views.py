from . import db
import django
from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse, JsonResponse
from django.db import DatabaseError
from enum import Enum
import datetime
import os
import asyncpg

def mainpage(request):
    return render(request, 'mainpage.html')

def login(request):
    try:
        if request.method == 'GET':
            return render(request, 'login.html')
        elif request.method == 'POST':
            return HttpResponse("", status=200)
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
            print(request.body)
            return HttpResponse("", status=200)
        else:
            return HttpResponse(f"Bad request method: {request.method} method is not supported!", status=400)
    except asyncpg.PostgresError as e:
        return HttpResponse(f"Postgres database error: {e}", status=500)
    except Exception as e:
        return HttpResponse(f"Unexpected error: {e}", status=500)

def redirect_to_main(request):
    return redirect('mainpage')
