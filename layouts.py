import dash_core_components as dcc
import dash_html_components as html
import dash_table
from components import Header, print_button
from datetime import datetime as dt
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from math import ceil
from about import *
import json
import urllib.request as ur

#for handling dates
format_str =  "%m/%d/%Y"

def date_format(dt_str):
    pydt = dt_str.split('/')
    pydt[-1] = "20"+pydt[-1]
    dt_str = "/".join(pydt)
    dt_str = dt.strptime(dt_str,format_str)
    return dt_str

#JHU Dataset from Github
dataURL_1_c = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
dataURL_1_r = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
dataURL_1_d = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

data_url_india = "https://api.covid19india.org/data.json"
data_url_dist = "https://api.covid19india.org/state_district_wise.json"

response1 = ur.urlopen(data_url_india)
df_india = json.loads(response1.read())
response2 = ur.urlopen(data_url_dist)
df_dist = json.loads(response2.read())

df1 = pd.read_csv(dataURL_1_c, error_bad_lines=False)
df2 = pd.read_csv(dataURL_1_r, error_bad_lines=False)
df3 = pd.read_csv(dataURL_1_d, error_bad_lines=False)
df_states = pd.read_csv("https://raw.githubusercontent.com/kbhartiya/covid19Dataset/master/covid_19_india.csv")
state_list = []

df_test = pd.read_csv("https://raw.githubusercontent.com/kbhartiya/covid19Dataset/master/ICMRTestingDetails.csv")
df_age = pd.read_csv("https://raw.githubusercontent.com/kbhartiya/covid19Dataset/master/AgeGroupDetails.csv")

test_con = df_test.iloc[-1]['TotalSamplesTested']
ind_test = df_test.iloc[-1]['TotalIndividualsTested']

def mapdate(date):
    pydt = date.split('/')
    pydt[-1] = "20"+pydt[-1]
    date = "/".join(pydt)
    date = dt.strptime(date,"%d/%m/%Y")
    return date

#For states
def state_n_cases(df,state_list):
    """
    nowDate = date.today()
    df['Date'] = df['Date'].apply(mapdate)
    #print(df.head(), nowDate) 
    #del
    #df_new = df.groupby('State/UnionTerritory')
    if(nowDate==df.iloc[-1]['Date']):
        df_new = df.groupby('Date').get_group(nowDate)
    else:
        df_new = df.groupby('Date').get_group(df.iloc[-1]['Date'])  
    """  
    
    stateToCasesDict = dict()
    for stat_data in df["statewise"]:
        state = stat_data["state"]
        if(state=="Total"):
            continue
        conf = stat_data['confirmed']
        if(conf=="0"):
            continue
        rec = stat_data['recovered']
        death = stat_data['deaths']
        state_list.append(state)
        stateToCasesDict[state] = [conf, rec, death]

    return stateToCasesDict, state_list


update_test_con_date = "*As on {}".format(df_india["tested"][-1]["updatetimestamp"])

#df1.rename(columns={'Province/State': 'State'}, inplace=True)

#print(df1.columns[4:])
#print(df1[df1.columns[4:]].sum())

######################## START GLOBAL STATS Category Layout ########################
def cssegiSDFormatterG(df):   
    count1 = []
    count2 = []
    count2.append(df.columns[4])
    i=0
    for col in df.columns[4:]:
        count1.append(df[col].sum())
        if(i==0):
            i+=1
            lastcol = col
            continue
        count2.append(df[col].sum()-df[lastcol].sum())
        lastcol = col
        i+=1
    return count1, count2    

count1_c, count2_c = cssegiSDFormatterG(df1)
count1_r, count2_r = cssegiSDFormatterG(df2)
count1_d, count2_d = cssegiSDFormatterG(df3)

#For confirmed cases
gfig_c1 = go.Figure(data=[go.Scatter(x=df1.columns[4:].map(date_format),y=count1_c,name="Confirmed Cases",line=dict(color='lightsalmon'))])
gfig_c1.update_layout(
    title="Confirmed cases",
    autosize=True,
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    ),
    
)

gfig_c2 = go.Figure(data=[go.Bar(x=df1.columns[4:].map(date_format),y=count2_c,name="Daily increase in Confiremed cases",marker_color='lightsalmon')])
gfig_c2.update_layout(
    title="Daily increase in confirmed cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)

#for recovered cases
gfig_r1 = go.Figure(data=[go.Scatter(x=df1.columns[4:].map(date_format),y=count1_r,name="Confirmed Cases",line=dict(color='green'))])
gfig_r1.update_layout(
    title="Recovered cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)


gfig_r2 = go.Figure(data=[go.Bar(x=df1.columns[4:].map(date_format),y=count2_r,name="Confirmed Cases",marker_color='green')])
gfig_r2.update_layout(
    title="Daily increase in recovered cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)

#for death cases
gfig_d1 = go.Figure(data=[go.Scatter(x=df1.columns[4:].map(date_format),y=count1_d,name="Confirmed Cases",line=dict(color='red'))])
gfig_d1.update_layout(
    title="Death cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    ),
    
    
)

gfig_d2 = go.Figure(data=[go.Bar(x=df1.columns[4:].map(date_format),y=count2_d,name="Confirmed Cases",marker_color='red')])
gfig_d2.update_layout(
    title="Daily increase in death cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)

'''
    html.Div([
    dcc.Dropdown(
        id="selector",
        options = [
            {
                'label':i,
                'value':i
            } for i in df1['Country/Region'].iteritems()
        ],
        value='Global',
    )]),
    '''
fatal = "{:.2f}".format((count1_d[-1]/(count1_c[-1]))*100.00)
fatal+="%"

layout_gstats_category = html.Div([
    Header(),
    
    
    #Confir Count Graph.
    
    html.Div([
        html.Div([
            html.H3("Confirmed"),
            html.H4(count1_c[-1],style={'color':'lightsalmon'}),
            html.H6('[+'+str(count1_c[-1]-count1_c[-2])+']',style={'color':'lightsalmon','marginTop':'-30px'}),
        ],className="info"),
        html.Div([
            html.H3("Active"),
            html.H4(count1_c[-1]-count1_r[-1]-count1_d[-1],style={'color':'orange'}),
            html.H6('[+'+str(count1_c[-1]-count1_c[-2]-(count1_r[-1]-count1_r[-2]+count1_d[-1]-count1_d[-2]))+']',style={'color':'orange','marginTop':'-30px'}),
        ],className="info"),

        html.Div([
            html.H3("Recovered"),
            html.H4(count1_r[-1],style={'color':'green'}),
            html.H6('[+'+str(count1_r[-1]-count1_r[-2])+']',style={'color':'green','marginTop':'-30px'}),
        ],className="info"),

        html.Div([
            html.H3("Deaths"),
            html.H4(count1_d[-1],style={'color':'red'}),
            html.H6('[+'+str(count1_d[-1]-count1_d[-2])+']',style={'color':'red','marginTop':'-30px'}),
        ],className="info"),

        html.Div([
            html.H3("Fatality Rate"),
            html.H4(fatal,style={'color':'red'}),
        ],className="info"),

    ],className="flex-container-1"),
    html.Div([        
    dcc.Graph(
        id='graph-1',
        figure=gfig_c1,
    ),
    dcc.Graph(
        id='graph-1',
        figure=gfig_r1,
    ),
    dcc.Graph(
        id='graph-1',
        figure=gfig_d1,
    ),
    
    ],className="flex-container"),
    html.Div([
    dcc.Graph(
        id='graph-1',
        figure=gfig_c2,
    ),
    #Recover Count   
    
    #Recover increase
    dcc.Graph(
        id='graph-1',
        figure=gfig_r2,
    ),
    #death count
    
    #death increase
    dcc.Graph(
        id='graph-1',
        figure=gfig_d2,
    ),

    ],className="flex-container"),
    
    
    #daily increase Confir Graph
    
    ])

######################## END Global STATS Category Layout ########################

######################## START INDIAN STATS Category Layout ######################

def cssegiSDFormatterI(df):   
    count1 = []
    count2 = []
    data = df
    data.set_index("Country/Region", inplace=True)
    data = data.loc['India']
    #print(data[:])
    count2.append(data[3])
    i=0
    for col in data[3:]:
        count1.append(col)
        if(i==0):
            i+=1
            lastcol = col
            continue
        count2.append(col-lastcol)
        lastcol = col
        i+=1
    return count1, count2

count1_ci, count2_ci = cssegiSDFormatterI(df1)
count1_ri, count2_ri = cssegiSDFormatterI(df2)
count1_di, count2_di = cssegiSDFormatterI(df3)

#For confirmed cases
ifig_c1 = go.Figure(data=[go.Scatter(x=df1.columns[4:].map(date_format),y=count1_ci,name="Confirmed Cases",line=dict(color='lightsalmon'))])
ifig_c1.update_layout(
    title="Confirmed cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    ),
    
)

ifig_c2 = go.Figure(data=[go.Bar(x=df1.columns[4:].map(date_format),y=count2_ci,name="Daily increase in Confiremed cases",marker_color='lightsalmon')])
ifig_c2.update_layout(
    title="Daily increase in confirmed cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)

#for recovered cases
ifig_r1 = go.Figure(data=[go.Scatter(x=df1.columns[4:].map(date_format),y=count1_ri,name="Confirmed Cases",line=dict(color='green'))])
ifig_r1.update_layout(
    title="Recovered cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)


ifig_r2 = go.Figure(data=[go.Bar(x=df1.columns[4:].map(date_format),y=count2_ri,name="Confirmed Cases",marker_color='green')])
ifig_r2.update_layout(
    title="Daily increase in recovered cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)

#for death cases
ifig_d1 = go.Figure(data=[go.Scatter(x=df1.columns[4:].map(date_format),y=count1_di,name="Confirmed Cases",line=dict(color='red'))])
ifig_d1.update_layout(
    title="Death cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    ),
    
    
)

ifig_d2 = go.Figure(data=[go.Bar(x=df1.columns[4:].map(date_format),y=count2_di,name="Confirmed Cases",marker_color='red')])
ifig_d2.update_layout(
    title="Daily increase in death cases",
    autosize=True,
    
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)

snc,state_list = state_n_cases(df_india, state_list)
dist_to_conf = dict()
dist_to_state = dict()
for state in state_list:
    dists = df_dist[state]["districtData"]
    for dist in dists:
        #print(dist)
        dist_to_conf[dist] = df_dist[state]["districtData"][dist]["confirmed"]
        dist_to_state[dist] = state

max_dist = max(dist_to_conf,key=dist_to_conf.get)
state_dist_max = dist_to_state[max_dist] 
min_dist = min(dist_to_conf,key=dist_to_conf.get)
state_dist_min = dist_to_state[min_dist]

ifig_states = go.Figure()
ifig_states.add_trace(go.Bar(
    x=[f[1][0] for f in snc.items()],
    y=[f[0] for f in snc.items()],
    name="Confirmed",
    orientation='h',
    marker=dict(
        color='lightsalmon',
    )

))

ifig_states.add_trace(go.Bar(
    x=[f[1][1] for f in snc.items()],
    y=[f[0] for f in snc.items()],
    name="Recovered",
    orientation='h',
    marker=dict(
        color='rgba(0,255,0,0.7)',
    ),
    

))
ifig_states.add_trace(go.Bar(
    x=[f[1][2] for f in snc.items()],
    y=[f[0] for f in snc.items()],
    name="Deaths",
    orientation='h',
    marker=dict(
        color='rgba(255,0,0,0.7)',
    )

))
ifig_states.update_layout(
    title="State wise patients",
    barmode='stack',
    autosize=True,
    height=1000,
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
    ),
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)

age_group = [k[1] for k in df_age['AgeGroup'].iteritems()]
age_n = [f[1] for f in df_age['TotalCases'].iteritems()]
age_percent = [int(p[1].split('.')[0]) for p in df_age['Percentage'].iteritems()]
#print(age_group)
ifig_age = go.Figure()
ifig_age.add_trace(go.Bar(
    x=age_group,
    y=age_n,
    name="patient age group",
    marker={
        'color' : age_percent,
        'colorscale': 'ylorrd',
    }

))

ifig_age.update_layout(
    title="Patients age group",
    autosize=True,
    height=600,
    font=dict(
        family='Quicksand',
        size=18,
        color="#7f7f7f"
    )
)


'''
width=500,
height=600,
'''
'''
    html.Div([
    dcc.Dropdown(
        id="selector",
        options = [
            {
                'label':i,
                'value':i
            } for i in df1['Country/Region'].iteritems()
        ],
        value='Global',
    )]),
    '''
fat = (int(df_india["statewise"][0]["deaths"])*1.00/(int(df_india["statewise"][0]["confirmed"])*1.00))*100.00    
fatali = "{:.2f}".format(fat)
fatali+="%"
activeDelta = int(df_india["key_values"][0]["confirmeddelta"])-int(df_india["key_values"][0]["recovereddelta"])-int(df_india["key_values"][0]["deceaseddelta"])
layout_instats_category = html.Div([
    Header(),
    
    
    #Confir Count Graph.
    
    
    html.Div([
        html.Div([
            html.H3("Confirmed"),
            html.H4(df_india["statewise"][0]["confirmed"],style={'color':'lightsalmon'}),#count1_ci[-1]
            html.H6('[+ '+str(df_india["key_values"][0]["confirmeddelta"])+']',style={'color':'lightsalmon','marginTop':'-30px'}),#'[+'+str(count1_ci[-1]-count1_ci[-2])+']'
        ],className="info"),
        html.Div([
            html.H3("Active"),
            html.H4(df_india["statewise"][0]["active"],style={'color':'orange'}),#count1_ci[-1]-count1_ri[-1]-count1_di[-1]
            html.H6('[+ '+str(activeDelta)+']',style={'color':'orange','marginTop':'-30px'}),
        ],className="info"),

        html.Div([
            html.H3("Recovered"),
            html.H4(df_india["statewise"][0]["recovered"],style={'color':'green'}),
            html.H6('[+ '+str(df_india["key_values"][0]["recovereddelta"])+']',style={'color':'green','marginTop':'-30px'}),
        ],className="info"),

        html.Div([
            html.H3("Deaths"),
            html.H4(df_india["statewise"][0]["deaths"],style={'color':'red'}),
            html.H6('[+ '+str(df_india["key_values"][0]["deceaseddelta"])+']',style={'color':'red','marginTop':'-30px'}),
        ],className="info"),

        html.Div([
            html.H3("Fatality Rate"),
            html.H4(fatali,style={'color':'red'}),
        ],className="info"),

    ],className="flex-container-1"),
    
    html.Div([        
        dcc.Graph(
        id='graph-1',
        figure=ifig_c1,
        ),
        dcc.Graph(
        id='graph-1',
        figure=ifig_r1,
        ),
        dcc.Graph(
        id='graph-1',
        figure=ifig_d1,
        ),
    
    ],className="flex-container"),

    html.Div([
        dcc.Graph(
        id='graph-1',
        figure=ifig_c2,
        ),
    
        dcc.Graph(
        id='graph-1',
        figure=ifig_r2,
        ),
        #death count
    
        #death increase
        dcc.Graph(
        id='graph-1',
        figure=ifig_d2,
        ),

    ],className="flex-container"),
    html.Div([
        dcc.Graph(
            id='graph-2',
            figure=ifig_states,
        ),
    ],className="gr-container"),
    html.Br(),
    html.H4("Highest number of cases are from "+max_dist+", "+state_dist_max+" with "+str(dist_to_conf[max_dist])+" confirmed cases",style={'textAlign':'center'}),
    html.H4("Lowest number of cases are from "+min_dist+", "+state_dist_min+" with "+str(dist_to_conf[min_dist])+" confirmed cases",style={'textAlign':'center'}),
    html.Div([
        html.Div([
           html.H3("Test Conducted*"),
           html.H4(df_india["tested"][-1]["totalsamplestested"],style={'color':'orange'}), 
        ],className="info-1"),
        html.Div([
            html.H3("Individuals Tested*"),
            html.H4(df_india["tested"][-1]["totalindividualstested"],style={'color':'blue'}), 
        ],className="info-1"),
        
    ],className="flex-container"),
    html.Div([
        dcc.Graph(
            id='graph-2',
            figure=ifig_age,
        ),

    ],className="gr-container"),
    
    html.Br(),

    html.H5(update_test_con_date,style={'textAlign':'center'}),
    dcc.Link("DATA SOURCE", href="https://api.covid19india.org/",className="datasource"),
    ])   
    #daily increase Confir Graph
    
######################## END INDIAN STATS Category Layout ########################

######################## START REPORT CATEGORY Layout ########################
layout_report_category = html.Div([
    Header(),
    html.Div([ 
    # CC Header
    html.Div([
        html.Div([
            html.Div([
                html.H1("OOPS!"),
            ],className="notFound-404"),
            
            html.H2("404 - Page Not Found"),
            html.P("The page you are looking for might have been removed had its name changed or is temporarily unavailable."),
            dcc.Link("Go To Homepage", href="/about/"),
        ]),
        
    ],className="notFound"),
    ],id="notFound"),
    ],className="page")

######################## END REPORT CATEGORY Layout ########################
noPage = html.Div([ 
    # CC Header
    html.Div([
        html.Div([
            html.Div([
                html.H1("OOPS!"),
            ],className="notFound-404"),
            
            html.H2("404 - Page Not Found"),
            html.P("The page you are looking for might have been removed had its name changed or is temporarily unavailable."),
            dcc.Link("Go To Homepage", href="/instats/"),
        ]),
        
    ],className="notFound"),
    ],id="notFound")