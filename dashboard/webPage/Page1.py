import dash
from dash import dcc, html, Input, Output

def homepage_layout():
    return html.Div(
        [
        # html.Img(src="/assets/dashboard.png", 
        #          style={
        #             'width': '50%',
        #             'display': 'inline-block', 
        #             'margin': 'auto',
        #             'position': 'absolute',
        #             'zIndex': '1',  # 图片层级低于标题
        #             'opacity': '0.35'  }),
        html.Img(src="/assets/Python.png", 
                 style={
                    'width': '10%',
                    'display': 'inline-block', 
                    'margin': 'auto',
                    'position': 'absolute',
                    'top': '0',
                    'left': '190px',
                    'zIndex': '1',  # 图片层级低于标题
                    'opacity': '1'  }),
        html.Img(src="/assets/quanta.png", 
                 style={
                    'width': '15%',
                    'display': 'inline-block', 
                    'margin': 'auto',
                    'position': 'absolute',
                    'top': '0',
                    'right': '0',
                    'zIndex': '1',  # 图片层级低于标题
                    'opacity': '1'  }),
        html.Img(src="/assets/QMB.jpeg", 
                 style={
                    'width': '90%',
                    'display': 'inline-block', 
                    'margin': 'auto',
                    'position': 'absolute',
                    'zIndex': '1',  # 图片层级低于标题
                    'opacity': '0.6'  }),
        html.H1("QMB Software Test", 
                style={
                    'textAlign': 'center',
                    'fontSize': '50px', 
                    'fontWeight': 'bold',
                    'position': 'relative',
                    'zIndex': '2',
                    }),
        html.P("Test DashBoard", style={'textAlign': 'center', 'fontSize': '36px','zIndex': '2'})
        ],
    style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center', 'height': '100vh'}
    )