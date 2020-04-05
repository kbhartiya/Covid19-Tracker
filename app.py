import dash#
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from layouts import layout_gstats_category, layout_instats_category, layout_report_category, noPage
#import callbacks
#
external_stylesheets1 = [
                        "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "//fonts.googleapis.com/css?family=Quicksand",
                        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                    ]
external_stylesheets = [
                        "//fonts.googleapis.com/css?family=Quicksand",
                        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
                        ]

external_scripts = ["https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js",
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
                    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js",
                ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/')#, external_stylesheets=external_stylesheets,external_scripts=external_scripts
server = app.server
app.config.suppress_callback_exceptions = True
#import dash_auth
# Keep this out of source code repository - save in a file or a database
#{%renderer%} after {%scripts%} because of rendering error.
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {%metas%}
        <title>CoV@INDIA</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div class="contact">
            <div class="contact-1">
                <a href="#" class="con-link"><i class="fa fa-github-alt" style="font-size:36px;color:#333"></i></a>
                <a href="#" class="con-link"><i class="fa fa-linkedin" style="font-size:36px;color:#333"></i></a>
            </div>
        </div>       
        <div class="contact" style="text-align:center">
            <div class="contact-2">
                @kbhartiya
            </div>    
        </div>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/instats/':
        return layout_instats_category    
    elif pathname == '/gstats/':
        return layout_gstats_category
    elif pathname == '/report/':
        return layout_report_category    
    else:
        return noPage

if __name__ == '__main__':
    app.run_server(debug=True)
