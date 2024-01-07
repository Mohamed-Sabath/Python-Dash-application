#!/usr/bin/env python
# coding: utf-8

# Mohamed Sabath

# In[1]:


import pandas as pd
data = pd.read_csv("SuperStoreOrders.csv")
data.head()


# In[2]:


data.info()


# In[3]:


data.shape


# In[4]:


data.isnull().sum()


# #### Preprocessing

# In[5]:


data['order_date'] = pd.to_datetime(data['order_date'])
data['ship_date'] = pd.to_datetime(data['ship_date'])


# In[6]:


data.info()


# In[7]:


data = data.sort_values('order_date')
data = data.drop(['order_id','product_name', 'year','customer_name','market',
                  'product_id','state','country','region'], axis=1)
data.head()


# In[8]:


data.tail()


# In[9]:


data['sales'] = pd.to_numeric(data['sales'], errors='coerce').astype('Int64')
#errors='coerce': When set to 'coerce', it means that if there are any non-numeric values in the 'sales' column during the
#conversion, those non-numeric values will be replaced with NaN (Not a Number).

data.info() 


# #### Checking the null values of the categorical columns

# In[10]:


uv1 = data['ship_mode'].unique()
uv2 = data['segment'].unique()
uv3 = data['category'].unique()
uv4 = data['sub_category'].unique()
uv5 = data['order_priority'].unique()

print('Unique values of shipping modes - ',uv1)
print("."*110)
print('Unique values of segments - ',uv2)
print("."*110)
print('Unique values of categoties - ',uv3)
print("."*110)
print('Unique values of sub categories - ',uv4)
print("."*110)
print('Unique values of order priorites - ',uv5)
print("."*110)


# In[11]:


#Line graphs

df1 = data[data['ship_mode'] == 'First Class']
df1 = df1.groupby(pd.Grouper(key='ship_date', freq='D')).sum().reset_index()

df11 = data[data['ship_mode'] == 'Second Class']
df11 = df11.groupby(pd.Grouper(key='ship_date', freq='D')).sum().reset_index()

df12 = data[data['ship_mode'] == 'Standard Class']
df12 = df12.groupby(pd.Grouper(key='ship_date', freq='D')).sum().reset_index() 


# In[12]:


df1.head()


# In[13]:


df2 = data.groupby('order_date').agg({'quantity':'sum', 'shipping_cost':'sum', 
                                                'sales':'sum', 'profit':'sum'})
# #order_date': This column will contain the unique dates from the 'order_date' column.
# 'quantity': The sum of the 'quantity' column for each unique 'order_date'.
# 'shipping_cost': The sum of the 'shipping_cost' column for each unique 'order_date'.
# 'sales': The sum of the 'sales' column for each unique 'order_date'.
# 'profit': The sum of the 'profit' column for each unique 'order_date'.
df2.head()


# In[14]:


df2.corr()


# In[15]:


#Datasets for the 3rd tab

sub_sales = data.groupby('sub_category')['sales'].sum().reset_index()
sub_sales


# In[16]:


data3 = data.groupby(['category', 'order_priority'])[['quantity', 
                                                   'sales']].sum().reset_index()
#group your data by two columns, 'category' and 'order_priority', and then aggregating the 'quantity' and 'sales' columns by
#taking their sums within each group.

#This means it will give you the total quantity and total sales sum for each unique combination of 'category' and 'order_priority'
data3


# In[17]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from datetime import datetime as dt

app = dash.Dash()

app.title = "Final_assignment"


#Creating the app layout
app.layout = html.Div([
    html.H1('ANALYSISNG SUPER-STORE DATA', style={'borderwidth':'2px', 'borderStyle':'solid','border-width': '2px','border-radius': '5%','borderColor':'#B243D6','text-align': 'center','backgroundColor':'#938F95'}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Line Chart For Shipping Cost Over The Period', value='tab-1', style = {
               'borderwidth':'2px', 'borderStyle':'solid','border-width': '2px','border-radius': '5%','borderColor':'#B243D6',
               'textAlign': 'Center', 'backgroundColor':'#9905C0', 'color':'#FFFFFF'}),
        dcc.Tab(label='Scatter Plot for the Daily Total Quantity for Sales, Shipping Cost and Profit ', value='tab-2', style = {'borderwidth':'2px', 'borderStyle':'solid','border-width': '2px','border-radius': '5%','borderColor':'#1E2763',
               'textAlign': 'Center', 'backgroundColor':'#1E2763  ', 'color':'#F2EEF5'}),
        dcc.Tab(label='Bar Plot and Box Plot', value='tab-3', style = {'borderwidth':'2px', 'borderStyle':'solid','border-width': '2px','border-radius': '5%','borderColor':'#21672C',
               'textAlign': 'Center', 'backgroundColor':'#21672C', 'color':'#F2EEF5'}),
        dcc.Tab(label='Bar Chart', value='tab-4', style = {'borderwidth':'2px', 'borderStyle':'solid','border-width': '2px','border-radius': '5%','borderColor':'#691C7E',
               'textAlign': 'Center', 'backgroundColor':'#8F123F', 'color':'#F2EEF5'})]),
    html.Div(id='tab-content'), html.H5('Created by M.M.M Sabath - [007]', style={'text-align': 'center'})])


#callbacks
@app.callback(
    dash.dependencies.Output('tab-content', 'children'),
    [dash.dependencies.Input('tabs', 'value')]
)
def render_content(requirement):
    if requirement == 'tab-1':
        return html.Div([ html.P("This is a Line chart which shows the Total shipping cost over the period. Additionaly the users can also filter the results with the Shipping Class and Date from 2011-01-01 to 2014-12-30 using the Dropdown option and The Date Picker.", 
                                 style={'font-weight': 'normal','fontSize':'17px', 'margin-left': '5px','margin-top': '25px'}),
            dcc.Dropdown(
                id='dp1',
                options=[
                    {'label': 'First Class', 'value': 'op1'},
                    {'label': 'Second Class', 'value': 'op2'},
                    {'label': 'Standard Class', 'value': 'op3'}
                ],
                value='op1', style={'margin-right': '1150px','margin-left': '5px', 'margin-top': '15px', 
                                        'border-radius': '5%'}
            ),
            dcc.DatePickerRange(
                id='date-range-picker',
                min_date_allowed= '2011-01-01',
                max_date_allowed= '2014-12-30',
                start_date= '2011-01-03',
                end_date='2011-12-31', 
                style={'margin-top': '15px','margin-left': '5px'}
            ),
            html.Div(id='graph-container01'),
        ])
    
    
    elif requirement == 'tab-2':
        return html.Div([ html.P("This is a Scatter plot which shows the Daily Total Sales with the combination of Daily total Quantity.", 
                                 style={'font-weight': 'normal','fontSize':'17px', 'margin-left': '5px','margin-top': '25px'}),
            dcc.RadioItems(
                id='rp1',
                options=[
                    {'label': 'Sales', 'value': 'op4'},
                    {'label': 'Shipping cost', 'value': 'op5'},
                    {'label': 'Profit', 'value': 'op6'}
                ],
                value='op4', style={'margin': '10px', 'margin-top': '25px'},
                labelStyle={'display': 'block'}
            ),
                       
            html.Div(id='graph-container02'),
        ])
    
    
    elif requirement == 'tab-3':
        fig = px.bar(
            sub_sales,
            x='sub_category',
            y='sales',
            color_discrete_sequence=['#339933']
        )
        fig.update_layout(
            title="Total Profit distribution for the Year 2011 to 2014",
            xaxis_title="Sub Category",
            yaxis_title="Total Sales",
            title_x=0.5
        )

        return html.Div([
            html.Div([
                dcc.Graph(id="bar-chart", figure=fig),
            ], style={'width': '50%','display': 'inline-block', 'margin-top': '25px'}),  # Set width and display to inline-block for side-by-side layout
            html.Div([
                dcc.Graph(id="box-plot")
            ], style={'width': '50%','display': 'inline-block', 'margin-top': '25px'})  # Set width and display to inline-block for side-by-side layout
        ])

        
    elif requirement == 'tab-4':
        return html.Div([
            html.P("Select category", style={'font-weight': 'normal', 'fontSize': '17px', 'margin-left': '5px', 'margin-top': '25px'}),
            dcc.RadioItems(
                id='x-axis-radio',
                options=[{'label': category, 'value': category} for category in data['category'].unique()],
                value=data['category'].unique()[0],  # Set default value
                labelStyle={'display': 'block'} #Block-level elements typically start on a new line and take up the full width available to them.
            ),
            html.P("Select Y-Axis", style={'font-weight': 'normal', 'fontSize': '17px', 'margin-left': '5px', 'margin-top': '25px'}),
            dcc.RadioItems(
                id='y-axis-radio',
                options=[
                    {'label': 'Quantity', 'value': 'quantity'}, #Here it will show i there like 'Quantity'. The 2nd parameter "quantity" is the actual variable name.
                    {'label': 'Sales', 'value': 'sales'}
                ],
                value='quantity',  # Set default value
                labelStyle={'display': 'block'}
            ),
            dcc.Graph(id='bar-chart')
        ])




#Tab 1
@app.callback(Output('graph-container01', 'children'), [Input('dp1', 'value'), 
                                                      Input('date-range-picker', 'start_date'), 
                                                      Input('date-range-picker', 'end_date')])

def update_graph(selected_tab1, start_date, end_date):
    if selected_tab1 == 'op1':
        data = df1
        title = 'Total Shipping cost by First Class'
    elif selected_tab1 == 'op2':
        data = df11
        title = 'Total Shipping cost by Second Class'
    else:
        data = df12
        title = 'Total Shipping cost by Standard Class'

    # Filter data based on date range
    filtered_data_by_shipping_date = data[(data['ship_date'] >= start_date) & (data['ship_date'] <= end_date)]

    line_chart_tab1 = go.Figure(data=go.Scatter(x=filtered_data_by_shipping_date['ship_date'], 
                                                y=filtered_data_by_shipping_date['shipping_cost'],
                                           mode='lines', line=dict(color='#a149d3')))
    line_chart_tab1.update_layout(
        title=title,
        xaxis=dict(title='Date'),
        yaxis=dict(title='Shipping cost'),
        title_font_size= 15
    )

    return dcc.Graph(figure=line_chart_tab1)


#Tab 2
@app.callback(Output('graph-container02', 'children'), [Input('rp1', 'value')])
def update_graph2(selected_tab2):
    if selected_tab2 == 'op4':
        data = df2
        title = 'Total daily sales over Quantity [Correlation = 0.946566]'
        x_axis_data = data['quantity']
        y_axis_data = data['sales']
        y_lable2 = 'Daily Average Sales'
    elif selected_tab2 == 'op5':
        data = df2
        title = 'Total daily shipping cost over Quantity [Correlation = 0.874253]'
        x_axis_data = data['quantity']
        y_axis_data = data['shipping_cost']
        y_lable2 = 'Daily Total Shipping Cost'
    else:
        data = df2
        title = 'Total daily profits over Quantity [Correlation = 0.523746]'
        x_axis_data = data['quantity']
        y_axis_data = data['profit']
        y_lable2 = 'Daily Total Profit'
        
    scatter_chart_tab2 = go.Figure(data=go.Scatter(x=x_axis_data, y=y_axis_data, mode='markers', marker=dict(color='#241D5D ')))
    scatter_chart_tab2.update_layout(
        title=title,
        xaxis=dict(title='Daily Total Quantity'),
        yaxis=dict(title=y_lable2),
        title_font_size= 15
    )

    return dcc.Graph(figure=scatter_chart_tab2)


#Tab 3
@app.callback(Output("box-plot", "figure"),
              Input("bar-chart", "clickData"))
def update_box_plots(click_data):
    if click_data is not None:
        selected_sub_category = click_data['points'][0]['x']
    else:
        selected_sub_category = 'Accessories'  # Default
    filtered_data = data[data['sub_category'] == selected_sub_category]
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=filtered_data['quantity'],
        name='quantity',
        marker=dict(color='#339933')
    ))
    fig.update_layout(
        title=f"Distribution of sold quantity by sub category: {selected_sub_category}",
        xaxis_title="Sub category",
        yaxis_title="Quantity",
        title_x=0.5
    )
    return fig


# Tab 4
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('x-axis-radio', 'value'),
     Input('y-axis-radio', 'value')]
)
def update_bar_chart(selected_category, selected_y_axis):
    filtered_data = data3[data3['category'] == selected_category]
    
    custom_colors = {
    'Critical': '#ff1a75',
    'High': '#99003d',
    'Low': '#4d001f',
    'Medium': '#ff4d94'
}
    
    fig = px.bar(
        filtered_data,
        x='order_priority',
        y=selected_y_axis,
        color='order_priority',
        color_discrete_map= custom_colors,  # Apply custom colors
        labels={'order_priority': 'Order Priority', selected_y_axis: selected_y_axis},
        title=f'{selected_category} - {selected_y_axis}',
    )
    fig.update_layout(barmode='stack')
    fig.update_traces(showlegend=False)
    return fig




if __name__ == '__main__':
    app.run_server(port=8060)



# In[ ]:




