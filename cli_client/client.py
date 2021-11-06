import os
import sys
import requests
import urllib3
from argparse import ArgumentParser, FileType
from colorama import init as colorinit
from termcolor import cprint 
from pyfiglet import figlet_format

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

port = 8765
BASE_URL = f'https://localhost:{port}/energy/api/'
TOKEN_FILE_PATH = "/home/ntonasa/softeng19bAPI.token"
SSL_VERIFY = False

def main():
   welcome()
   main_parser = generate_parser()
   args = main_parser.parse_args()
   params = vars(args)
   if 'func' in params:
      response = args.func(params)
      if response.status_code == 400:
         print("400: BAD REQUEST")
      elif response.status_code == 500:
         print("500: Internal Server Error")
      else:
         if params['format'] == 'json':
            print(response.json())
         else:
            print(response.text)

def get_token():
   if os.path.isfile(TOKEN_FILE_PATH):
      f = open(TOKEN_FILE_PATH, 'r')
      token = f.read()
      f.close()
      return token
   else:
      return None

def health_check(params):
   return requests.get(BASE_URL+"HealthCheck", verify=SSL_VERIFY)

def reset(params):
   return requests.post(BASE_URL+"Reset", verify=SSL_VERIFY)

def login(params):
   payload = {'username': params['username'], 'password': params['passw']}
   response = requests.post(BASE_URL+"Login", data=payload, verify=SSL_VERIFY)
   if response.status_code==200:
      f = open(TOKEN_FILE_PATH, "w")
      token = response.json()['token']
      f.write(token)
      f.close()
   return response

def logout(params):
   token = get_token()
   response = requests.post(BASE_URL+"Logout", headers={'X-OBSERVATORY-AUTH': token}, verify=SSL_VERIFY)
   if token:
      os.remove("/home/ntonasa/softeng19bAPI.token")
   return response

def new_user(params):
   payload = {'username': params['newuser'], 'password': params['passw'], 'email': params['email'], 'quota': params['quota']}
   token = get_token()
   return requests.post(BASE_URL+"Admin/users", headers={'X-OBSERVATORY-AUTH': token}, data=payload, verify=SSL_VERIFY)

def user_status(params):
   token = get_token()
   return requests.get(BASE_URL+"Admin/users/"+params['userstatus'], headers={'X-OBSERVATORY-AUTH': token}, verify=SSL_VERIFY)

def mod_user(params):
   token = get_token()
   payload = {'username': params['moduser'], 'password': params['passw'], 'email': params['email'], 'quota': params['quota']}
   return requests.put(BASE_URL+"Admin/users/"+params['moduser'], headers={'X-OBSERVATORY-AUTH': token}, data=payload, verify=SSL_VERIFY)

def new_data(params):
   token = get_token()
   files = {'file' : params['source']}
   return requests.post(BASE_URL+"Admin/"+params['newdata'], headers={'X-OBSERVATORY-AUTH': token}, files=files, verify=SSL_VERIFY)

def actual_total_load(params):
   token = get_token()
   if params['date']:
      api_call = 'date'
   elif params['month']:
      api_call = 'month'
   elif params['year']:
      api_call = 'year'

   return requests.get(
      BASE_URL+f"ActualTotalLoad/{params['area']}/{params['timeres']}/{api_call}/{params[api_call]}?format={params['format']}", 
      headers={'X-OBSERVATORY-AUTH': token}, 
      verify=SSL_VERIFY
   )

def aggregated_generation_per_type(params):
   token = get_token()
   if params['date']:
      api_call = 'date'
   elif params['month']:
      api_call = 'month'
   elif params['year']:
      api_call = 'year'

   return requests.get(
      BASE_URL+f"AggregatedGenerationPerType/{params['area']}/{params['prodtype']}/{params['timeres']}/{api_call}/{params[api_call]}?format={params['format']}", 
      headers={'X-OBSERVATORY-AUTH': token}, 
      verify=SSL_VERIFY
   )

def day_ahead_total_load_forecast(params):
   token = get_token()
   if params['date']:
      api_call = 'date'
   elif params['month']:
      api_call = 'month'
   elif params['year']:
      api_call = 'year'

   return requests.get(
      BASE_URL+f"DayAheadTotalLoadForecast/{params['area']}/{params['timeres']}/{api_call}/{params[api_call]}?format={params['format']}", 
      headers={'X-OBSERVATORY-AUTH': token}, 
      verify=SSL_VERIFY
   )

def actual_vs_forecast(params):
   token = get_token()
   if params['date']:
      api_call = 'date'
   elif params['month']:
      api_call = 'month'
   elif params['year']:
      api_call = 'year'

   return requests.get(
      BASE_URL+f"ActualvsForecast/{params['area']}/{params['timeres']}/{api_call}/{params[api_call]}?format={params['format']}", 
      headers={'X-OBSERVATORY-AUTH': token}, 
      verify=SSL_VERIFY
   )

def admin(params):
   if params['newuser']:
      return new_user(params)
   elif params['moduser']:
      return mod_user(params)
   elif params['userstatus']:
      return user_status(params)
   elif params['newdata']:
      return new_data(params)


## Helper Functions
def welcome():
   colorinit(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
   cprint(figlet_format('NEXUS ELECTRIC', font='starwars'), 'blue', attrs=['bold'])
   class color:
      BOLD = '\033[1m'
      DARKCYAN = '\033[36m'
      UNDERLINE = '\033[4m'
      END = '\033[0m'

   part = '-----------------------------------------------------------'
   print(color.DARKCYAN + part+'\nWelcome to the Nexus ELectric official command line client!\n'+part+'\n' + color.END)
