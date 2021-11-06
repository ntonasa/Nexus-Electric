from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import authentication, permissions

import os
import requests
import json

BASE_API_URL = 'https://localhost:8765/energy/api/'
BASE_LOCAL_URL = 'http://localhost:8888/energy/'


@api_view(['GET'])
def about(request):
    token = request.get_signed_cookie('token', False, salt='_@f5QB:&uZ.2#QZFu/^?')
    context = {'logged_in' : True} if token else {}
    return render(request, 'about.html', context)

@api_view(['GET'])
def logout(request):
    response = HttpResponseRedirect(os.path.join(BASE_LOCAL_URL, 'login'))
    response.delete_cookie('token')
    return response

class LoginView(APIView):
    def get(self, request):
        token = request.get_signed_cookie('token', False, salt='_@f5QB:&uZ.2#QZFu/^?')
        if token:
            return HttpResponseRedirect(os.path.join(BASE_LOCAL_URL, 'nexuselectric'))
        else:
            return render(request, 'login.html')
    
    def post(self, request):
        response = requests.post(
            os.path.join(BASE_API_URL, 'Login'),
            {
                'username' : request.data['username'],
                'password' : request.data['password']
            },verify=False
        )

        data = response.json()
        if 'token' in data:
            response = HttpResponseRedirect(os.path.join(BASE_LOCAL_URL, 'nexuselectric'))
            response.set_signed_cookie('token', data['token'], salt='_@f5QB:&uZ.2#QZFu/^?')
            return response
        else:
            return render(request, 'login.html', context={'error_message' : "Unable to login with specified credentials."})

class NexusElectricView(APIView):
    def get(self, request):
        token = request.get_signed_cookie('token', False, salt='_@f5QB:&uZ.2#QZFu/^?')
        if not token:
            return HttpResponseRedirect(os.path.join(BASE_LOCAL_URL, 'login'))
        else:
            return render(request, 'home.html', {'logged_in' : True})
    
    def post(self, request):
        token = request.get_signed_cookie('token', False, salt='_@f5QB:&uZ.2#QZFu/^?')
        if not token:
            return HttpResponseRedirect(os.path.join(BASE_LOCAL_URL, 'login'))
        else:
            if request.data['dataset'] != 'AggregatedGenerationPerType':
                response = requests.get(
                    os.path.join(BASE_API_URL, request.data['dataset'], request.data['area'], request.data['resolution'], request.data['date_func'], request.data['date']),
                    headers={'X-OBSERVATORY-AUTH': token}, 
                    verify=False
                )
            else:
                prodtype = 'AllTypes' if ('prodtypeall' in request.data) else request.data['prodtype']
                response = requests.get(
                    os.path.join(BASE_API_URL, request.data['dataset'], request.data['area'], prodtype, request.data['resolution'], request.data['date_func'], request.data['date']), 
                    headers={'X-OBSERVATORY-AUTH': token}, 
                    verify=False
                )
            
            if response.status_code == 200:
                data = response.json()
                data_table = {
                    'headers' : [],
                    'rows' : []
                }
                data_table['headers'] = list(data[0].keys())
                
                for obj in data:
                    data_table['rows'].append(list(obj.values()))
                
                return render(request, 'home.html', {'logged_in' : True, 'data_table' : data_table})
            else:
                return render(request, 'home.html', {'logged_in' : True, 'error_message' : True})

