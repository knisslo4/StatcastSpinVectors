from flask import Flask, render_template, request
import plotly.graph_objs as go
import json
import plotly

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_graph', methods=['POST'])
def update_graph():
    spin_x = float(request.form['spin_x'])
    spin_y = float(request.form['spin_y'])
    spin_z = float(request.form['spin_z'])
    seam_lat = float(request.form['seam_lat'])
    seam_lon = float(request.form['seam_lon'])

    fig = create_plot(spin_x, spin_y, spin_z, seam_lat, seam_lon)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json

def create_plot(spin_x, spin_y, spin_z, seam_lat, seam_lon):
    # Baseball trajectory (simplified for example purposes)
    trajectory = go.Scatter3d(
        x=[0, spin_x],
        y=[0, spin_y],
        z=[0, spin_z],
        mode='lines+markers',
        marker=dict(size=5, color='blue'),
        line=dict(color='blue', width=2)
    )

    # Strike zone box
    strike_zone = go.Scatter3d(
        x=[-0.85, 0.85, 0.85, -0.85, -0.85, 0.85, 0.85, -0.85],
        y=[-0.73, -0.73, 0.73, 0.73, -0.73, -0.73, 0.73, 0.73],
        z=[1.5, 1.5, 1.5, 1.5, 3.5, 3.5, 3.5, 3.5],
        mode='lines',
        line=dict(color='red', width=5),
        name='Strike Zone'
    )

    layout = go.Layout(
        scene=dict(
            xaxis=dict(range=[-3000, 3000]),
            yaxis=dict(range=[-3000, 3000]),
            zaxis=dict(range=[0, 4000]),
            aspectratio=dict(x=1, y=1, z=1),
            annotations=[
                dict(
                    showarrow=False,
                    x=spin_x,
                    y=spin_y,
                    z=spin_z,
                    text="Baseball",
                    xanchor="left",
                    xshift=10,
                    opacity=0.7
                )
            ]
        ),
        title='3D Baseball Pitch Trajectory'
    )

    fig = go.Figure(data=[trajectory, strike_zone], layout=layout)
    return fig

if __name__ == '__main__':
    app.run(debug=True)