import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import datetime

# Load your output CSV
df = pd.read_csv('output.csv')

# Parse date and sort by date
df['date'] = pd.to_datetime(df['date'])

# Group by date — sum sales across all regions per day
df_grouped = df.groupby('date', as_index=False)['sales'].sum()
df_grouped = df_grouped.sort_values('date')

# Create the line chart
fig = px.line(
    df_grouped,
    x='date',
    y='sales',
    labels={
        'date': 'Date',
        'sales': 'Total Sales ($)'
    }
)

# Fix for Plotly bug — use timestamp instead of string date
price_increase_date = datetime.datetime(2021, 1, 15).timestamp() * 1000

fig.add_vline(
    x=price_increase_date,
    line_dash='dash',
    line_color='red',
    annotation_text='Price Increase (Jan 15, 2021)',
    annotation_position='top right'
)

fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')

# Build the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={'fontFamily': 'Arial', 'maxWidth': '1100px', 'margin': 'auto', 'padding': '20px'},
    children=[
        html.H1(
            'Soul Foods — Pink Morsel Sales Visualiser',
            style={'textAlign': 'center', 'color': '#333'}
        ),
        html.P(
            'Were sales higher before or after the Pink Morsel price increase on 15 January 2021?',
            style={'textAlign': 'center', 'color': '#666'}
        ),
        dcc.Graph(
            id='sales-line-chart',
            figure=fig
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)