from flask import Flask, render_template, request
import json
import math


app = Flask(__name__)


def generate_motion_data(phase_radians: float, angular_speed: float, amplitude: float, final_time: float, damping_ratio: float = 0.0, num_samples: int = 600):

    if final_time <= 0:
        final_time = 5.0
    if num_samples < 10:
        num_samples = 10

    dt = final_time / (num_samples - 1)
    times = []
    displacements = []
    velocities = []
    accelerations = []

    # Damping is ignored for this simple nursery-level model
    for i in range(num_samples):
        t = i * dt
        theta = angular_speed * t + phase_radians
        # Nursery-level simple harmonic motion formulas
        x = amplitude * math.sin(theta)
        v = amplitude * angular_speed * math.cos(theta)
        a = - amplitude * (angular_speed ** 2) * math.sin(theta)
        times.append(t)
        displacements.append(x)
        velocities.append(v)
        accelerations.append(a)

    return times, displacements, velocities, accelerations


@app.route('/', methods=['GET', 'POST'])
def index():

    # Defaults designed for a friendly demo
    default_phase = 0.0  # radians
    default_w = 2 * math.pi  # rad/s
    default_amplitude = 1.0  # arbitrary units
    default_tf = 10.0  # seconds

    if request.method == 'POST':
        try:
            phase = float(request.form.get('phi', default_phase))
        except ValueError:
            phase = default_phase
        try:
            w = float(request.form.get('w', default_w))
        except ValueError:
            w = default_w
        try:
            xm = float(request.form.get('xm', default_amplitude))
        except ValueError:
            xm = default_amplitude
        try:
            tf = float(request.form.get('tf', default_tf))
        except ValueError:
            tf = default_tf
    else:
        phase = default_phase
        w = default_w
        xm = default_amplitude
        tf = default_tf
        damping = 0.0

    times, xs, vs, accs = generate_motion_data(phase, w, xm, tf)

    meta = {
        'phase': phase,
        'angular_speed': w,
        'amplitude': xm,
        'final_time': tf,
    }
    data_payload = {
        'times': times,
        'x': xs,
        'v': vs,
        'a': accs,
        'meta': meta,
    }

    return render_template(
        'index.html',
        data_json=json.dumps(data_payload),
        meta=meta
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


