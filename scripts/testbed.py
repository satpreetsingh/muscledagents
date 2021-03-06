from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
import os
import math
from os.path import dirname
import plotly.graph_objs as go
from plotly.offline import plot

from pymuscle.hill_type import (
    contractile_element_force_length_curve as ce_length_curve,
    contractile_element_force_velocity_curve as ce_velocity_curve,
)

model_base_path = os.path.join(
    "..",
    "muscledagents",
    "envs",
    "mujoco",
    "assets",
)
model_path = os.path.join(
    model_base_path,
    "muscled-ant.xml"
)
model = load_model_from_path(model_path)
sim = MjSim(model)
viewer = MjViewer(sim)

t = 0
total_steps = 15000
inc = 5.0 / total_steps
time_step = 0.002
forces = []
sensor_forces = []
lengths = []
act_forces = []
initial_stiffness = None
total_forces = []
prev_length = None
for i in range(1, total_steps + 1):
    sim.step()

    if i == 1:
        print("Rest Length", sim.model.tendon_lengthspring)
        print(len(sim.data.ctrl))
        # sim.model.tendon_lengthspring[0] = sim.model.tendon_lengthspring[0] * 0.65

    if i > 400:
        sim.data.ctrl[1] = math.cos(i/100) - 1

    # import pdb
    # pdb.set_trace()
    if not initial_stiffness:
        initial_stiffness = sim.model.tendon_stiffness[0]

    # sim.model.tendon_stiffness[0] = sim.model.tendon_stiffness[0] + 10.0
    # sim.model.body_mass[2] = sim.model.body_mass[2] + 0.1
    # print("Lengths", sim.data.ten_length)
    # cur_length = sim.data.ten_length[0]
    # # print("Rest Length", sim.model.tendon_lengthspring)
    # rest_length = sim.model.tendon_lengthspring[0]
    # # print("Stiffness", sim.model.tendon_stiffness)
    # cur_stiffness = sim.model.tendon_stiffness[0]
    # tension = 0
    # # Hooke's Law
    # if cur_length > rest_length:
    #     delta = cur_length - rest_length
    #     frac = cur_length / rest_length
    #     tension = delta * cur_stiffness
    #     sim.model.tendon_stiffness[0] = initial_stiffness * frac



    # print("Tension", tension)

    # print("Sensor 1", sim.data.sensordata[:3])
    # print("Sensor 1 mag", sensor_force)
    # print("Sensor 2", sim.data.sensordata[3:])
    # print("Sensor 2 mag", np.linalg.norm(sim.data.sensordata[3:]))

    # sim.data.ctrl[0] = sim.data.ctrl[0] - 0.001
    # if i > 6000:
    #     sim.data.ctrl[0] = 0.0

    # if i > 3000:
    #     length_factor = ce_length_curve(rest_length, cur_length)

    #     if not prev_length:
    #         prev_length = cur_length
    #     velocity_factor = ce_velocity_curve(
    #         rest_length,
    #         cur_length,
    #         prev_length,
    #         time_step
    #     )

    #     sim.data.ctrl[0] = -(length_factor * velocity_factor)

    #     forces.append(tension)
    #     norm_length = cur_length / rest_length
    #     lengths.append(norm_length)
    #     act_force = np.abs(sim.data.actuator_force[0])
    #     act_forces.append(act_force)
    #     sensor_force = np.linalg.norm(sim.data.sensordata[:3])
    #     sensor_forces.append(sensor_force)
    #     total_force = act_force + tension
    #     total_forces.append(total_force)

    #     prev_length = cur_length

    # if 6000 < i < 9000:
    #     sim.model.body_mass[2] = sim.model.body_mass[2] + 0.1

    # if i > 9000:
    #     if sim.model.body_mass[2] > 1:
    #         sim.model.body_mass[2] = sim.model.body_mass[2] - 0.1

    # print(sim.data.ctrl[0])
    # left_val = (math.sin(i / 400) * 2.5) - 2.5
    # sim.data.ctrl[0] = left_val
    # print(sim.data.qfrc_passive)
    # right_val = (math.sin(math.pi + i / 1000) * 2.5) - 2.5
    # sim.data.ctrl[1] = right_val
    viewer.render()

# fig = go.Figure(
#     data=[
#         go.Scatter(
#             y=forces
#         ),
#         go.Scatter(
#             y=sensor_forces
#         )
#     ],
#     layout=go.Layout(
#         title='Calculated tension over time'
#     )
# )
# plot(fig, filename='total-force-by-excitation.html')

# fig = go.Figure(
#     data=[
#         go.Scatter(
#             y=lengths
#         )
#     ],
#     layout=go.Layout(
#         title='Tendon Length by Time'
#     )
# )
# plot(fig, filename='length-by-time.html')

fig = go.Figure(
    data=[
        go.Scatter(
            y=forces,
            x=lengths
        ),
        go.Scatter(
            y=act_forces,
            x=lengths
        ),
        go.Scatter(
            y=total_forces,
            x=lengths
        ),
    ],
    layout=go.Layout(
        title='Tension by Length',
        xaxis=dict(
            range=[0.0, 1.8]
        )
    )
)
plot(fig, filename='tension-by-length.html')
