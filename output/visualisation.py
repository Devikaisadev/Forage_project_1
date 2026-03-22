import os
import datetime
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load CSV using absolute path so both app and pytest can find it
df = pd.read_csv(r'C:\Users\ASUS\Desktop\quantium-starter-repo\output\output.csv')

# Parse and sort dates
df['date'] = pd.to_datetime(df['date'])

# Price increase date fix for Plotly bug
price_increase_date = datetime.datetime(2021, 1, 15).timestamp() * 1000

def create_figure(dataframe):
    fig = px.line(
        dataframe,
        x='date',
        y='sales',
        labels={'date': 'Date', 'sales': 'Total Sales ($)'}
    )
    fig.add_vline(
        x=price_increase_date,
        line_dash='dash',
        line_color='#FF4B4B',
        annotation_text='Price Increase (Jan 15, 2021)',
        annotation_position='top right'
    )
    fig.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family='Segoe UI, Arial', size=13, color='#333333'),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        margin=dict(l=60, r=40, t=40, b=60),
        hovermode='x unified'
    )
    fig.update_traces(
        line=dict(color='#6C63FF', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(108, 99, 255, 0.08)'
    )
    return fig

# Initial figure
df_grouped = df.groupby('date', as_index=False)['sales'].sum().sort_values('date')

# Build app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={'minHeight': '100vh', 'backgroundColor': '#f4f6fb', 'fontFamily': 'Segoe UI, Arial, sans-serif'},
    children=[

        # Navbar
        html.Div(
            style={
                'backgroundColor': '#6C63FF', 'padding': '18px 40px',
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.15)'
            },
            children=[
                html.Div([
                    html.Span('🍬', style={'fontSize': '26px', 'marginRight': '10px'}),
                    html.Span('Soul Foods Analytics', style={'color': 'white', 'fontSize': '22px', 'fontWeight': '700'})
                ], style={'display': 'flex', 'alignItems': 'center'}),
                html.Span('Pink Morsel Sales Dashboard', style={'color': 'rgba(255,255,255,0.75)', 'fontSize': '14px'})
            ]
        ),

        # Main Content
        html.Div(
            style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '40px 24px'},
            children=[

                # Header — id used by tests
                html.H1(
                    'Pink Morsel Sales Over Time',
                    id='header',
                    style={'color': '#1a1a2e', 'fontSize': '30px', 'fontWeight': '700', 'margin': '0 0 8px 0'}
                ),
                html.P(
                    'Were sales higher before or after the Pink Morsel price increase on 15 January 2021?',
                    style={'color': '#666', 'fontSize': '15px', 'margin': '0 0 32px 0'}
                ),

                # Stat Cards
                html.Div(
                    style={'display': 'flex', 'gap': '20px', 'marginBottom': '32px', 'flexWrap': 'wrap'},
                    children=[
                        html.Div(
                            style={
                                'backgroundColor': 'white', 'borderRadius': '12px', 'padding': '24px 28px',
                                'flex': '1', 'minWidth': '200px', 'boxShadow': '0 2px 12px rgba(0,0,0,0.07)',
                                'borderLeft': '4px solid #6C63FF'
                            },
                            children=[
                                html.P('Total Records', style={'color': '#888', 'fontSize': '13px', 'margin': '0 0 6px 0'}),
                                html.H2(f"{len(df_grouped):,}", style={'color': '#1a1a2e', 'fontSize': '28px', 'fontWeight': '700', 'margin': '0'}),
                                html.P('daily data points', style={'color': '#aaa', 'fontSize': '12px', 'margin': '4px 0 0 0'})
                            ]
                        ),
                        html.Div(
                            style={
                                'backgroundColor': 'white', 'borderRadius': '12px', 'padding': '24px 28px',
                                'flex': '1', 'minWidth': '200px', 'boxShadow': '0 2px 12px rgba(0,0,0,0.07)',
                                'borderLeft': '4px solid #43c59e'
                            },
                            children=[
                                html.P('Peak Sales Day', style={'color': '#888', 'fontSize': '13px', 'margin': '0 0 6px 0'}),
                                html.H2(f"${df_grouped['sales'].max():,.0f}", style={'color': '#1a1a2e', 'fontSize': '28px', 'fontWeight': '700', 'margin': '0'}),
                                html.P('highest single day', style={'color': '#aaa', 'fontSize': '12px', 'margin': '4px 0 0 0'})
                            ]
                        ),
                        html.Div(
                            style={
                                'backgroundColor': 'white', 'borderRadius': '12px', 'padding': '24px 28px',
                                'flex': '1', 'minWidth': '200px', 'boxShadow': '0 2px 12px rgba(0,0,0,0.07)',
                                'borderLeft': '4px solid #FF4B4B'
                            },
                            children=[
                                html.P('Price Increase Date', style={'color': '#888', 'fontSize': '13px', 'margin': '0 0 6px 0'}),
                                html.H2('Jan 15, 2021', style={'color': '#1a1a2e', 'fontSize': '24px', 'fontWeight': '700', 'margin': '0'}),
                                html.P('marked on chart in red', style={'color': '#aaa', 'fontSize': '12px', 'margin': '4px 0 0 0'})
                            ]
                        ),
                    ]
                ),

                # Region Picker — id used by tests
                html.Div(
                    style={
                        'backgroundColor': 'white', 'borderRadius': '12px',
                        'padding': '20px 28px', 'marginBottom': '24px',
                        'boxShadow': '0 2px 12px rgba(0,0,0,0.07)'
                    },
                    children=[
                        html.Label('Filter by Region:', style={'fontWeight': '600', 'color': '#333', 'marginBottom': '10px', 'display': 'block'}),
                        dcc.Dropdown(
                            id='region-picker',
                            options=[{'label': 'All Regions', 'value': 'all'}] +
                                    [{'label': r.capitalize(), 'value': r} for r in df['region'].unique()],
                            value='all',
                            clearable=False,
                            style={'maxWidth': '300px'}
                        )
                    ]
                ),

                # Chart Card — id used by tests
                html.Div(
                    style={
                        'backgroundColor': 'white', 'borderRadius': '16px',
                        'padding': '28px', 'boxShadow': '0 2px 16px rgba(0,0,0,0.08)'
                    },
                    children=[
                        html.H3('Daily Total Sales — All Regions', style={'color': '#333', 'fontSize': '17px', 'fontWeight': '600', 'margin': '0 0 4px 0'}),
                        html.P('The red dashed line marks the Pink Morsel price increase on 15 Jan 2021', style={'color': '#999', 'fontSize': '13px', 'margin': '0 0 20px 0'}),
                        dcc.Graph(
                            id='sales-line-chart',
                            figure=create_figure(df_grouped),
                            config={'displayModeBar': False}
                        )
                    ]
                ),

                # Footer
                html.Div(
                    style={'textAlign': 'center', 'marginTop': '40px', 'color': '#bbb', 'fontSize': '13px'},
                    children=[html.P('Soul Foods Internal Analytics Dashboard · Built with Dash & Plotly')]
                )
            ]
        )
    ]
)

# Callback for region picker
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-picker', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered = df.groupby('date', as_index=False)['sales'].sum()
    else:
        filtered = df[df['region'] == selected_region].groupby('date', as_index=False)['sales'].sum()
    filtered = filtered.sort_values('date')
    return create_figure(filtered)


if __name__ == '__main__':
    app.run(debug=True)