<h1 align="center">
  <br>Trip Advance</h1>

**TripAdvance** é um sistema desenvolvido em Django que realiza treinamento e predições para auxiliar no planejamento de viagens. Ele utiliza um modelo de aprendizado de máquina treinado para prever informações úteis, além de integrar gráficos e funcionalidades de scraping para coletar dados atualizados.

<br>

## Estrutura do Projeto
A estrutura principal do projeto é a seguinte:

```
TripAdvance/ 
├── archives/ # Contém arquivos auxiliares e backups 
├── trainedmodel/ # Modelos treinados para predições 
├── tripadvance/ # Aplicação principal do Django 
├── .gitignore # Arquivos ignorados pelo Git 
├── FlightSearch.py # Lógica de scraping e busca de voos 
├── README.md # Documentação principal do projeto 
├── manage.py # Arquivo de gerenciamento do Django
```

<br>

## Funcionalidades
1. **Treinamento de Modelos**: Permite o treinamento de modelos preditivos usando dados históricos.
2. **Predições**: Realiza previsões baseadas no modelo treinado para auxiliar no planejamento de viagens.
3. **Scraping de Dados**: Coleta informações atualizadas de voos por meio do módulo `FlightSearch.py`.
4. **Gráficos Interativos**: Visualiza informações por meio de gráficos implementados no frontend.
5. **Interface Web**: Desenvolvida com Django, proporcionando uma navegação intuitiva.

<br>

## Requisitos do Sistema
- Python 3.8 ou superior
- Django 4.0 ou superior
- Bibliotecas adicionais:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `scikit-learn`
  - `requests`

<br>


## Como Executar o Projeto

### 1. Configurar o Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar o banco de dados
```bash
python manage.py migrate
```

### 4. Executar o Servidor
```bash
python manage.py runserver
```


 <br>

<h2 align="left" >Equipe 🧠</h2>

- Arthur Diesel Ogg (26681706)
- Gabriela Cristina Schmitt (25733150)
- Vinicius Dionizio Patrocinio (27038386)

<br>

✨ Obrigada pela atenção! ✨
