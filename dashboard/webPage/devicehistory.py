import dash
import yaml
from datetime import datetime
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from yieldget import captureYield

# app = dash.Dash(__name__)
# test = ''

configs = yaml.safe_load(open('./yieldget/config.yaml', mode='r').read())

def device_history_layout(app):
    data = [project for project in configs['Project']]
    return html.Div([
    # 自动完成的下拉框
    html.Div(
        [
            html.Img(src="/assets/yield_report.png", 
                 style={
                    'width': '10vw',
                    'height': 'auto',
                    'display': 'inline-block', 
                    'margin': 'auto',
                    'position': 'absolute',
                    'right': '0',
                    'zIndex': '1',  # 图片层级低于标题
                    'opacity': '0.99'  }),
            dcc.Input(
            id='search-box', 
            type='text', 
            placeholder='Input SN...', 
            debounce=True,
            style={
                'width': "70%",
                'height': '40px',
                'margin-right': '10px'
            }),
            html.Button('Search', 
                        id='confirm-button', 
                        n_clicks=0,
                        style={
                            'height': '40px',
                            
                        }),
            html.Br(),
        ]
    ),

    dcc.Dropdown(
    id='project-dropdown',
    options=data,
    placeholder="select Project",
    style={'width': '40%', 'height': '40px', 'margin': '10px 0'}
                ),
                
    html.Div(id='markdown-output')
    # html.Div(id='search-output', style={'padding': '20px',})

    ])


def register_callbacks(app):
    @app.callback(
        Output('markdown-output', 'children'),
        [Input('confirm-button', 'n_clicks')],
        [Input('search-box', 'value'),
         Input('project-dropdown', 'value')]
    )
    def display_table(n_clicks, search_value, dropdown_value):
        if n_clicks > 0:
            results = captureYield.search_by_keyword(search_value, f"./yieldget/{dropdown_value}.db")
            results = sorted(results, key=lambda x: int(x.split('_')[-1].split('.')[0][0:14]))
            value_list = []
            index = 0
            for result in results:
                index += 1
                # result = result.replace('\\\\', '//').replace('\\','/')
                result_list = result.split('\\')
                print(result_list)
                value_list.append(
                    [
                        index, 
                        datetime.strptime(result_list[-1].split('_')[-1].split('.')[0], '%Y%m%d%H%M%S'), #Test time
                        search_value, 
                        dropdown_value,
                        'Debug' if result_list[9] == 'Offline' else 'Production', 
                        result_list[10], #Station ID
                        result,  #Link
                        result_list[-2] #Result
                    ]
                )
            dicts = []
            keys = ['index', 'time', 'name', 'project', 'test_mode', 'station_id', 'test_record', 'test_result']
            for values  in value_list:
                new_dict = dict(zip(keys, values))
                dicts.append(new_dict)
            return dash_table.DataTable(
                columns=[
                    {"name": "Index", "id": "index"},
                    {"name": "Time", "id": "time"},
                    {"name": "Name", "id": "name"}, 
                    {"name": "Project", "id": "project"},
                    {"name": "Test Mode", "id": "test_mode"},
                    {"name": "Station ID","id": "station_id"},
                    {"name": "Test Record", "id":"test_record", "presentation": "markdown"},
                    {"name": "Test Result", "id":"test_result"}],
                data=dicts,
                style_table={
                    'margin': '40px auto', 
                    'width': '70%',
                    'padding': '10px',
                    'position': 'absolute',
                    'textAlign': 'left',
                    },
                style_cell={
                    'textAlign': 'left',  # 设置所有单元格文本居左对齐
                    'padding': '5px',  # 设置内边距
                    'border': '1px solid #ddd',  # 设置单元格边框
                    'fontSize': '18px'
                },
                style_header={
                    'textAlign': 'center',  # 表头文字居中
                    'fontWeight': 'bold',  # 加粗
                    'backgroundColor': '#f0f0f0',  # 表头背景颜色
                    'fontSize': '25px'
                },
                style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{test_result} = "PASS"',  # 条件
                        'column_id': 'index'  # 选择特定列
                    },
                    'backgroundColor': 'green',  # 设置背景颜色
                },
                {
                    'if': {
                            'filter_query': '{test_result} != "PASS"',  # 条件
                            'column_id': 'test_record'  # 选择特定列
                        },
                        'backgroundColor': 'red',  # 设置背景颜色
                },
                {
                    'if': {
                            'filter_query': '{test_mode} != "Production"',  # 条件
                            'column_id': 'test_mode'  # 选择特定列
                        },
                        'backgroundColor': 'lightyellow',  # 设置背景颜色
                },
                {
                    'if': {
                            'filter_query': '{test_mode} = "Production"',  # 条件
                            'column_id': 'test_mode'  # 选择特定列
                        },
                        'backgroundColor': 'lightblue',  # 设置背景颜色
                }
                ]
            )
            # return dcc.Markdown(table)

    return dcc.Markdown("Please click 'Search' after entering a name.")
# def register_callbacks(app):
#     @app.callback(
#         Output('search-output', 'children'),
#         [Input('confirm-button', 'n_clicks')],
#         [Input('search-box', 'value'),
#          Input('age-dropdown', 'value')]
#     )
#     def update_search_output(n_clicks, search_value, dropdown_value):
#         if n_clicks > 0:
#             return f"你输入的 SN: {search_value}, 选择的项目: {dropdown_value}"
#         return "请点击搜索按钮并选择项目"