from django.contrib import admin
from django.urls import path
from pa_app import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pa_app.views import MailsViewSet, DbMailsViewSet, MailsDbMailsViewSet, check_email

router = DefaultRouter()
router.register(r'mails', MailsViewSet)
router.register(r'dbmails', DbMailsViewSet)
router.register(r'mailsdbmails', MailsDbMailsViewSet)

#Liste url site 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('accueil/', views.accueil, name='accueil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('check-email/', views.check_email, name='check_email'),
    path('api/', include(router.urls)), 
]
