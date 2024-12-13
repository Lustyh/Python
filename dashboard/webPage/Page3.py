import dash
import plotly.express as px
import plotly.graph_objs as go
# from yieldget import captureYield
from dash import dcc, html, Input, Output


def page2_layout():
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
        title='综合图表示例',
        xaxis=dict(
        title='自定义 X 轴',  # X 轴标题
        tickvals=[1, 2, 3, 4],  # 自定义范围值
        ticktext=['范围1', '范围2', '范围3', '范围4'],  # 对应的标签
        ),
        yaxis=dict(title='自定义 Y 轴', range=[0, 50]),
        showlegend=True
    )
    return html.Div([
        html.H1('页面 2'),
        html.P('这是第二个页面。'),
        dcc.Graph(figure=fig),
    ])