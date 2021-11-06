###/home/ntonasa/miniconda3/envs/TL/bin/python
import pytest
from client import *
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
rand_num = random.randint(0, 100000)

login_params = {'username': 'Ntonats'+str(rand_num), 'passw': 'energeiakos'}
test_user =  {'username': 'Ntonats'+str(rand_num), 'moduser':'Ntonats'+str(rand_num), 'userstatus':'Ntonats'+str(rand_num),  'newuser': 'Ntonats'+str(rand_num),'passw': 'energeiakos', 'email': 'hl@dmail.com', 'quota': 20}
create_params2 = {'username': 'Xristos'+str(rand_num),'newuser': 'Xristos'+str(rand_num), 'passw': '123', 'email': 'xr@dmail.com', 'quota': 20}
create_params1 = {'username': 'Den_xerw'+str(rand_num),'newuser': 'Den_xerw'+str(rand_num), 'passw': '234', 'email': 'ca@dmail.com', 'quota': 20}
login_params_admin = {'username': 'admin', 'passw': '321nimda'}


#Create test
login(login_params_admin)
new_user(test_user)
logout('')


def create_user(param):
    print("creating user")
    responce_ = new_user(param)
    return responce_

@pytest.fixture()
def login_user():
    print("login user")
    responce_ = login(login_params)
    yield responce_
    print("logout user")
    logout('')

@pytest.fixture()
def login_admin():
    print("login admin")
    responce_ = login(login_params_admin)
    yield responce_
    print("logout admin")
    logout('')

def test_health_check():
    print("health check...")
    responce = health_check({})
    assert responce.status_code == 200
    assert responce.text == '{"status":"OK"}'

def test_create_user_authorised(login_admin):
    print("user authorisation authorised...")
    responce = create_user(create_params1)
    assert login_admin.status_code == 200
    assert responce.status_code == 200

def test_create_user_unothorised(login_user):
    print("user authorisation unothorised...")
    responce = create_user(create_params2)
    assert login_user.status_code == 200
    assert responce.status_code == 403

def test_user_status_authorised(login_admin):
    print("user status authorised...")
    responce = user_status(test_user)
    assert login_admin.status_code == 200
    assert responce.status_code == 200
    # assert returns

def test_user_status_unothorised(login_user):
    print("user status unothorised...")
    responce = user_status(test_user)
    assert login_user.status_code == 200
    assert responce.status_code == 403

def test_mod_user_authorised(login_admin):
    print("user mod authorised...")
    test_user['email'] = 'el999@central.ntua.gr'
    responce = mod_user(test_user)
    assert login_admin.status_code == 200
    assert responce.status_code == 200
    # assert returns

def test_mod_user_unothorised(login_user):
    print("user mod unothorised...")
    test_user['email'] = 'el999@central.ntua.gr'
    responce = mod_user(test_user)
    assert login_user.status_code == 200
    assert responce.status_code == 403
    