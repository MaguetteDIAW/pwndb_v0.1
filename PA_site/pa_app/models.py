from django.db import models

# Create your models here for the database 
#model class Utilisateur 
class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)  
    mot_de_passe = models.CharField(max_length=50)


class Mails(models.Model):
    email = models.EmailField(unique=True)
    password = models.TextField()
    source = models.CharField(max_length=255, default='Inconnue')


    class Meta:
        db_table = 'api_pwndb_mails'

class DbMails(models.Model):
    name = models.TextField()


    class Meta:
        db_table = 'api_pwndb_db_mails'

class MailsDbMails(models.Model):
    id_mails = models.IntegerField(unique=True)
    id_db_mails = models.IntegerField(unique=True)
    

    class Meta:
        db_table = 'api_pwndb_mails_db_mails'