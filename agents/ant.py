"""
Ant

Learn to control your muscles to make forward progress!

Control Signals

The action space for an ant is continuous control over 16 muscles. For
each of four legs there are four muscles. One leg extensor, one leg flexor,
and two hip muscles which move the leg left and right (or forward and back
depending on your perspective.)

Gym Environment

The `step` method takes an array of 16 values which represent the input to
the fatigable muscle model for each muscle.

PyMuscle Model

The range of valid input values for the muscle model is determined by the
instantiation characteristics of the muscle. You can think of these inputs
as the spikes / second that the motor nuclei for each muscle receive. Each
muscle responds slightly differently and within a muscle each motor unit
will be recruited at a different level of input.

For example if you send an input value of 20 to the muscle model a small number
of weak motor units will be recruited an a small fraction of the total possible
force will be generated by the muscle. If, however, you use an value of 60 then
all or nearly all the motor units will be recruited and the muscle will produce
maximal voluntary output.

Output values are normalized by the maximum voluntary force the muscle can
produce. That value is a function of its instantiation characteristics. Output
values will thus usually be between 0.0 and 1.0.

PyMuscle Fatigue

After use muscles produce less force for the same level of input. So if you
were to send an input signal which recruited all motor units in a muscle
constantly for several seconds the output the model will return will rapidly
decrease. A period of light or no use is required for the muscle to recover.

MuJoCo Model

Each tendon actuator is control limited to the range [-3.0, 0.0]. When a
General actuator is tied to a Tendon in MuJoCo negative values are the
equivalent of contractions. Muscles cannot produce force in extension so no
positive non-zero values are allowed.

The expected input range is [-1.0, 0.0] which is the equivalent of voluntary
force. However real muscles can actually produce 3x voluntary force under
certain circumstances so we reserve that here for future use.

Actuators have a `gainprm` which scales this input value. This is tuned to
a value of 200 to work with the mass of the ant and the resistances of opposing
tendons.


"""
import math
from muscledagents.envs.mujoco import MuscledAntEnv


def main():
    env = MuscledAntEnv(apply_fatigue=True)

    # Set up the simulation parameters
    sim_duration = 60  # seconds
    frames_per_second = 50
    step_size = 1 / frames_per_second
    total_steps = int(sim_duration / step_size)

    action = [0.0] * env.muscle_count
    for i in range(total_steps):
        action[1] = ((math.sin(i / 25) + 1) / 2) * 60
        action[5] = ((math.sin(i / 35) + 1) / 2) * 60
        action[9] = ((math.sin(i / 45) + 1) / 2) * 60
        action[13] = ((math.sin(i / 55) + 1) / 2) * 60
        env.step(action)
        env.render()


if __name__ == '__main__':
    main()
