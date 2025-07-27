
#let doc-title = [= Cinemática Direta e Inversa de Braços Robóticos com Python]
#set page(width: 21cm, height: 29.7cm)  // A4
#set heading(numbering: "1.")

#doc-title

Neste documento, explicamos como funcionam braços robóticos, como obter a cinemática direta e inversa, e como validar essas equações usando Python, incluindo animações com Matplotlib.

== 1. Funcionamento de Braços Robóticos

Braços robóticos são sistemas articulados que simulam o movimento do braço humano. Eles são compostos por elos, juntas, atuadores e sensores. O movimento é gerado por motores e controlado por sistemas eletrônicos.

*Partes principais:*

- **Segmentos (elos):** partes rígidas que conectam as juntas.
- **Juntas:** permitem movimento (rotacionais ou prismáticas).
- **Atuadores:** motores elétricos, hidráulicos ou pneumáticos.
- **Sensores:** medem posição, velocidade, força etc.
- **Controlador:** interpreta comandos e controla o movimento.
- **Efetuador final:** ferramenta na extremidade do braço (pinça, garra, etc).

== 2. Cinemática Direta

Cinemática direta determina a posição do efetuador final com base nos ângulos das juntas e nos comprimentos dos elos.

Usamos os parâmetros de Denavit-Hartenberg para representar os movimentos:

- θ: ângulo da junta
- d: deslocamento ao longo de z
- a: comprimento ao longo de x
- α: rotação entre eixos z

Para braços simples, a posição pode ser calculada com trigonometria. Exemplo para um braço planar de 2 DOF:

```python
def cinematica_direta(theta1, theta2, L1, L2):
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return x, y

```
== 3. Cinemática Inversa

Cinemática inversa é o processo inverso: encontrar os ângulos das juntas para atingir uma posição desejada.

Para 2 DOF em 2D:
```py
def ik_2d(x, y, L1, L2):
    r = np.hypot(x, y)
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    sin_theta2 = np.sqrt(1 - cos_theta2**2)
    theta2 = np.arctan2(sin_theta2, cos_theta2)
    k1 = L1 + L2 * cos_theta2
    k2 = L2 * sin_theta2
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    return theta1, theta2
```


== 4. Validação com Python

Para validar, aplicamos a IK para obter os ângulos e, em seguida, usamos FK para calcular a posição novamente.
```py
# Parâmetros
L1, L2 = 1.0, 1.0
x_d, y_d = 1.0, 0.5
theta1, theta2 = ik_2d(x_d, y_d, L1, L2)
x_calc, y_calc = cinematica_direta(theta1, theta2, L1, L2)

Comparando x_calc, y_calc com x_d, y_d, o erro deve ser próximo de zero.
```


== 5. Animação com Matplotlib

Com matplotlib.animation, é possível simular o movimento do braço:

import matplotlib.animation as animation
...
```py
def update(frame):
    x, y = traj_x[frame], traj_y[frame]
    theta1, theta2 = ik(x, y)
    joints = fk(theta1, theta2)
    xs, ys = zip(*joints)
    line.set_data(xs, ys)
```

    ...

Essa animação mostra o braço seguindo uma trajetória circular, validando dinamicamente a cinemática inversa.

== 6. Conclusão

A cinemática direta e inversa são fundamentais no controle de braços robóticos. Com Python, podemos calcular, validar e simular esses movimentos de forma precisa e visual.


---



