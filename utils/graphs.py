# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:33:25 2023

@author: gieseking
"""
import utils.queries as queries
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import pandas as pd


def matches_month(c, season, combos, js=False):
    from datetime import datetime
    now = datetime.now().year
    months = ['Jan','Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec']
    years = [str(y) for y in range(season[0]-1,min(season[-1]+1,now+1))]
    fig = go.Figure()
    dfs = {}
    for com in combos:
        print('Generating matches per month for '+com[4])
        squery = queries.count_matches_month(category=com[0], ends=com[1], 
                                       rank1 = com[2], rank2 = com[3], 
                                       season=season)
        df = pd.DataFrame()
        for s in squery:
            result = c.execute(s).fetchall()
            #print(result)
            df = pd.concat([df,
                            pd.DataFrame({'Year':  [r[0] for r in result],
                                          'Month': [r[1] for r in result],
                                          'count': [r[2] for r in result]})])
        dfs[com[4]] = pd.pivot(df, columns='Year', 
                               index='Month',
                               values='count').fillna(0).astype(int)
        dfs[com[4]] = dfs[com[4]].reindex(list(range(1,13)), fill_value=0)
        #print(dfs[com[4]])
        show = True if com == combos[0] else False
        fig.add_trace(go.Heatmap(x=years, 
                                 y=months, 
                                 z=dfs[com[4]].values.tolist(),
                                 colorscale="Viridis",
                                 visible=show,
                                 hovertemplate='# Matches: %{z}<br>'+
                                     'Month: %{y} %{x}<extra></extra>'))
    traces = [com[4] for com in combos]
    
    buttons = []
    vis = [list(b) for b in [e==1 for e in np.eye(len(traces))]]
    for i, t in enumerate(traces):
        buttons.append(dict(method='update',
                            label=t,
                            args=[{'visible':vis[i]}]
                            ))
    fig.update_layout(
        yaxis = dict(autorange="reversed"),
        #title = 'Matches per Month',
        #title_x=0.5,
        xaxis_title = 'Year',
        yaxis_title = 'Month',
        height=700,
        width=1200,
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(size=18),
        updatemenus=[
            go.layout.Updatemenu(
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.2,
                yanchor="top"
            ),
        ])
    
    return plotly.io.to_html(fig, include_plotlyjs=js, full_html=False)

def final_scores(c, season, combos, js=False):
    fig = go.Figure()
    dfs = {}
    scores = list(range(0,13))
    for com in combos:
        print('Generating final scores for '+com[4])
        squery = queries.count_final_scores(category=com[0], ends=com[1], 
                                       rank1 = com[2], rank2 = com[3], 
                                       season=season)
        df = pd.DataFrame()
        for s in squery:
            result = c.execute(s).fetchall()
            #print(result)
            df = pd.concat([df,
                            pd.DataFrame({'Final1':  [r[0] for r in result],
                                          'Final2': [r[1] for r in result],
                                          'count': [r[2] for r in result]})])
        dfs[com[4]] = pd.pivot_table(df, columns='Final1', 
                               index='Final2',
                               values='count',
                               aggfunc='sum').fillna(0).astype(int)
        dfs[com[4]] = dfs[com[4]].reindex(scores, fill_value=0,
                                          axis=0)
        dfs[com[4]] = dfs[com[4]].reindex(scores, fill_value=0,
                                          axis=1)
        percent = dfs[com[4]]/dfs[com[4]].sum().sum()
        #print(percent)
        #print(dfs[com[4]])
        show = True if com == combos[0] else False
        fig.add_trace(go.Heatmap(x=scores, 
                                 y=scores, 
                                 z=dfs[com[4]].values.tolist(),
                                 customdata=percent,
                                 colorscale="Viridis",
                                 visible=show,
                                 hovertemplate='Final score: %{x}-%{y}<br>'+
                                     'Matches: %{z} (%{customdata:.2%})'+
                                     '<extra></extra>'))
    traces = [com[4] for com in combos]
    
    buttons = []
    vis = [list(b) for b in [e==1 for e in np.eye(len(traces))]]
    for i, t in enumerate(traces):
        buttons.append(dict(method='update',
                            label=t,
                            args=[{'visible':vis[i]}]
                            ))
    fig.update_layout(
        #title = 'Final Scores',
        #title_x=0.5,
        xaxis_title = 'Team 1 Final Score',
        yaxis_title = 'Team 2 Final Score',
        height=700,
        width=720,
        margin=dict(l=20, r=20, t=120, b=20),
        font=dict(size=18),
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
    
    return plotly.io.to_html(fig, include_plotlyjs=js, full_html=False)

def end_scores(c, season, combos, js=False):
    from plotly.subplots import make_subplots
    plotly.io.templates.default = "simple_white"
    fig = make_subplots(rows=1, cols=3,
                        shared_yaxes=False,
                        subplot_titles=['Scores, Team 1 Hammer', 
                                        'Scores, Team 2 Hammer',
                                        'Hammer By End'])
    scores = list(range(-5,6))
    vis = []
    traces = []
    for com in combos:
        if com[1] == None:
            continue
        traces.append(com[4])
        print('Generating end scores for '+com[4])
        squery = queries.get_end_scores(category=com[0], ends=com[1], 
                                       rank1 = com[2], rank2 = com[3], 
                                       season=season)
        matches = pd.DataFrame()
        for s in squery:
            result = c.execute(s).fetchall()
            #print(result)
            matches = pd.concat([matches,
                        pd.DataFrame(result,
                                     columns=['Final1','Final2',
                                              'End1', 'Ham1', 'End2', 'Ham2', 
                                              'End3', 'Ham3', 'End4', 'Ham4',
                                              'End5', 'Ham5', 'End6', 'Ham6', 
                                              'End7', 'Ham7', 'End8', 'Ham8',
                                              'End9', 'Ham9', 'End10', 'Ham10', 
                                              'End11', 'Ham11', 'End12', 'Ham12'])])
        hammer = pd.DataFrame(columns=['Team 1 Hammer','Team 2 Hammer', 
                                       'Team 1 Win', 'Team 2 Win'])
        ham1 = pd.DataFrame()
        ham2 = pd.DataFrame()
        endcols = []
        for e in range(1,com[1]+2):
            endcols.append('End'+str(e))
            ham1 = pd.concat([ham1, 
                    matches[matches['Ham'+str(e)]==1]['End'+str(e)].value_counts()], 
                    axis=1)
            ham2 = pd.concat([ham2, 
                    matches[matches['Ham'+str(e)]==-1]['End'+str(e)].value_counts()], 
                    axis=1)
            hammer.loc[e] = [matches['Ham'+str(e)].value_counts()[1],
                             matches['Ham'+str(e)].value_counts()[-1],
                             matches[(matches['Final1'] + matches['Final2'] == 
                                      matches[endcols].abs().sum(axis=1)) &
                                     (matches['Final1'] > matches['Final2'])
                                     ]['Ham'+str(e)].isna().sum(),
                             matches[(matches['Final1'] + matches['Final2'] == 
                                      matches[endcols].abs().sum(axis=1)) &
                                     (matches['Final1'] < matches['Final2'])
                                     ]['Ham'+str(e)].isna().sum(),
                             ]
        #print(matches[matches['Final1'] > matches['Final2']
        #        ].count())
        hammer.loc[com[1]+2] = [0, 0, 
                                matches[matches['Final1'] > matches['Final2']
                                        ].shape[0],
                                matches[matches['Final1'] < matches['Final2']
                                        ].shape[0]]

        hammer["Unknown Hammer"] = len(matches) - hammer.sum(axis=1)
        hammer = hammer/len(matches)*100
        #print(hammer) 
        
        ham1 = ham1/len(matches)*100
        ham1.index = ham1.index.astype(int) 
        ham1 = ham1.reindex(scores).fillna(0)
        #print(ham1)
            
        ham2 = ham2/len(matches)*100
        ham2.index = -ham2.index.astype(int) 
        ham2 = ham2.reindex(scores).fillna(0)
        #print(ham2)
        
        colors = plotly.colors.sample_colorscale('Viridis', com[1]+1)
        show = True if len(vis)==0 else False
        
            
        for i in range(com[1]+1):
            fig.add_trace(go.Scatter(x=ham1.index,
                                     y=ham1['End'+str(i+1)],
                                     name='End '+str(i+1),
                                     marker=dict(color=colors[i], size=8),
                                     line=dict(color=colors[i]),
                                     visible=show,
                                     meta=[str(i+1)],
                                     hovertemplate='End %{meta[0]}'+
                                         ' score %{x}, team 1 hammer<br>'+
                                         'Frequency: %{y:.2f}%'+
                                         '<extra></extra>'),
                          row=1, col=1)
            fig.add_trace(go.Scatter(x=ham2.index,
                                     y=ham2['End'+str(i+1)],
                                     name='End '+str(i+1),
                                     marker=dict(color=colors[i], size=8),
                                     line=dict(color=colors[i]),
                                     visible=show,
                                     showlegend=False,
                                     meta=[str(i+1)],
                                     hovertemplate='End %{meta[0]}'+
                                         ' score %{x}, team 2 hammer<br>'+
                                         'Frequency: %{y:.2f}%'+
                                         '<extra></extra>'),
                          row=1, col=2)
        ham_colors = ['red','blue','maroon','navy','silver']
        for i, col in enumerate(hammer.columns):
            shape = 'square' if i%2 == 0 else 'diamond'
            size = 10 if i%2 == 0 else 8
            dash = 'solid' if i%2 == 0 else 'dash'
            fig.add_trace(go.Scatter(x=hammer.index,
                                     y=hammer[col],
                                     name=col,
                                     marker=dict(color=ham_colors[i], 
                                                 size=size,
                                                 symbol=shape),
                                     line=dict(color=ham_colors[i],
                                               dash=dash),
                                     visible=show,
                                     meta=[col],
                                     hovertemplate='%{meta[0]}, End %{x}<br>'+
                                         'Frequency: %{y:.2f}%'+
                                         '<extra></extra>'),
                          row=1, col=3)
        if len(vis) == 0:
            vis.append([True]*((com[1]+1)*2+5))
        else: 
            curr_len = len(vis[-1])
            for v in vis:
                v.extend([False]*((com[1]+1)*2+5))
            vis.append([False]*curr_len+[True]*((com[1]+1)*2+5))
    #print(len(fig.data))
    #print('vis',len(vis[0]), len(vis[-1]))    
    #traces = [com[4] for com in combos]
    buttons = []
    #vis = [list(b) for b in [e==1 for e in np.eye(len(traces))]]
    for i, t in enumerate(traces):
        buttons.append(dict(method='update',
                            label=t,
                            args=[{'visible':vis[i]}]
                            ))
    fig.update_layout(
        #title = 'End Scores',
        #title_x=0.5,
        xaxis_title = 'Team 1 End Score',
        xaxis2_title= 'Team 2 End Score',
        xaxis3_title= 'End',
        yaxis_title = 'Percentage of Matches',
        legend={'font':{'size':18},
                #'title':{'text':'End'}
                },
        #legend_title_text='End',
        height=700,
        width=1200,
        margin=dict(l=20, r=20, t=120, b=20),
        font=dict(size=18),
        updatemenus=[
            go.layout.Updatemenu(
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.2,
                yanchor="top"
            ),
        ])
    
    return plotly.io.to_html(fig, include_plotlyjs=js, full_html=False)

def win_probability(c, season, combos, js=False):
    from plotly.subplots import make_subplots
    plotly.io.templates.default = "simple_white"
    fig = make_subplots(rows=1, cols=2,
                        shared_yaxes=True,
                        subplot_titles=['Team 1 Hammer', 'Team 2 Hammer'])
    vis = []
    traces = []
    for com in combos:
        if com[1] == None:
            continue
        traces.append(com[4])
        print('Generating win probabilities for '+com[4])
        squery = queries.get_end_scores(category=com[0], ends=com[1], 
                                       rank1 = com[2], rank2 = com[3], 
                                       season=season)
        matches = pd.DataFrame()
        for s in squery:
            result = c.execute(s).fetchall()
            #print(result)
            matches = pd.concat([matches,
                        pd.DataFrame(result,
                                     columns=['Final1','Final2',
                                              'End1', 'Ham1', 'End2', 'Ham2', 
                                              'End3', 'Ham3', 'End4', 'Ham4',
                                              'End5', 'Ham5', 'End6', 'Ham6', 
                                              'End7', 'Ham7', 'End8', 'Ham8',
                                              'End9', 'Ham9', 'End10', 'Ham10', 
                                              'End11', 'Ham11', 'End12', 'Ham12'])])
        matches['Win1'] = np.where(matches['Final1'] > matches['Final2'], 
                                   True, False)
        matches['Margin0'] = 0
        matches['Margin1'] = matches['End1']
        for e in range(2,com[1]+2):
            matches['Margin'+str(e)] = (matches['Margin'+str(e-1)] + 
                                        matches['End'+str(e)])
        margin = list(range(-5,6))
        margin_cols = ['Margin'+str(m) for m in margin]
        win_cols = ['Win'+str(m) for m in margin]
        prob_cols = ['Prob'+str(m) for m in margin]
        text_cols = ['Text'+str(m) for m in margin]
        all_cols = margin_cols + win_cols + prob_cols
        #pd.set_option('display.max_columns', None)
        #print(matches.head())
        ham1 = pd.DataFrame(columns=all_cols)
        ham2 = pd.DataFrame(columns=all_cols)
        for e in range(1,com[1]+2):
            for m in margin:
                ham1.at[e,'Margin'+str(m)] = (
                    matches[(matches['Margin'+str(e-1)] == m) &
                            (matches['Ham'+str(e)] == 1)].shape[0])
                ham1.at[e,'Win'+str(m)] = (
                    matches[(matches['Margin'+str(e-1)] == m) &
                            (matches['Ham'+str(e)] == 1) &
                            (matches['Win1'] == True)].shape[0])
                ham1.at[e,'Prob'+str(m)] = (ham1.at[e,'Win'+str(m)] / 
                                            ham1.at[e,'Margin'+str(m)]*100 
                                            if ham1.at[e,'Margin'+str(m)] > 0 
                                            else None)
                ham1.at[e,'Text'+str(m)] = (str(ham1.at[e,'Win'+str(m)]) + '/' +
                                            str(ham1.at[e,'Margin'+str(m)]))
                ham2.at[e,'Margin'+str(m)] = (
                    matches[(matches['Margin'+str(e-1)] == m) &
                            (matches['Ham'+str(e)] == -1)].shape[0])
                ham2.at[e,'Win'+str(m)] = (
                    matches[(matches['Margin'+str(e-1)] == m) &
                            (matches['Ham'+str(e)] == -1) &
                            (matches['Win1'] == True)].shape[0])
                ham2.at[e,'Prob'+str(m)] = (ham2.at[e,'Win'+str(m)] / 
                                            ham2.at[e,'Margin'+str(m)]*100 
                                            if ham2.at[e,'Margin'+str(m)] > 0 
                                            else None)
                ham2.at[e,'Text'+str(m)] = (str(ham2.at[e,'Win'+str(m)]) + '/' +
                                            str(ham2.at[e,'Margin'+str(m)]))
        for m in margin:
            if m == 0: 
                continue
            ham1.at[com[1]+1,'Margin'+str(m)] = None
            ham1.at[com[1]+1,'Win'+str(m)] = None
            ham1.at[com[1]+1,'Prob'+str(m)] = None
            ham2.at[com[1]+1,'Margin'+str(m)] = None
            ham2.at[com[1]+1,'Win'+str(m)] = None
            ham2.at[com[1]+1,'Prob'+str(m)] = None
            
        #print(ham1[prob_cols])
        #print(ham2[prob_cols])
        
        show = True if len(vis)==0 else False
        fig.add_trace(go.Heatmap(x=margin, 
                             y=list(range(1,com[1]+2)), 
                             z=ham1[prob_cols].values.tolist(),
                             meta=ham1[text_cols].values.tolist(),
                             colorscale="RdBu", reversescale=True,
                             visible=show,
                             hovertemplate='Team 1 Win Probability: %{z:.1f}%<br>'+
                                 '(%{meta} matches)<br>'+
                                 'Team 1 Hammer in End %{y}, Margin %{x}'+
                                 '<extra></extra>'),
                      row=1, col=1)
        fig.add_trace(go.Heatmap(x=margin, 
                             y=list(range(1,com[1]+2)), 
                             z=ham2[prob_cols].values.tolist(),
                             meta=ham2[text_cols].values.tolist(),
                             colorscale="RdBu", reversescale=True,
                             visible=show,
                             hovertemplate='Team 1 Win Probability: %{z:.1f}%<br>'+
                                 '(%{meta} matches)<br>'+
                                 'Team 2 Hammer in End %{y}, Margin %{x}'+
                                 '<extra></extra>'),
                      row=1, col=2)
        if len(vis) == 0:
            vis.append([True]*2)
        else: 
            curr_len = len(vis[-1])
            for v in vis:
                v.extend([False]*2)
            vis.append([False]*curr_len+[True]*2)

    buttons = []
    for i, t in enumerate(traces):
        buttons.append(dict(method='update',
                            label=t,
                            args=[{'visible':vis[i]}]
                            ))
    fig.update_layout(
        #yaxis = dict(autorange="reversed"),
        xaxis_title = 'Team 1 Points Margin',
        xaxis2_title = 'Team 1 Points Margin',
        yaxis_title = 'End',
        height=700,
        width=1200,
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(size=18),
        updatemenus=[
            go.layout.Updatemenu(
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.2,
                yanchor="top"
            ),
        ])
    
    return plotly.io.to_html(fig, include_plotlyjs=js, full_html=False)


'''
def plot_matches_month(c, ends = None, category = None, 
                        rank1 = None, rank2 = None, season = None):
    text = queries.count_matches_month(category=category, ends=ends, 
                                   rank1 = rank1, rank2 = rank2, 
                                   season=season)
    count = []
    for t in text:
        #print(q)
        count.extend(c.execute(t).fetchall())
    years = list(range(season[0]-1, season[-1]+1))
    months = list(range(1,13))
    matches = np.zeros([len(years),len(months)])
    season = [season[0]-1] + season
    for i in count:
        #print(i)
        matches[season.index(i[0]),i[1]-1] = i[2]
    #print(matches)
    plt.pcolormesh(months, years, matches)
    plt.colorbar()
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.title('Matches by Month')
    plt.show()

    return 

def plot_final_scores(c, ends = 8, category = None, 
                        rank1 = None, rank2 = None, season = None):
    text = queries.count_final_scores(category=category, ends=ends, 
                                   rank1 = rank1, rank2 = rank2, 
                                   season=season)
    count = []
    for t in text:
        #print(t)
        count.extend(c.execute(t).fetchall())
    maxrange = 16
    axis = list(range(maxrange))
    score_dist = np.zeros(maxrange)
    score_pair_dist = np.zeros((maxrange,maxrange))
    for i in count:
        if int(i[1]) < maxrange and int(i[0]) < maxrange:
            score_pair_dist[int(i[1]),int(i[0])] += i[2]
            score_dist[int(i[0])] += i[2]
            score_dist[int(i[1])] += i[2]
    score_dist /= np.sum(score_dist)
    score_pair_dist /= np.sum(score_pair_dist)
    
    # Plot individual and paired score distribution
    plt.bar(axis, score_dist, color='#440154')
    plt.xlabel('Final score')
    plt.ylabel('Fraction of Matches')
    plt.show()

    plt.pcolormesh(axis, axis, score_pair_dist, vmin=0, vmax=0.05)
    plt.colorbar()
    plt.xlabel('Team 1 Score')
    plt.ylabel('Team 2 Score')
    plt.title('Matches by Final Score')
    plt.show()
    
    return

def plot_end_scores(c, ends = 8, category = None, 
                        rank1 = None, rank2 = None, season = None,
                        plot_end = [1]):
    text = queries.get_end_scores(category=category, ends=ends, 
                                   rank1 = rank1, rank2 = rank2, 
                                   season=season)
    scores = []
    for t in text:
        scores.extend(c.execute(t).fetchall())
    import pandas as pd
    scores = pd.DataFrame(scores, columns = ['End1', 'Ham1', 'End2', 'Ham2', 
                                             'End3', 'Ham3', 'End4', 'Ham4',
                                             'End5', 'Ham5', 'End6', 'Ham6', 
                                             'End7', 'Ham7', 'End8', 'Ham8',
                                             'End9', 'Ham9', 'End10', 'Ham10', 
                                             'End11', 'Ham11', 'End12', 'Ham12'])
    ham1 = pd.DataFrame()
    ham2 = pd.DataFrame()
    for end in plot_end:
        ham1 = pd.concat([ham1, 
                          scores[scores['Ham'+str(end)]==1]['End'+str(end)].value_counts()], 
                         axis=1)
        ham2 = pd.concat([ham2, 
                          scores[scores['Ham'+str(end)]==-1]['End'+str(end)].value_counts()], 
                         axis=1)
    
    ham1.index = ham1.index.astype(int) 
    ham1 = ham1.sort_index().fillna(0).astype(int)
    #print(ham1)
    
    print('ham2',ham2)
    ham2['i'] = ham2.index.astype(int) 
    print(ham2['i'])
    ham2.set_index('i')
    ham2 = ham2.sort_index().fillna(0).astype(int)
    print('ham2',ham2)
    
    colors = plt.cm.viridis(np.linspace(0,1,len(plot_end)))
    
    plt.figure()
    ham1.plot(color=colors)
    plt.legend(loc='best')
    plt.show()
    plt.figure()
    ham2.plot(color=colors)
    plt.legend(loc='best')
    plt.show()
    
    #import plotly.express as px
    #fig = px.line(ham1, x=ham1.index, y="End1")
    #fig.show()
    
    return
'''