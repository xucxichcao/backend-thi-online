from django.shortcuts import render
from rest_framework import viewsets
from .models import accountBulkCreate
from .serializers import AccountBulkCreateSerializer

# Create your views here.


class AccountBulkCreateViewSet(viewsets.ModelViewSet):
    queryset = accountBulkCreate.objects.all()
    serializer_class = AccountBulkCreateSerializer
