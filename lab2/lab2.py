import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import math
from matplotlib.animation import FuncAnimation
import sympy as sp
from matplotlib.patches import Polygon

if __name__ == "__main__":
    t = sp.Symbol('t')

    #границы рисунка
    # fig, ax = plt.subplots()
    fig = plt.figure(figsize=(4, 8))
    ax = fig.add_subplot(1, 2, 1)
    plt.xlim(-4, 8)
    plt.ylim(-2, 6)
    ax.set_aspect(1)

    # Линия нижней поверхности
    bottom_line_x = [-4, 8]
    bottom_line_y = [0, 0]
    plt.plot(bottom_line_x, bottom_line_y, 'k')

    # Прямоугольник
    Rec_x = 0.9 * sp.cos(t) - 0.2 * sp.sin(t)
    body1 = plt.Rectangle((-1, 1.5), width=5, height=2.0, color='c')

    VxRec = sp.diff(Rec_x, t)
    # ax.add_patch(body1)

    # Круги
    Cir_x = 0.9 * sp.cos(t) - 0.2 * sp.sin(t)
    circle1 = plt.Circle((0.0, 0.5), radius=0.5, color="r")

    # ax.add_patch(circle1)
    circle2 = plt.Circle((3, 0.5), radius=0.5, color="r")
    # ax.add_patch(circle2)

    # Треугольники
    triangle_line1, = plt.plot([0, 0.5], [0.5, 1.5] , 'b')
    triangle_line2, = plt.plot([0.5, -0.5], [1.5, 1.5], 'b')
    triangle_line3, = plt.plot([-0.5, 0], [1.5,0.5], 'b')

    triangle_line4, = plt.plot([3, 3.5], [0.5, 1.5], 'b')
    triangle_line5, = plt.plot([3.5, 2.5], [1.5, 1.5], 'b')
    triangle_line6, = plt.plot([2.5, 3], [1.5, 0.5], 'b')

    # Координаты шарнира
    l_x0 = 2.5
    l_y0 = 2.5  # координаты центра окружности
    # alpha = 90*sp.sin(t) * math.pi / 180  # угол
    alpha = 80 * sp.sin(t) * math.pi / 180
    r = 3  # радиус окружности
    l_y = l_y0 - r * sp.cos(alpha)
    l_x = l_x0 + r * sp.sin(alpha) + Rec_x

    VxO = sp.diff(l_x, t)
    VyO = sp.diff(l_y, t)

    # Спираль
    #l_x0, l_u0 - координаты центра спирали
    Xspr = Rec_x + l_x0
    Yspr = l_y0

    # Массивы
    T = np.linspace(0, 20, 1000)

    XSpr = np.zeros_like(T)
    YSpr = np.zeros_like(T)

    ALPHA = np.zeros_like(T)
    OY = np.zeros_like(T)
    OX = np.zeros_like(T)
    REC_X = np.zeros_like(T)

    VXREC = np.zeros_like(T)
    VXO = np.zeros_like(T)
    VYO = np.zeros_like(T)

    for i in np.arange(len(T)):
        XSpr[i] = sp.Subs(Xspr, t, T[i])
        YSpr[i] = sp.Subs(Yspr, t, T[i])

        ALPHA[i] = sp.Subs(alpha, t, T[i])
        REC_X[i] = sp.Subs(Rec_x, t, T[i])
        OY[i] = l_x0 - r * sp.cos(ALPHA[i])
        OX[i] = l_y0 + r * sp.sin(ALPHA[i]) + REC_X[i]
        VXREC[i] = sp.Subs(VxRec, t, T[i])
        VXO[i] = sp.Subs(VxO, t, T[i])
        VYO[i] = sp.Subs(VyO, t, T[i])

    # Шарнир
    line, = plt.plot([1.5, OX[0]], [2.5, OY[0]], 'b')

    # Грузик
    cargo = plt.Circle((OX[0], OY[0]), radius=0.2, color="k")

    def Spring(x0, y0, q):  # return lists for a spring
        SX = [x0 - 0.3 * t * sp.cos(t) / (6 * math.pi) for t in # 0.3 указывает на увеличение/уменьшение диаметра полюса на каждый 1 градус вращения
              np.linspace(0, q + 6.5 * math.pi, 100)]           # от t зависит количество градусов, повернутых спиралью
        SY = [y0 - 0.3 * t * sp.sin(t) / (6 * math.pi) for t in
              np.linspace(0, q + 6.5 * math.pi, 100)]
        return SX, SY

    # Спираль
    SpX, SpY = Spring(XSpr[0], YSpr[0], ALPHA[0])
    Spr, = plt.plot(SpX, SpY, 'black')

    # Графики
    ax2 = fig.add_subplot(4, 2, 2)
    ax2.plot(T, VXREC)
    plt.title('Vx of the Rectangle')
    plt.xlabel('t values')
    plt.ylabel('Vx values')

    ax3 = fig.add_subplot(4, 2, 4)
    ax3.plot(T, VXO)
    plt.title('Vx of the Cargo')
    plt.xlabel('t values')
    plt.ylabel('Vx values')

    ax4 = fig.add_subplot(4, 2, 6)
    ax4.plot(T, VYO)
    plt.title('Vy of the Cargo')
    plt.xlabel('t values')
    plt.ylabel('Vy values')

    plt.subplots_adjust(wspace=0.3, hspace=0.7)

    def init():
        # Прямоугольник
        ax.add_patch(body1)
        # Выколотая окружность
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        # Спираль
        ax.add_patch(Spr)
        # Грузик
        ax.add_patch(cargo)
        # Шарнир
        # ax.add_patch(line)
        return Spr, cargo, body1, circle1, circle2,

    def anima(j):  # Анимация движения
        body1.xy = REC_X[j], 1.5
        circle1.center = REC_X[j] + 1, 0.5
        circle2.center = REC_X[j] + 4, 0.5

        SpX, SpY = Spring(XSpr[j], YSpr[j], ALPHA[j])
        Spr.set_data(SpX, SpY)

        triangle_line1.set_data([REC_X[j] + 1, 1.5 + REC_X[j]], [0.5, 1.5])
        triangle_line2.set_data([REC_X[j] + 1.5, 0.5 + REC_X[j]], [1.5, 1.5])
        triangle_line3.set_data([REC_X[j] + 0.5, 1 + REC_X[j]], [1.5, 0.5])
        triangle_line4.set_data([REC_X[j] + 4, 4.5 + REC_X[j]], [0.5, 1.5])
        triangle_line5.set_data([REC_X[j] + 4.5, 3.5 + REC_X[j]], [1.5, 1.5])
        triangle_line6.set_data([REC_X[j] + 3.5, 4 + REC_X[j]], [1.5, 0.5])

        line.set_data([REC_X[j] + 2.5, OX[j]], [2.5, OY[j]])
        cargo.center = OX[j], OY[j]

        return Spr, line, body1, circle1, circle2, triangle_line1, triangle_line2, triangle_line3, triangle_line4, triangle_line5, triangle_line6, cargo,

    anim = FuncAnimation(fig, anima, init_func=init, frames=1000, interval=0.5, blit=True)
    plt.show()