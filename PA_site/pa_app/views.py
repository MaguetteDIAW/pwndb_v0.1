from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Mails, DbMails, MailsDbMails
from .serializers import MailsSerializer, DbMailsSerializer, MailsDbMailsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# fonction POST pour l'inscription + verif validation du formulaire 
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})



# fonction POST pour la connexion user + sinon incription /ou auth non valid 
def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')


@login_required
def accueil(request):
    return render(request, 'accueil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

class MailsViewSet(viewsets.ModelViewSet):
    queryset = Mails.objects.all()
    serializer_class = MailsSerializer
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            response_data = []
            for item in request.data:
                email = item.get('email')
                if Mails.objects.filter(email=email).exists():
                    response_data.append({
                        "email": email,
                        "error": "Duplicate entry"
                    })
                else:
                    serializer = self.get_serializer(data=item)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    response_data.append(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email:
            self.queryset = self.queryset.filter(email=email)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

# verifie l'email en BD
""" def check_email(request):
    message = ""
    message_type = ""
    emails_found = None  # list stocker les résultats trouvés
    
    if request.method == "POST":
        email_query = request.POST.get("query")
        emails_found = Mails.objects.filter(email__icontains=email_query)
        if emails_found.exists():
            message = "Attention on a trouvé votre adresse email dans notre base de données."
            message_type = "error"
        else:
            message = "Pas de fuites de données trouvées."
            message_type = "success"
    
    return render(request, 'accueil.html', {
        'message': message,
        'message_type': message_type,
        'emails_found': emails_found  # passe les résultats trouvés au template
    }) """

#verifie Email + domain en BD 
def check_email(request):
    message = ""
    message_type = ""
    emails_found = None

    if request.method == "POST":
        query = request.POST.get("query").strip().lower()
        if '@' in query:
            # La requête semble être une adresse email
            emails_found = Mails.objects.filter(email__iexact=query)
        else:
            # La requête semble être un nom de domaine
            # Recherche d'emails contenant ce domaine
            emails_found = Mails.objects.filter(email__regex=r'@' + query + r'\.')
        
        if emails_found.exists():
            message = "Attention on a trouvé votre adresse email dans notre base de données."
            message_type = "error"
        else:
            message = "Pas de fuites de données trouvées."
            message_type = "success"

    return render(request, 'accueil.html', {
        'message': message,
        'message_type': message_type,
        'emails_found': emails_found
    })




class DbMailsViewSet(viewsets.ModelViewSet):
    queryset = DbMails.objects.all()
    serializer_class = DbMailsSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MailsDbMailsViewSet(viewsets.ModelViewSet):
    queryset = MailsDbMails.objects.all()
    serializer_class = MailsDbMailsSerializer
