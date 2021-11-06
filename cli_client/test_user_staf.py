import pytest
from client import *
import random
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

rand_num = random.randint(0, 100000)

create_params = {'username': 'Alex'+str(rand_num), 'moduser':'Alex'+str(rand_num), 'userstatus':'Alex'+str(rand_num),  'newuser': 'Alex'+str(rand_num),'passw': 'dab', 'email': 'al@dmail.com', 'quota': 20}
login_params = {'username': 'Alex'+str(rand_num), 'passw': 'dab'}
login_params_admin = {'username': 'admin', 'passw': '321nimda'}

@pytest.fixture(scope="session", autouse=True)
def create_user():
    print("\nSetup, creating user")
    login(login_params_admin)
    responce_ = new_user(create_params)
    logout('')
    yield responce_
    print("ending session")

@pytest.fixture()
def login_user():
    print("Setup, login user")
    responce_ = login(login_params)
    yield responce_
    print("logout")
    logout('')

@pytest.fixture()
def login_admin():
    print("Setup, login admin")
    responce_ = login(login_params_admin)
    yield responce_
    print("logout admin")
    logout('')

def test_get_actual_total_load(login_user):
    assert login_user.status_code == 200
    query = {'area':'Greece', 'date':'2020-01-01', 'timeres':'PT30M', 'format':'json', 'month': '', 'year': ''}
    responce = actual_total_load(query)
    assert responce.status_code == 200

def test_get_aggregated_generation_type(login_user):
    assert login_user.status_code == 200
    query = {'area':'Austria', 'date':'2018-01-06', 'timeres':'PT15M', 'prodtype':'Fossil Gas', 'format':'json', 'month': '', 'year': ''}
    responce = aggregated_generation_per_type(query)
    assert responce.status_code == 200
    foo=json.loads(responce.text)
    if len(foo) > 0:
        k_foo=set(list(foo[0].keys()))
        correct = set(['Source', 'Dataset', 'AreaName', 'Year', 'Month', 'Day', 'DateTimeUTC', 'ActualGenerationOutputValue', 'UpdateTimeUTC'])
        assert k_foo == correct
    pass

def test_get_day_ahead_total_load_forcast(login_user):
    assert login_user.status_code == 200
    query = {'area':'Greece', 'month':'2020-01', 'timeres':'PT60M', 'format':'json', 'date': '', 'year': ''}
    responce = day_ahead_total_load_forecast(query)
    assert responce.status_code == 200

def test_get_actual_vs_forcast(login_user):
    assert login_user.status_code == 200
    query = {'area':'Greece', 'timeres':'PT60M', 'year': '2018', 'format':'json', 'date': '', 'month': ''}
    responce = actual_vs_forecast(query)
    assert responce.status_code == 200

