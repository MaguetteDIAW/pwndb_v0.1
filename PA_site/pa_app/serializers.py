# api_pwndb/serializers.py
from rest_framework import serializers
from .models import Mails, DbMails, MailsDbMails

class MailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mails
        fields = '__all__'

class DbMailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbMails
        fields = '__all__'

class MailsDbMailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailsDbMails
        fields = '__all__'
