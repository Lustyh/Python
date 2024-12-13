import dash
import yaml
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html, Input, Output
from dash.dependencies import Input, Output
from yieldget import get_failItem

configs = yaml.safe_load(open('./yieldget/config.yaml', mode='r').read())

def page1_layout(app):
    data = [project for project in configs['Project']]
    return html.Div([
    html.Div(
        [
        dcc.Dropdown(
            id='project-dropdown',
            options=data,
            placeholder="select Project",
            style = {
                'width': '50%',
                'height': '40px',
                'margin-right': '10px'
            }
        ),
        html.Button('Confirm', 
                    id='ok-button', 
                    n_clicks=0,
                    style={
                        'height': '40px',
                        'marginLeft': '0px',
                    }),
        html.Br(),
        ],
        style={'display': 'flex', 'alignItems': 'flex-start'}
    ),
        html.Div(id='Retest-rate')
    ])

def callbakcs(app):
    @app.callback(
        Output('Retest-rate', 'children'),
        [Input('ok-button', 'n_clicks')],
        [Input('project-dropdown', 'value')
        ]
    )
    def display_table(n_clicks, dropdown_value):
        if n_clicks > 0:
            
            df = px.data.iris()
            fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')
            fig = go.Figure()

            # 添加数据
            fig.add_trace(go.Scatter(
                x=[1, 2, 3, 4],
                y=[10, 20, 30, 40],
                mode='lines+markers+text',
                text=["点1", "点2", "点3", "点4"],
                textposition="bottom right",
                hovertemplate="点名: %{text}<br>X值: %{x}<br>Y值: %{y}",
                name='综合示例'
            ))

            # 设置横纵坐标和图表样式
            fig.update_layout(
                title='Top3 Retest Items',
                xaxis=dict(
                title='自定义 X 轴',  # X 轴标题
                tickvals=[1, 2, 3, 4],  # 自定义范围值
                ticktext=['范围1', '范围2', '范围3', '范围4'],  # 对应的标签
                ),
                yaxis=dict(title='自定义 Y 轴', range=[0, 50]),
                showlegend=True
            )
            return html.Div([
                html.H1(f'{dropdown_value} retest rate'),
                html.P('7 days data'),
                dcc.Graph(figure=fig),
            ])