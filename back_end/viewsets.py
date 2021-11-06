from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import FormParser

class GetOnlyGenericViewset(viewsets.ViewSet):
    http_method_names = ['get']