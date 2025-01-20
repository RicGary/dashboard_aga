from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import base64
import datetime
import io

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])


def parse_csv(contents):
    _, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    return df    
    

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents')
        )
def update_output(list_of_contents):
    # if list_of_contents is not None:
    #     children = [parse_csv(c) for c in list_of_contents]

    df = None
    for c in list_of_contents:
        df = parse_csv(c)
        
    print(df)

    return html.Span("poi")

if __name__ == '__main__':
    app.run(debug=True)
