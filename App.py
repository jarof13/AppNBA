# App.py
import dash
from Layouts import create_layout
from Callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = 'Stats Explorer Summary of the NBA'

# Configurar layout
app.layout = create_layout(app)

# Registrar callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug = False)
