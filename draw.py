# coding:utf-8
import math
import sys
import time

from OpenGL import GLUT, GLU, GL

from SensorStreamer import SensorStreamer
import numpy as np


class draw_posture():
    rotation = 0
    axis = (0, 1, 0)
    ss = SensorStreamer()
    acc_ref = (0, 0, -1)

    def init(width, height):
        """初期化"""
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)  # 隠面消去を有効に
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(
            45.0, float(width) / float(height), 0.1, 100.0)  # 投影変換

    def display():
        # draw process
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL. GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        # 視野変換：カメラの位置と方向のセット
        GLU.gluLookAt(0.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        # draw rotate axis
        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glVertex3f(-axis[0] * 10, -axis[1] * 10, -axis[2] * 10)
        GL.glVertex3f(axis[0] * 10, axis[1] * 10, axis[2] * 10)
        GL.glEnd()
        # draw pot
        GL.glColor3f(1.0, 1.0, 0.0)
        GL.glRotatef(rotation, *axis)
        GLUT.glutWireTeapot(1.5)
        GL.glFlush()  # OpenGLコマンドの強制実行

    def reshape(width, height):
        """画面サイズの変更時に呼び出されるコールバック関数"""
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)

    def idle():
        # idle is invoked when GL isn't doing anything else
        global rotation, axis
        ax, ay, az, gx, gy, gz, mx, my, mz = ss.get_data()
        v1 = [0, -1, 0]
        v2 = [ax, az, ay]
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        theta = math.acos(np.dot(v1, v2) / (n1 * n2))
        axis = list(np.cross(v1, v2))
        rotation = theta * 180 / math.pi
        # of mainLoop
        GLUT.glutPostRedisplay()
        time.sleep(0.0001)

    def main():
        GLUT.glutInit(sys.argv)
        GLUT.glutInitDisplayMode(
            GLUT.GLUT_RGB | GLUT.GLUT_SINGLE | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(300, 300)  # ウィンドウサイズ
        GLUT.glutInitWindowPosition(100, 100)  # ウィンドウ位置
        GLUT.glutCreateWindow("shape")  # ウィンドウを表示
        GLUT.glutDisplayFunc(display)  # 描画コールバック関数を登録
        GLUT.glutReshapeFunc(reshape)  # リサイズコールバック関数の登録
        GLUT.glutIdleFunc(idle)
        init(300, 300)
        GLUT.glutMainLoop()

if __name__ == "__main__":
    main()
