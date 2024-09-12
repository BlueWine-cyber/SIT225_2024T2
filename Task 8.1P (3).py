import sys
import csv
import traceback
import time
from arduino_iot_cloud import ArduinoCloudClient
import threading
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# Setup Python to Arduino Cloud
DEVICE_ID = "6352d501-6754-4c7b-bd21-c09204cd5536"
SECRET_KEY = "Z?1rcUObjGZJXXq!MiHQVcTGU"

# Create buffers
BUFFER_SIZE = 100
x_buffer, y_buffer, z_buffer = [], [], []
timestamps = []

# File to save data
CSV_FILE = "phone_accelerometer.csv"

# # Callback Functions
# Handle X-axis changes
def on_accelerometer_X(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"New X-axis value: {value}")
    buffer_data(timestamp, value, None, None)

# Handle Y-axis changes
def on_accelerometer_Y(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"New Y-axis value: {value}")
    buffer_data(timestamp, None, value, None)

# Handle Z-axis value changes
def on_accelerometer_Z(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"New Z-axis value: {value}")
    buffer_data(timestamp, None, None, value)

def write_headers(filename, headers):
    # Write headers to a CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  
            writer.writerow(headers)


# Store combined data to a CSV file
def store_combined_data(timestamp, x, y, z):
    write_headers(CSV_FILE, ["Timestamp", "X Value", "Y Value", "Z Value"])
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, x, y, z])


# Buffer data and store it to a CSV file
def buffer_data(timestamp, x, y, z):
    global x_buffer, y_buffer, z_buffer, timestamps
    
    # Adds the value to the buffer
    x_buffer.append(x)
    y_buffer.append(y)
    z_buffer.append(z)
    
    timestamps.append(timestamp)

    store_combined_data(timestamp, x, y, z)

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Accelerometer Data Visualization"),
    dcc.Graph(id="accelerometer-graph"),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)  
])

@app.callback(
    Output('accelerometer-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)

def update_graph(n_intervals):

    # Update the graph with new data
    global x_buffer, y_buffer, z_buffer, timestamps

    if len(timestamps) == 0:
        return go.Figure()

    figure = {
        'data': [
            go.Scatter(x=timestamps, y=x_buffer, mode="lines", name="X"),
            go.Scatter(x=timestamps, y=y_buffer, mode="lines", name="Y"),
            go.Scatter(x=timestamps, y=z_buffer, mode="lines", name="Z")
        ],
        'layout': go.Layout(title="Accelerometer Data", xaxis={'title': 'Time'}, yaxis={'title': 'Acceleration'})
    }

    if len(x_buffer) >= BUFFER_SIZE:
        x_buffer.clear()
        y_buffer.clear()
        z_buffer.clear()
        timestamps.clear()

    return figure

def run_dash_server():
    # Starts Dash server
    app.run_server(debug=False, port=8050)


def main():
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    client.register("accelerometer_X", value=None, on_write=on_accelerometer_X)
    client.register("accelerometer_Y", value=None, on_write=on_accelerometer_Y)
    client.register("accelerometer_Z", value=None, on_write=on_accelerometer_Z)

    print("Connected to Arduino cloud")

    client.start()

    dash_thread = threading.Thread(target=run_dash_server)
    dash_thread.start()

if __name__ == "__main__":
    try:
        main()  
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=sys.stdout)