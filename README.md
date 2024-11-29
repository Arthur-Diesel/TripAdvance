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

# Fluxo de Execução

1. Login / registrar-se
2. O usuário faz upload de um arquivo CSV.
3. O sistema processa os dados para limpeza e normalização.
4. São geradas visualizações estatísticas e interativas.
5. O usuário escolhe o modelo e ajusta os parâmetros.
6. O modelo é treinado e avaliado.
7. O usuário pode realizar previsões com base em entradas personalizadas.

<br>

## Detalhamento do treinamento

### Funções Principais de treino e predição
#### 1. Preprocessamento dos Dados (preprocess_data)
A função de preprocessamento é responsável por preparar os dados para análise e treinamento do modelo. Ela recebe como entrada o caminho para o arquivo CSV e retorna um DataFrame processado, executando as seguintes etapas:
- Carregamento dos dados do arquivo CSV
- Remoção de registros com valores nulos
- Conversão das colunas relevantes para tipos numéricos
- Normalização da coluna duration(minutes) utilizando MinMaxScaler

#### 2. Visualizações Estatísticas (plot_data)
Esta função gera visualizações estáticas importantes para análise dos dados, recebendo como entrada o DataFrame processado. Os gráficos gerados incluem:
- Gráfico de dispersão mostrando a relação entre duração e preço
- Gráfico de pizza apresentando a distribuição das cidades de partida
- Gráfico de barras exibindo os preços médios por cidade
- Linha de tendência com ajuste linear entre duração e preço
- Gráficos interativos com dados de cidade e voo

#### 3. Visualizações Interativas
O sistema oferece três tipos principais de visualizações interativas:
- **Dispersão Interativa (plot_interactive_scatter)**: Demonstra a correlação entre duração e preço, categorizada por cidade de partida
- **Área (plot_interactive_area)**: Apresenta a distribuição de preços por cidade de partida
- **Linha (plot_interactive_line)**: Exibe o preço médio por cidade de partida

#### 4. Treinamento de Modelos (train_model)
A função de treinamento aceita como entrada o DataFrame processado, o tipo de modelo (Árvore de Decisão ou KNN) e os parâmetros específicos do modelo. Ela retorna:
- O modelo treinado
- Métricas de desempenho (MAE e RMSE)

O processo de treinamento inclui:
- Divisão dos dados em conjuntos de treino e teste
- Seleção e configuração do modelo com base nos parâmetros fornecidos
- Avaliação do desempenho do modelo

#### 5. Interface Interativa (interactive_interface)
A interface interativa oferece as seguintes funcionalidades:
- Upload de arquivos CSV
- Seleção do tipo de modelo e configuração de parâmetros
- Geração de visualizações dos dados
- Treinamento do modelo selecionado
- Previsão de valores com base em entradas do usuário

Os elementos interativos incluem:
- Área para upload de arquivos
- Sliders para ajuste de parâmetros
- Botões para análise de dados e realização de previsões
- 
<br>

## Requisitos do Sistema
- Python 3.8 ou superior
- Django 4.0 ou superior
- Bibliotecas adicionais:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `scikit-learn`
  - `charts-js`
  - `bootstrap`
  - `jquery`

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
