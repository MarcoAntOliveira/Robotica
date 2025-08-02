import numpy as np
import matplotlib.pyplot as plt

def fk_multi(theta_list, length_list):
    x, y = 0, 0
    positions = [(x, y)]
    total_angle = 0
    for theta, L in zip(theta_list, length_list):
        total_angle += theta
        x += L * np.cos(total_angle)
        y += L * np.sin(total_angle)
        positions.append((x, y))
    return positions  # retorna todas as posições das juntas

def plot_braco_multi(theta_list, length_list):
    joints = fk_multi(theta_list, length_list)
    xs, ys = zip(*joints)
    plt.plot(xs, ys, 'o-', lw=4)
    plt.xlim(-sum(length_list)-0.5, sum(length_list)+0.5)
    plt.ylim(-sum(length_list)-0.5, sum(length_list)+0.5)
    plt.gca().set_aspect('equal')
    plt.grid(True)
    plt.title("Braço Robótico com Vários Elos")
    plt.show()

# Teste com 3 juntas
theta_list = [np.pi/4, np.pi/4, -np.pi/6]  # ângulos em radianos
length_list = [1.0, 0.8, 0.6]              # comprimentos dos elos

plot_braco_multi(theta_list, length_list)
