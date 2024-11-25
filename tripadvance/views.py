from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm, UploadForm
from archives.models import Archive
from trainedmodel.models import TrainedModel
import csv
import os
import datetime
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pickle
import matplotlib

matplotlib.use('Agg')

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
                    return render(request, 'upload.html', {'error': 'O arquivo deve conter as colunas date, start_city, end_city, airline, duration e price.'})
            
            df = pd.read_csv(f'./tripadvance/archives/{filename}')
            if df.isnull().values.any():
                os.remove(f'./tripadvance/archives/{filename}')
                return render(request, 'upload.html', {'error': 'O arquivo não pode conter valores nulos.'})
        
            archiveCreated = Archive.objects.create(created_by=request.user, path=f'./tripadvance/archives/{filename}', created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
            archiveCreated.save()
            return render(request, 'upload.html', {'success': 'Arquivo enviado com sucesso, salvo com o nome: ' + filename})
    return render(request, 'upload.html')

@login_required
def train(request):
    user = request.user
    archives = Archive.objects.all()
    new_csv = pd.DataFrame(columns=['date', 'start_city', 'end_city', 'airline', 'duration', 'price'])
    for archive in archives:
        csv = pd.read_csv(archive.path)
        new_csv = pd.concat([new_csv, csv], ignore_index=True)
    new_csv.to_csv('./tripadvance/static/trainedmodel/training_data.csv', index=False)
    name = 'model_' + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + f'_{user.username}' + '.pkl'
    type = request.POST.get('type')
    df = pd.read_csv('./tripadvance/static/trainedmodel/training_data.csv')
    df = df.dropna()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df = df.dropna(subset=['price', 'duration'])
    scaler = MinMaxScaler()
    df['duration'] = scaler.fit_transform(df[['duration']])
    x = df[['duration']]
    y = df['price']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = None

    if type == 'decision_tree':
        depth = request.POST.get('model_depth')
        depth = None if depth == '' else int(depth)
        model = DecisionTreeRegressor(max_depth=depth, random_state=42)
    else : #KNN
        neighbors = request.POST.get('model_neighbors')
        neighbors = None if neighbors == '' else int(neighbors)
        model = KNeighborsRegressor(n_neighbors=neighbors)        
    
    model.fit(x_train, y_train)
    with open(f'./tripadvance/models/{name}', 'wb') as f:
        pickle.dump(model, f)
    
    userModels = TrainedModel.objects.filter(created_by=request.user)
    for userModel in userModels:
        if os.path.exists(userModel.path):
            os.remove(userModel.path)
        userModel.delete()
    
    y_pred = model.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    trainedModel = TrainedModel.objects.create(
        path=f'./tripadvance/models/{name}',
        created_by=request.user,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        mae=mae,
        mse=mse,
        rmse=rmse)
    trainedModel.save()
    
    return render(request, 'predict.html', {'success': 'Modelo treinado com sucesso.'})

@login_required
def graphs(request):
    if not os.path.exists('./tripadvance/static/trainedmodel/training_data.csv'):
        return render(request, 'graphs.html', {'error': 'Você ainda não treinou um modelo.'})
    
    df = pd.read_csv('./tripadvance/static/trainedmodel/training_data.csv')
    df['start_city'] = df['start_city'].str.strip().str.title()
    df['end_city'] = df['end_city'].str.strip().str.title()
    df['start_city'] = df['start_city'].str.replace("\ufffdN", "an")
    df['end_city'] = df['end_city'].str.replace("\ufffdN", "an")
    
    city_counts = df['start_city'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(city_counts, labels=city_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.axis('equal')
    plt.savefig(f'./tripadvance/static/imgs/generated_pie.png')
    
    avg_price_by_city = df.groupby('start_city')['price'].mean().sort_values()
    plt.figure(figsize=(10, 6))
    avg_price_by_city.plot(kind='bar', color='green', alpha=0.8)
    plt.xlabel("Cidade de Partida")
    plt.ylabel("Preço Médio (USD)")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'./tripadvance/static/imgs/generated_bar.png')    
    
    plt.figure(figsize=(8, 6))
    plt.scatter(df['duration'], df['price'], color='blue', alpha=0.7, label="Dados")
    z = np.polyfit(df['duration'], df['price'], 1)
    p = np.poly1d(z)
    plt.plot(df['duration'], p(df['duration']), color='red', linewidth=2, label="Tendência")
    plt.xlabel("Duração (min)")
    plt.ylabel("Preço (USD)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f'./tripadvance/static/imgs/generated_trend.png')
    return render(request, 'graphs.html', {'data': df.to_json()})
    

@login_required
def predict(request):
    if request.method == 'GET':
        model = TrainedModel.objects.filter(created_by=request.user).last()
        model.created_at = model.created_at.strftime('%d/%m/%Y %H:%M:%S')
        return render(request, 'predict.html', {'model': model})
    if request.method == 'POST':
        start_interval = request.POST.get('start_interval')
        end_interval = request.POST.get('end_interval')
        start_interval = None if start_interval == '' else int(start_interval)
        end_interval = None if end_interval == '' else int(end_interval)
        middle = (start_interval + end_interval) / 2
        model = TrainedModel.objects.filter(created_by=request.user).last()
        if model is None:
            return render(request, 'predict.html', {'error': 'Você ainda não treinou um modelo.'})
        model_path = model.path        
        model = TrainedModel.objects.filter(created_by=request.user).last()
        model.created_at = model.created_at.strftime('%d/%m/%Y %H:%M:%S')
        with open(model_path, 'rb') as file:
            modelLoaded = pickle.load(file)
            prediction = modelLoaded.predict([[middle]])
            prediction = prediction.tolist() if isinstance(prediction, np.ndarray) else prediction
            prediction = round(prediction[0], 2)
            return render(request, 'predict.html', {'prediction': prediction, 'model': model})

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