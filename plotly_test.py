# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:56:18 2023

@author: gieseking
"""

import plotly.express as px
import plotly
import plotly.subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

'''
b2_show = [list(b) for b in [e==1 for e in np.eye(10)]]
print(b2_show)

data = [[0, 139, 235], 
        [0, 38, 84], 
        [0, 134, 99], 
        [0, 44, 61], 
        [0, 34, 61], 
        [158, 179, 116], 
        [394, 650, 316], 
        [800, 703, 333], 
        [591, 827, 185], 
        [247, 359, 0]]
year = ['2021', '2022', '2023']
month = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
fig = go.Figure(go.Heatmap(x=year, 
                 y=month, 
                 z=data,
                 colorscale='Viridis'))
plotly.io.write_html(fig, 'test.html')
'''

df = pd.DataFrame({'End1': [0,0,1,5,30,143,293,362,420,159,62,13,1,1,
                            0,0,11,19,141,324,159,180,86,22,11,0,0,0],
                   'End2': [0,0,1,9,21,104,133,266,286,145,34,5,1,0,
                            0,2,8,40,204,527,239,339,143,52,15,3,0,0],
                   'End3': [0,0,2,9,27,123,143,250,309,131,46,16,2,0,
                            0,1,10,25,208,547,165,318,168,51,21,7,0,0],
                   'End4': [0,1,1,7,29,124,115,312,303,150,48,15,6,2,
                            0,3,13,47,191,519,148,285,160,75,16,3,0,0],
                   'End5': [0,0,2,6,20,137,102,247,308,141,36,16,3,0,
                            1,2,12,45,197,493,121,296,132,45,20,5,1,1],
                   'End6': [0,1,1,4,25,98,86,278,273,122,54,12,2,1,
                            1,2,9,34,186,453,72,236,110,53,17,9,0,0],
                   'End7': [0,1,0,5,21,81,102,225,215,84,34,6,2,0,
                            1,0,9,33,135,290,73,157,80,30,6,0,1,0],
                   'End8': [0,0,0,3,9,67,18,226,104,16,9,0,0,0,
                            0,0,3,15,61,127,11,88,43,16,0,0,0,0],
                   'End9': [0,0,0,0,1,7,0,72,16,2,0,0,0,0,
                            0,0,1,1,2,31,1,18,6,0,0,0,0,0],
                   'Hammer': [1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                              2,2,2,2,2,2,2,2,2,2,2,2,2,2]},
                  index = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7,
                           -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7])
#print(df)
#print(df[df['Hammer']==1]['End1'])

colors = px.colors.sample_colorscale('viridis',len(df.columns.tolist())-1)
fontmin = 18

fig = plotly.subplots.make_subplots(rows=1, cols=2,
                                    shared_yaxes=True,
                                    subplot_titles=['Team 1 Hammer', 'Team 2 Hammer'])

for i in range(9):
    fig.add_trace(go.Scatter(x=df[df['Hammer']==1].index,
                             y=df[df['Hammer']==1]['End'+str(i+1)],
                             name=str(i+1),
                             marker=dict(color=colors[i], size=8),
                             line=dict(color=colors[i])),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df[df['Hammer']==2].index,
                             y=df[df['Hammer']==2]['End'+str(i+1)],
                             name=str(i+1),
                             marker=dict(color=colors[i], size=8),
                             line=dict(color=colors[i]),
                             showlegend=False),
                  row=1, col=2)
fig.update_layout(title="Score probabilities by end",
                  title_x=0.5,
                  title_y=0.99,
                  xaxis = dict(tickfont = dict(size=fontmin)),
                  yaxis = dict(tickfont = dict(size=fontmin)),
                  xaxis_title="Score",
                  xaxis2_title="Score",
                  yaxis_title="Probability",
                  legend_title="End",
                  font=dict(size=fontmin),
                  template='simple_white',
                  margin=dict(l=20, r=20, t=100, b=20))

buttons=list([dict(args=[{'y':[df[df['Hammer']==1]['End1'],
                               df[df['Hammer']==2]['End1'],
                               df[df['Hammer']==1]['End2'],
                               df[df['Hammer']==2]['End2'],
                               df[df['Hammer']==1]['End3'],
                               df[df['Hammer']==2]['End3'],
                               df[df['Hammer']==1]['End4'],
                               df[df['Hammer']==2]['End4'],
                               df[df['Hammer']==1]['End5'],
                               df[df['Hammer']==2]['End5'],
                               df[df['Hammer']==1]['End6'],
                               df[df['Hammer']==2]['End6'],
                               df[df['Hammer']==1]['End7'],
                               df[df['Hammer']==2]['End7'],
                               df[df['Hammer']==1]['End8'],
                               df[df['Hammer']==2]['End8'],
                               df[df['Hammer']==1]['End9'],
                               df[df['Hammer']==2]['End9']]}],
                    
                   label="Men (rank 1-25 vs. rank 101-500)",
                   method="restyle"
                ),
              dict(args=[{'y':[df[df['Hammer']==2]['End1'],
                               df[df['Hammer']==1]['End1'],
                               df[df['Hammer']==2]['End2'],
                               df[df['Hammer']==1]['End2'],
                               df[df['Hammer']==2]['End3'],
                               df[df['Hammer']==1]['End3'],
                               df[df['Hammer']==2]['End4'],
                               df[df['Hammer']==1]['End4'],
                               df[df['Hammer']==2]['End5'],
                               df[df['Hammer']==1]['End5'],
                               df[df['Hammer']==2]['End6'],
                               df[df['Hammer']==1]['End6'],
                               df[df['Hammer']==2]['End7'],
                               df[df['Hammer']==1]['End7'],
                               df[df['Hammer']==2]['End8'],
                               df[df['Hammer']==1]['End8'],
                               df[df['Hammer']==2]['End9'],
                               df[df['Hammer']==1]['End9']]}],
                                  
                   label="Men (rank 101-500 vs. rank 1-25)",
                   method="restyle"
                )
            ])
fig.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
    ])

'''
buttons=list([dict(args=[{'y':[df1['A'],df1['B']]}],
                    
                   label="df1",
                   method="restyle"
                ),
                dict(args=[{'y':[df2['A'], df2['B']]}],
                    
                    label="df2",
                    method="restyle"
                )
            ])

fig.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=-0.25,
            xanchor="left",
            y=1,
            yanchor="top"
        ),
    ]
)
'''
'''
fig = px.line(df, x=df.index, y=df.columns.tolist(), 
              facet_col='Hammer',
              color_discrete_sequence=colors,
              template='simple_white')
fig.update_layout(title="Score probabilities by end",
                  xaxis = dict(tickfont = dict(size=fontmin)),
                  yaxis = dict(tickfont = dict(size=fontmin)),
                  xaxis_title="Score",
                  xaxis2_title="Score",
                  yaxis_title="Probability",
                  legend_title="End",
                  font=dict(size=fontmin))
'''
#plotly.io.write_html(fig, 'test.html')
