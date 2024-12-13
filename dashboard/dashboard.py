import dash
from dash import dcc, html, Input, Output
from webPage import Page1, Page2, Page3, devicehistory



# 初始化应用
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    # 页面 URL 路由
    dcc.Location(id='url', refresh=False),  
    
    # 主体区域，使用 flex 布局
    html.Div(
        children=[
            # 左侧导航栏
            html.Img(src="/assets/dashboard.png", 
                 style={
                    'width': '10%',
                    'display': 'inline-block', 
                    'margin': 'auto',
                    'position': 'fixed',
                    'bottom': '0',
                    'left': '0',
                    'zIndex': '1',  # 图片层级低于标题
                    'opacity': '1'  }),
            html.Nav([
                dcc.Link('Home', href='/', className='nav-link', style={'marginBottom': '10px'}),
                dcc.Link('Retest', href='/page-1', className='nav-link', style={'marginBottom': '10px'}),
                dcc.Link('Dashboard-overall', href='/page-2', className='nav-link', style={'marginBottom': '10px'}),
                dcc.Link('Device history', href='/device-history', className='nav-link', style={'marginBottom': '10px'})
            ], 
            style={
                'display': 'flex',
                'flexDirection': 'column',  # 竖直排列导航链接
                'alignItems': 'flex-start',  # 左对齐
                'width': '150px',  # 控制导航栏宽度
                'padding': '20px',
                'backgroundColor': '#f8f9fa',  # 设置背景颜色
                'position': 'fixed',  # 固定在页面左侧
                'height': '100vh'  # 使导航栏占满整个页面的高度
            }),

            # 右侧内容区
            html.Div(
                id='page-content', 
                style={
                    # 'display': 'flex',
                    'marginLeft': '220px',  # 为了避免内容被左侧导航栏遮挡，设置右侧内容区的左边距
                    'flexDirection': 'row',
                    'padding': '20px',
                    'height': '100vh'
                },
                # style={
                #     'display': 'flex',
                #     'flexDirection': 'row',  # 水平排列导航和内容区域
                #     'height': '100vh',  # 页面填充整个视口
                # }
            ),
        ],
    )
])

# 回调函数更新页面内容
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return Page1.homepage_layout()
    elif pathname == '/page-1':
        return Page2.page1_layout(app)
    elif pathname == '/page-2':
        return Page3.page2_layout()
    elif pathname == '/device-history':
        return devicehistory.device_history_layout(app)
    else:
        return html.Div([
            html.H1('404'),
            html.P('Page Not Found')
        ])
Page2.callbakcs(app)
devicehistory.register_callbacks(app)

# # 回调：设备历史页面的搜索框和下拉框
# @app.callback(
#     Output('search-output', 'children'),
#     [Input('confirm-button', 'n_clicks')],
#     [Input('search-box', 'value'),
#      Input('age-dropdown', 'value')]
# )
# def update_search_output(n_clicks, search_value, dropdown_value):
#     if n_clicks > 0:
#         return f"你输入的 SN: {search_value}, 选择的项目: {dropdown_value}"
#     return "请点击搜索按钮并选择项目"

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
