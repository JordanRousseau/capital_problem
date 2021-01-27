import numpy as np
import matplotlib.pyplot as plot

def test(data): 
  
  years = []
  months =data['janvier','février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre','décembre']

  #for i, month in enumerate(months, start= 0):
  #  years.append(data[:,i])

  month = 0
  fig, ax = plot.subplots()

  title = plot.title("Température de l'année")
  #print(data['janvier'])
  #ax.plot(data[:,0], data)
  df = data[months[month]]
  df.plot(kind='line',ax=ax, xlabel='Jours', ylabel='Température en °C');

  ax.grid(True)

  plot.show()

  # app_simple.layout = html.Div(children=[
  #   html.H1(children='Hello Dash'),

  #   html.Div(children='''
  #       Dash: A web application framework for Python.
  #   '''),

  #   dcc.Graph(
  #       id='example-graph',
  #       figure={
  #           'data': [
  #               {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
  #               {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
  #           ],
  #           'layout': {
  #               'title': 'Dash Data Visualization'
  #           }
  #       }
  #   )
  # ])