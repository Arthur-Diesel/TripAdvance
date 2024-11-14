from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm, UploadForm
from archives.models import Archive
import csv
import os
import datetime
import pandas as pd

# Signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após o cadastro
        else:
            # Adiciona erros ao formulário, se houver
            print(form.errors)  # Adicione isso para depurar
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout page
def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'home.html', {'user': user})
    return render(request, 'home.html')

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            if(file.name.endswith('.csv') == False):
                return render(request, 'upload.html', {'error': 'O arquivo deve ser um CSV.'})
            
            archives = os.listdir('./tripadvance/archives')
            filename = file.name
            i = 1
            while filename in archives:
                filename = f'{file.name.split(".csv")[0]}_{i}.csv'
                i += 1
            
            with open(f'./tripadvance/archives/{filename}', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            with open(f'./tripadvance/archives/{filename}', 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                if header != ['date', 'start_city', 'end_city', 'airline', 'duration', 'price']:
                    f.close()
                    os.remove(f'./tripadvance/archives/{filename}')
                    return render(request, 'upload.html', {'error': 'O arquivo deve conter as colunas date, city, start_airport, end_airport, airline, duration e price.'})
            
            df = pd.read_csv(f'./tripadvance/archives/{filename}')
            if df.isnull().values.any():
                os.remove(f'./tripadvance/archives/{filename}')
                return render(request, 'upload.html', {'error': 'O arquivo não pode conter valores nulos.'})
        
            if df.duplicated().values.any():
                os.remove(f'./tripadvance/archives/{filename}')
                return render(request, 'upload.html', {'error': 'O arquivo não pode conter valores duplicados.'})
            
            archiveCreated = Archive.objects.create(created_by=request.user, path=f'./tripadvance/archives/{filename}', created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
            archiveCreated.save()
            return render(request, 'upload.html', {'success': 'Arquivo enviado com sucesso, salvo com o nome: ' + filename})
    return render(request, 'upload.html')

@login_required
def archive(request, id):
    if request.method == 'GET':
        archive = Archive.objects.get(id=id)
        with open(archive.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/csv')
            response['Content-Disposition'] = 'attachment; filename=' + archive.path.split('/')[-1]
            return response
    if request.method == 'POST':
        archive = Archive.objects.get(id=id)
        os.remove(archive.path)
        archive.delete()
        return render(request, 'archives.html', {'success': 'Arquivo deletado com sucesso.'})

@login_required
def archives(request):
    archives = Archive.objects.filter(created_by=request.user)
    for archive in archives:
        archive.filename = archive.path.split('/')[-1]
    return render(request, 'archives.html', {'archives': archives})