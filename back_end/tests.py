from django.test import TestCase
from rest_framework.test import APITestCase, RequestsClient, APIRequestFactory
from collections import OrderedDict
import json
from back_end.models import *
from back_end.serializers import*
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import requests
import datetime
from django.utils import timezone
BASE_URL = 'https://localhost:8765/energy/api/'


class TestSuppEndpoints(APITestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        # self.factory = APIRequestFactory()
        timestamp = timezone.now()

        self.map_code_id = MapCode.objects.create(
            EntityCreatedAt=timestamp, EntityModifiedAt=timestamp)
        self.allocated_eic_detail = AllocatedEICDetail.objects.create(EntityCreatedAt=timestamp, EntityModifiedAt=timestamp,
                                                                      IsDeleted=0, AllocatedEICID=3)

        self.area_code_id = AggregatedGenerationPerType.objects.create(AreaCodeId=self.allocated_eic_detail,
                                                                       EntityCreatedAt=timestamp, EntityModifiedAt=timestamp, ActionTaskID='324285',
                                                                       Year=2020, Month=1, Day=12,  DateTime=timestamp,
                                                                       UpdateTime=timestamp, ActualGenerationOutput=40.00, ActualConsuption=32.00)

        self.user = User.objects.create_superuser(
            username='admin', password='321nimda', email='admin@gmail.com', is_staff=True)
        self.user.save()
        self.user = User.objects.create_user(
            username='tester', password='code')
        self.user.save()

    def test_healthcheck(self):
        response = self.client.get(
            BASE_URL+'HealthCheck', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "OK"})

    def test_reset(self):
        response = self.client.post(
            BASE_URL+'Reset', format='json')
        self.assertTrue(MapCode.objects.all().count() > 0)
        self.assertTrue(AggregatedGenerationPerType.objects.all().count() == 0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "OK"})
        self.assertTrue(User.objects.all().count() == 1)


class ActualTotalLoadTest(APITestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.timestamp = datetime.datetime.strptime(
            '2020-03-01 21:11:37.549641 +02:00', '%Y-%m-%d  %H:%M:%S.%f %z')
        # print(ActualTotalLoad.objects.all().count())

        self.map_code_id = MapCode.objects.create(
            EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp)
        self.allocated_eic_detail = AllocatedEICDetail.objects.create(EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp,
                                                                      IsDeleted=0, AllocatedEICID=3)

        self.resolution_code1 = ResolutionCode.objects.create(
            EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp, ResolutionCodeText='PT60M', ResolutionCodeNote='patata')
        self.resolution_code2 = ResolutionCode.objects.create(
            EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp, ResolutionCodeText='PT10M', ResolutionCodeNote='mpamia')
        self.resolution_code3 = ResolutionCode.objects.create(
            EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp, ResolutionCodeText='PT30M', ResolutionCodeNote='argeis')

        self.area_code_id1 = ActualTotalLoad.objects.create(AreaCodeId=self.allocated_eic_detail, MapCodeId=self.map_code_id, ResolutionCodeId=self.resolution_code1,
                                                            EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp, ActionTaskID='123',
                                                            Year=2020, Month=1, Day=12,  DateTime=self.timestamp,
                                                            UpdateTime=self.timestamp, TotalLoadValue=2.00, AreaName='Greece')

        self.area_code_id2 = ActualTotalLoad.objects.create(AreaCodeId=self.allocated_eic_detail, ResolutionCodeId=self.resolution_code2,
                                                            EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp, ActionTaskID='1234',
                                                            Year=2020, Month=2, Day=1,  DateTime=self.timestamp,
                                                            UpdateTime=self.timestamp, TotalLoadValue=2.00, AreaName='Greece')

        self.area_code_id3 = ActualTotalLoad.objects.create(AreaCodeId=self.allocated_eic_detail, ResolutionCodeId=self.resolution_code3,
                                                            EntityCreatedAt=self.timestamp, EntityModifiedAt=self.timestamp, ActionTaskID='12345',
                                                            Year=2018, Month=3, Day=5,  DateTime=self.timestamp,
                                                            UpdateTime=self.timestamp, TotalLoadValue=2.00, AreaName='Austria')

        quota = 10000
        self.user = User.objects.create_user(
            'tester', 'abarser@blablas.com', 'code')
        self.user.save()
        self.nexususer = NexusUser(user=self.user, quota=quota)
        self.nexususer.save()
    # Include an appropriate `Authorization:` header on all requests.

    def test_ActualTotalLoad1a(self):

        # Include an appropriate `Authorization:` header on all requests.
        #client = APIClient()
        # login user
        response = self.client.post(
            BASE_URL+'Login', {'username': 'tester', 'password': 'code'}, format='json')

        #client.login(username='tester', password='code')

        c = Token.objects.all().count()
        #token = Token.objects.get(user_id = self.user.id)
        token = response.data['token']
        #client.credentials(header ={'HTTP_X_OBSERVATORY_AUTH':token})
        response = self.client.get(
            BASE_URL+'ActualTotalLoad/Greece/PT60M/date/2020-01-12', format='json', HTTP_X_OBSERVATORY_AUTH=token)
        self.assertEqual(response.status_code, 200)
        #print("----------------------------")
        tmp_dict = dict(response.data[0])
        correct = {'ActualTotalLoadValue': 2.0, 'AreaName': 'Greece', 'Dataset': 'ActualTotalLoad', 'DateTimeUTC': str(
            self.timestamp)[:26], 'Day': 12, 'Month': 1, 'Source': 'entso-e', 'UpdateTimeUTC': str(self.timestamp)[:26], 'Year': 2020}
        #s = json.loads(response.text)
        self.assertEqual(tmp_dict, correct)

        #self.assertEqual(json.dumps(response.data), '[{"Source": "entso-e", "Dataset": "ActualTotalLoad", "AreaName": "Greece", "AreaTypeCode": "", "MapCode": "", "ResolutionCode": "PT60M", "Year": 2020, "Month": 1, "Day": 12, "DateTimeUTC": self.timestamp, "ActualTotalLoadByValue": 2.00, "UpdateTimeUTC": self.timestamp}]')
    def test_ActualTotalLoad1b(self):

        # Include an appropriate `Authorization:` header on all requests.
        #client = APIClient()
        # login user
        response = self.client.post(
            BASE_URL+'Login', {'username': 'tester', 'password': 'code'}, format='json')

        #client.login(username='tester', password='code')

        c = Token.objects.all().count()
        #token = Token.objects.get(user_id = self.user.id)
        token = response.data['token']
        #client.credentials(header ={'HTTP_X_OBSERVATORY_AUTH':token})
        response = self.client.get(
            BASE_URL+'ActualTotalLoad/Greece/PT60M/month/2020-01', format='json', HTTP_X_OBSERVATORY_AUTH=token)
        self.assertEqual(response.status_code, 200)
        #print("----------------------------")
        tmp_dict = dict(response.data[0])
        #correct = {'ActualTotalLoadValue': 2.0, 'AreaName': 'Greece', 'Dataset': 'ActualTotalLoad', 'DateTimeUTC': str(
        #    self.timestamp)[:26], 'Day': 12, 'Month': 1, 'Source': 'entso-e', 'UpdateTimeUTC': str(self.timestamp)[:26], 'Year': 2020}
        correct = {"Source": "entso-e", "Dataset": "ActualTotalLoad", "AreaName": "Greece", "AreaTypeCode": None,
                   "MapCode": None, "ResolutionCode": "PT60M", "Year": 2020, "Month": 1, "Day": 12, "ActualTotalLoadByDayValue": 2.0}
        #s = json.loads(response.text)
        self.assertEqual(tmp_dict, correct)

        #self.assertEqual(json.dumps(response.data), '[{"Source": "entso-e", "Dataset": "ActualTotalLoad", "AreaName": "Greece", "AreaTypeCode": "", "MapCode": "", "ResolutionCode": "PT60M", "Year": 2020, "Month": 1, "Day": 12, "DateTimeUTC": self.timestamp, "ActualTotalLoadByValue": 2.00, "UpdateTimeUTC": self.timestamp}]')
    def test_ActualTotalLoad1c(self):

        # Include an appropriate `Authorization:` header on all requests.
        #client = APIClient()
        # login user
        response = self.client.post(
            BASE_URL+'Login', {'username': 'tester', 'password': 'code'}, format='json')

        #client.login(username='tester', password='code')

        c = Token.objects.all().count()
        #token = Token.objects.get(user_id = self.user.id)
        token = response.data['token']
        #client.credentials(header ={'HTTP_X_OBSERVATORY_AUTH':token})
        response = self.client.get(
            BASE_URL+'ActualTotalLoad/Greece/PT60M/year/2020', format='json', HTTP_X_OBSERVATORY_AUTH=token)
        self.assertEqual(response.status_code, 200)
        #print("----------------------------")
        tmp_dict = dict(response.data[0])
        #correct = {'ActualTotalLoadValue': 2.0, 'AreaName': 'Greece', 'Dataset': 'ActualTotalLoad', 'DateTimeUTC': str(
        #    self.timestamp)[:26], 'Day': 12, 'Month': 1, 'Source': 'entso-e', 'UpdateTimeUTC': str(self.timestamp)[:26], 'Year': 2020}
        #correct = {"Source": "entso-e", "Dataset": "ActualTotalLoad", "AreaName": "Greece", "AreaTypeCode": None,
        #           "MapCode": None, "ResolutionCode": "PT60M", "Year": 2020, "Month": 1, "Day": 12, "ActualTotalLoadByDayValue": 2.0}
                   
        correct={"Source":"entso-e","Dataset":"ActualTotalLoad","AreaName":"Greece","AreaTypeCode":None,"MapCode":None,"ResolutionCode":"PT60M","Year":2020,"Month":1,"ActualTotalLoadByMonthValue":2.0}
        #s = json.loads(response.text)
        self.assertEqual(tmp_dict, correct)


    def test_not_authorized(self):
        response = self.client.get(
                BASE_URL+'ActualTotalLoad/Greece/PT60M/year/2020', format='json')
        self.assertEqual(response.status_code, 403)



class AdminEdpoints(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'admin', 'abarser@blablas.com', '321nimda', is_staff=True)
        self.admin_user.save()

        quota = 10000
        self.user = User.objects.create_user(
            'tester', 'abarser@blablas.com', 'code')
        self.user.save()
        self.nexususer = NexusUser(user=self.user, quota=quota)
        self.nexususer.save()

    def test_insert_user(self):

        payload = {'username': 'admin', 'password': '321nimda'}
        response = self.client.post(BASE_URL+"Login", data=payload)
        self.assertEqual(response.status_code, 200)
        prev = User.objects.all().count()
        token = response.data['token']
        payload = {'username': 'ThRectifier', 'password': '987', 'email': 'rectifier@nexus.gr', 'quota': 1234}
        response = self.client.post(BASE_URL+"Admin/users", HTTP_X_OBSERVATORY_AUTH=token, data=payload)
        last=User.objects.all().count()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(last>prev)

    def test_forbiden_insert_user(self):

        payload = {'username': 'tester', 'password': 'code'}
        response = self.client.post(BASE_URL+"Login", data=payload)
        self.assertEqual(response.status_code, 200)
        prev = User.objects.all().count()
        token = response.data['token']
        payload = {'username': 'ThRectifier', 'password': '987', 'email': 'rectifier@nexus.gr', 'quota': 1234}
        response = self.client.post(BASE_URL+"Admin/users", HTTP_X_OBSERVATORY_AUTH=token, data=payload)
        last=User.objects.all().count()
        self.assertEqual(response.status_code, 403)
        self.assertTrue(prev==last)

    def test_get_user(self):
        #login user
        payload = {'username': 'tester', 'password': 'code'}
        tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        response = self.client.post(BASE_URL+"Login", data=payload)
        self.assertEqual(response.status_code, 200)
        
        #login admin
        payload = {'username': 'admin', 'password': '321nimda'}
        response = self.client.post(BASE_URL+"Login", data=payload)
        self.assertEqual(response.status_code, 200)
        
        token = response.data['token']
        username='tester'
        #payload = {'username': 'ThRectifier', 'password': '987', 'email': 'rectifier@nexus.gr', 'quota': 1234}
        response = self.client.get(BASE_URL+"Admin/users/"+username, HTTP_X_OBSERVATORY_AUTH=token)
        correct={"username":"tester","API_key":"8e19ae3ef160ab1a70b6d1b3b1c6e91ae8e1d72c","email":"abarser@blablas.com","quota":10000}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict(response.data[0]).keys(),correct.keys())

    def test_update_user(self):
        #login user
        payload = {'username': 'tester', 'password': 'code'}
        tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        response = self.client.post(BASE_URL+"Login", data=payload)
        self.assertEqual(response.status_code, 200)
        
        #login admin
        payload = {'username': 'admin', 'password': '321nimda'}
        response = self.client.post(BASE_URL+"Login", data=payload)
        self.assertEqual(response.status_code, 200)
        
        token = response.data['token']
        username='tester'
        payload = {'username': 'tester1', 'password': '9hhgjg87', 'email': 'rectifier@nexus.gr', 'quota': 1234}
        response = self.client.put(BASE_URL+"Admin/users/"+username, HTTP_X_OBSERVATORY_AUTH=token, data=payload)
        print(self.user.username)
        correct={"username":"tester","API_key":"","email":"abarser@blablas.com","quota":10000}
        self.assertEqual(response.status_code, 200)
        rec = dict(response.data).keys()
        #del rec['API_key']
        self.assertEqual(rec,correct.keys())