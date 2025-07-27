import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parâmetros do braço
L1, L2 = 1.0, 1.0

# Cinemática direta
def fk(theta1, theta2):
    x0, y0 = 0, 0
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)
    return [(x0, y0), (x1, y1), (x2, y2)]

# Cinemática inversa
def ik(x, y):
    r = np.hypot(x, y)
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if abs(cos_theta2) > 1:
        return None, None  # Ponto fora do alcance
    sin_theta2 = np.sqrt(1 - cos_theta2**2)
    theta2 = np.arctan2(sin_theta2, cos_theta2)
    k1 = L1 + L2 * cos_theta2
    k2 = L2 * sin_theta2
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    return theta1, theta2

# Trajetória desejada (círculo)
N = 100
t = np.linspace(0, 2*np.pi, N)
traj_x = 1.0 + 0.5 * np.cos(t)
traj_y = 0.5 * np.sin(t)

# Preparar figura
fig, ax = plt.subplots()
line, = ax.plot([], [], 'o-', lw=4)
trace, = ax.plot([], [], 'g--', lw=1)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid()

# Armazena os pontos visitados para formar o rastro
trajecao_real = []

# Função de inicialização
def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

# Função de atualização da animação
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

plt.title("Simulação do Braço Robótico 2D")
plt.show()
