import numpy as np
import pandas as pd
import matplotlib
import glob
import plotly.express as px
from os import listdir
#Create dash application
import dash
from dash import Dash, dcc, html, Input, Output, State

class Cancer():
    #Store dataframes:
    def __init__(self, application = None):
        self.Africa = pd.read_pickle("cancer/data/Africa.pkl", compression="gzip")
        self.Asia = pd.read_pickle("cancer/data/Asia.pkl", compression="gzip")
        self.Europe = pd.read_pickle("cancer/data/Europe.pkl", compression="gzip")
        self.North_america = pd.read_pickle("cancer/data/North_america.pkl", compression="gzip")
        self.South_america = pd.read_pickle("cancer/data/South_america.pkl", compression="gzip")
        self.Oceania = pd.read_pickle("cancer/data/Oceania.pkl", compression="gzip")
        self.World = pd.read_pickle("cancer/data/World.pkl", compression="gzip")
        
        self.continent = ['Asia', 'Europe', 'Africa', 'Oceania', 
                                 'North-america', 'South-america']
        self.cancers = sorted(['Lip','Tongue','Mouth','Salivary glands','Tonsil','Oropharynx','Nasopharynx','Pyriform sinus','Hypopharynx','Oesophagus','Stomach','Small intestine','Colon','Rectosigmoid junction','Rectum','Anus','Liver','Gallbladder','Pancreas','Ill-defined digestive organs','Nasal cavity and middle ear','Accessory sinuses','Larynx','Trachea','Lung','Thymus','Heart, mediastinum and pleura','Bone','Skin','Mesothelioma','Kaposi sarcoma','Peripheral nerves', 'Peritoneum and retroperitoneum','Connective and soft tissue','Breast','Vulva','Vagina','Cervix uteri','Corpus uteri','Ovary','Other female genital organs','Placenta','Penis','Prostate','Other male genital organs','Kidney','Renal pelvis','Ureter','Bladder','Other urinary organs','Eye','Meninges', 'Central nervous system','Brain','Other parts of central nervous system','Thyroid','Adrenal gland','Other endoctrine','Non-Hodgkin lymphoma','Hodgkin disease',  'Immunoproliferative diseases','Multiple myeloma','Lymphoid leukaemia','Myeloid leukaemia','Leukaemia and unspecified','Myeloproliferative disorders','Myelodysplastic syndromes'])
        self.age_group=[
                        '0-4',
                        '5-9',
                        '10-14',
                        '15-19',
                        '20-24',
                        '25-29',
                        '30-34',
                        '35-39',
                        '40-44',
                        '45-49',
                        '50-54',
                        '55-59',
                        '60-64',
                        '65-69',
                        '70-74',
                        '75-79',
                        '80-84',
                        '85+',
                        'Unknown']
        #Insérer la valeur du main layout représentant la page html elle même.
        #self.main_layout = None
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            #self.app.layout = self.main_layout

        app = Dash(__name__)
        self.df =px.data.tips()
        self.df1 = px.data.tips()
        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des Cancers entre les pays'),
            html.Div([dcc.Graph(id='cancer-main-graph'), 
                      dcc.Checklist(
                            id='continent-id',
                            options=[{'label': i, 'value': i} for i in sorted(self.continent)],
                            value=['Asia','Europe','North-america'],
                            labelStyle={'display':'block'},
                            style={'display': 'inline-block'}),
                    dcc.Dropdown(
                            id='cancer-dropdown-id',
                            options=[{'label': i, 'value': i} for i in (self.cancers)],
                            value=['Lung','Breast','Brain','Stomach','Liver'],
                            multi=True,
                            style={'width':'40%','verticalAlign':'middle'}
            )], style={'width':'100%', })
            ,
            html.Div([
                    dcc.Graph(id='cancer-by-sex',
                            style={'width':'100%', 'display':'inline-block'}),
                    dcc.RangeSlider(
                            id='cancer-by-age-slider',
                            min=0,
                            max=18,
                            step=1,
                            marks={0:'0-4',1:'5-9',2:'10-14',3:'15-19',4:'20-24',5:'25-29',6:'30-34',7:'35-39',8:'40-44',9:'45-49',10:'50-54',11:'55-59',12:'60-64',13:'65-69',14:'70 -74',15:'75-79',16:'80-84',17:'85+',18:'Unknown'},
                            value=[4,7])],
                style={'display':'block', 'width':"100%"}),
            html.Div([
                dcc.Graph(id='cancer-by-age', 
                          style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id='cancer-by-country',
                          style={'width':'50%', 'display':'inline-block', 'padding-left': '0.5%'}),
            ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            html.Div(dcc.RadioItems(id='sex-radioitem', 
                                     options=[{'label':'Male', 'value':'Male'},
                                              {'label':'Female', 'value':'Female'}, 
                                              ],
                                    value='Female',
                                    style={'display':'block'})),
            html.Br()])
        

        self.app.callback(dash.dependencies.Output('cancer-main-graph','figure'),
                          dash.dependencies.Input('continent-id', 'value'),
                          dash.dependencies.Input('cancer-dropdown-id','value'),
                          )(self.update_main_graph)
        
        self.app.callback(dash.dependencies.Output('cancer-by-sex','figure'),
                          dash.dependencies.Input('continent-id', 'value'),
                          dash.dependencies.Input('cancer-dropdown-id','value'),
                          dash.dependencies.Input('cancer-by-age-slider','value')
                          )(self.update_graph_age)
        
        self.app.callback(dash.dependencies.Output('cancer-by-age','figure'),
                          dash.dependencies.Input('continent-id', 'value'),
                          dash.dependencies.Input('cancer-dropdown-id','value'),
                          dash.dependencies.Input('sex-radioitem','value'),
                          )(self.update_graph_sex)
        
        self.app.callback(dash.dependencies.Output('cancer-by-country','figure'),
                          dash.dependencies.Input('continent-id', 'value'),
                          dash.dependencies.Input('cancer-dropdown-id','value'),
                          )(self.update_graph_country)
        
#         self.app.callback(dash.dependencies.Output('cancer-by-country-selected-continent','figure'),
#                           dash.dependencies.Input('continent-id', 'value'),
#                           dash.dependencies.Input('cancer-dropdown-id','value'),
#                           dash.dependencies.Input('marginal-option-id','value'),
#                           )(self.update_graph)
        
    def update_main_graph(self,continent_id,column_x):
        sub_df= self.World[self.World['Continent'].isin(continent_id)]
        sub_df = sub_df[sub_df['Type of Cancer'].isin(column_x)]
        fig = px.histogram(self.df, x=sub_df['Type of Cancer'],y=sub_df['Number of cases'],labels={'x':'Type of Cancer', 'y':'Number of cases'},color=sub_df['Continent'],text_auto=True)
        fig.update_layout(xaxis_title="Type of Cancer", yaxis_title="Number of cases")
        return fig
    
    def update_graph_age(self,continent_id,column_x,selected_age_group):
        selected_age_group_l = [self.age_group[i] for i in range(selected_age_group[0], selected_age_group[1])]
        sub_df= self.World[self.World['Continent'].isin(continent_id)]
        sub_df = sub_df[sub_df['Type of Cancer'].isin(column_x)]
        sub_df = sub_df[sub_df['Age group'].isin(selected_age_group_l)]
        fig = px.histogram(self.df1, x=sub_df['Type of Cancer'],y=sub_df['Number of cases'],labels={'x':'Type of Cancer', 'y':'Number of cases'},color=sub_df['Age group'],text_auto=True)
        fig.update_layout(xaxis_title="Type of Cancer", yaxis_title="Number of cases")
        return fig
    
    def update_graph_sex(self,continent_id,column_x,selected_sex):
        sub_df= self.World[self.World['Continent'].isin(continent_id)]
        sub_df = sub_df[sub_df['Type of Cancer'].isin(column_x)]
        sub_df = sub_df[sub_df['Sex'] == selected_sex]
        fig = px.histogram(self.df1, x=sub_df['Type of Cancer'],y=sub_df['Number of cases'],labels={'x':'Type of Cancer', 'y':'Number of cases'},text_auto=True)
        fig.update_layout(xaxis_title="Type of Cancer", yaxis_title="Number of cases")
        return fig
    
    def update_graph_country(self,continent_id,column_x):
        sub_df= self.World[self.World['Continent'].isin(continent_id)]
        sub_df = sub_df[sub_df['Type of Cancer'].isin(column_x)]
        fig = px.histogram(self.df1, x=sub_df['Country'],y=sub_df['Number of cases'],labels={'x':'Country', 'y':'Number of cases'},color=sub_df['Type of Cancer'],text_auto=True)
        fig.update_layout(xaxis_title="Country", yaxis_title="Number of cases")
        return fig
    # def update_graph(self, current_df, column_x, column_y, marginal_option):
    #     df = px.data.tips()
    #     if marginal_option == 'violin' or marginal_option == 'rug' or marginal_option == 'box':
    #         fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y],labels={'x':column_x, 'y':column_y,'color':column_color},marginal=marginal_option,text_auto=True)
    #     else:
    #         fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y], color=current_df[column_color],labels={'x':column_x, 'y':column_y,'color':column_color},text_auto=True)
    #     return fig


if __name__ == '__main__':
    cncr = Cancer()
    cncr.app.run_server(debug=True,port=8051)