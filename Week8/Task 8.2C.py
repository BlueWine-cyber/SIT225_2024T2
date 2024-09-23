import threading
import asyncio
import nest_asyncio
import dash
import plotly.graph_objs as go
from arduino_iot_cloud import ArduinoCloudClient
from collections import deque
from dash import Dash, dcc, html

nest_asyncio.apply()

# Constants
DEVICE_ID = "6352d501-6754-4c7b-bd21-c09204cd5536"
SECRET_KEY = "Z?1rcUObjGZJXXq!MiHQVcTGU"
BUFFER_SIZE = 30

# Data buffers
x_buffer = deque(maxlen=BUFFER_SIZE)
y_buffer = deque(maxlen=BUFFER_SIZE)
z_buffer = deque(maxlen=BUFFER_SIZE)

def average(data, window_size=5):
    """Calculate the average of the last `window_size` values in `data`"""
    if len(data) < window_size:
        return sum(data) / len(data) if data else 0
    return sum(list(data)[-window_size:]) / window_size

def latest_data():
    """Return the latest averaged values from the data buffers"""
    new_x = average(x_buffer)
    new_y = average(y_buffer)
    new_z = average(z_buffer)

    if new_x is None or new_y is None or new_z is None:
        new_x, new_y, new_z = 0, 0, 0

    return new_x, new_y, new_z

async def connect_to_arduino():
    """Connect to the Arduino IoT Cloud device and register callbacks"""
    try:
        client = ArduinoCloudClient(
            device_id=DEVICE_ID,
            username=DEVICE_ID,
            password=SECRET_KEY
        )

        def on_accelerometer_x_changed(client, value):
            print(f"New X: {value}")
            x_buffer.append(value)

        def on_accelerometer_y_changed(client, value):
            print(f"New Y: {value}")
            y_buffer.append(value)

        def on_accelerometer_z_changed(client, value):
            print(f"New Z: {value}")
            z_buffer.append(value)

        client.register("accelerometer_X", value=0.0, on_write=on_accelerometer_x_changed)
        client.register("accelerometer_Y", value=0.0, on_write=on_accelerometer_y_changed)
        client.register("accelerometer_Z", value=0.0, on_write=on_accelerometer_z_changed)

        await client.start()
        print("Arduino IoT Cloud client started successfully.")
    except Exception as error:
        print(f"Error setting up Arduino IoT Cloud: {error}")

def live_update_plotly_dash(data_source, interval=100):
    """Create a Plotly Dash app that updates with the latest data"""
    app = Dash(__name__)

    x_buffer_local = deque(maxlen=BUFFER_SIZE)
    y_buffer_local = deque(maxlen=BUFFER_SIZE)
    z_buffer_local = deque(maxlen=BUFFER_SIZE)

    app.layout = html.Div([
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
    ])

    @app.callback(dash.dependencies.Output('live-graph', 'figure'),
                  [dash.dependencies.Input('interval-component', 'n_intervals')])
    def update_graph(n):
        new_x, new_y, new_z = data_source()
        print(f"Updating graph with data: X={new_x}, Y={new_y}, Z={new_z}")

        if new_x is not None and new_y is not None and new_z is not None:
            x_buffer_local.append(new_x)
            y_buffer_local.append(new_y)
            z_buffer_local.append(new_z)

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=list(x_buffer_local), mode='lines', name='X-axis'))
        fig.add_trace(go.Scatter(y=list(y_buffer_local), mode='lines', name='Y-axis'))
        fig.add_trace(go.Scatter(y=list(z_buffer_local), mode='lines', name='Z-axis'))

        fig.update_layout(title='Live Accelerometer Data',
                          xaxis_title='Time',
                          yaxis_title='Acceleration',
                          xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False),
                          template='plotly_dark')

        return fig

    try:
        print("Start plotly")
        app.run_server(debug=True, host='127.0.0.1', port=8050)
    except Exception as e:
        print(f"Error starting Plotly Dash server: {e}")

def setup_arduino_cloud():
    """Start the Arduino IoT Cloud connection in a separate thread"""
    arduino_thread = threading.Thread(target=connect_to_arduino)
    arduino_thread.start()

if __name__ == '__main__':
    setup_arduino_cloud()
    live_update_plotly_dash(latest_data)
