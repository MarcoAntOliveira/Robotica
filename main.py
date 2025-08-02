import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parâmetros do braço
L1, L2, L3 = 1.0, 1.0, 1.0

# Cinemática direta: calcula posições acumulando ângulos corretamente
def fk(theta1: float, theta2: float, theta3: float = 0):
    x0, y0 = 0, 0
    a1 = theta1
    a2 = theta1 + theta2
    a3 = theta1 + theta2 + theta3  # Inclui orientação final, se desejar

    x1 = x0 + L1 * np.cos(a1)
    y1 = y0 + L1 * np.sin(a1)

    x2 = x1 + L2 * np.cos(a2)
    y2 = y1 + L2 * np.sin(a2)

    x3 = x2 + L3 * np.cos(a3)
    y3 = y2 + L3 * np.sin(a3)

    return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]

# Cinemática inversa para 2 DOF (L3 será apenas visual)
def ik(x, y):
    # Compensar a posição final (remoção de L3)
    r = np.hypot(x, y)
    if r > (L1 + L2 + L3):
        return None, None  # Fora do alcance

    # Reduz a posição desejada para considerar L3
    angle_to_target = np.arctan2(y, x)
    x -= L3 * np.cos(angle_to_target)
    y -= L3 * np.sin(angle_to_target)

    # IK clássica para 2 elos
    r = np.hypot(x, y)
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if abs(cos_theta2) > 1:
        return None, None  # Impossível

    sin_theta2 = np.sqrt(1 - cos_theta2**2)
    theta2 = np.arctan2(sin_theta2, cos_theta2)
    k1 = L1 + L2 * cos_theta2
    k2 = L2 * sin_theta2
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return theta1, theta2

# Trajetória desejada (círculo)
N = 100
t = np.linspace(0, 2*np.pi, N)
traj_x = 1.5 + 0.5 * np.cos(t)
traj_y = 0.5 * np.sin(t)

# Preparar figura
fig, ax = plt.subplots()
line, = ax.plot([], [], 'o-', lw=4)
trace, = ax.plot([], [], 'g--', lw=1)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.grid()

# Rastro
trajecao_real = []

def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

def update(frame):
    x, y = traj_x[frame], traj_y[frame]
    theta1, theta2 = ik(x, y)
    if theta1 is None:
        return line, trace
    joints = fk(theta1, theta2)
    xs, ys = zip(*joints)
    line.set_data(xs, ys)
    trajecao_real.append((xs[-1], ys[-1]))
    tr_x, tr_y = zip(*trajecao_real)
    trace.set_data(tr_x, tr_y)
    return line, trace

# Criar animação
ani = animation.FuncAnimation(fig, update, frames=N, init_func=init,
                              blit=True, interval=50, repeat=True)

plt.title("Simulação do Braço Robótico 3 Elos (2 DOF + Efetuador)")
plt.show()
