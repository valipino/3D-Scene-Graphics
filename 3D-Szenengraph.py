# Die Funktionen wurden mithilfe von den Bibliotheken von Python, OpenGL geschrieben, außerdem wurde das Wissen
# aus der Vorlesung/Übung angewendet und schlussendlich für einige Hilfestellungen ChatGPT/Phind genutzt


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

SIZE = 400
ANGLE_INCREMENT = 15


class Scene:

    def __init__(self, window):
        self.xAngle = 0
        self.yAngle = 0
        self.zoom = 0
        self.window = window
        self.last_y = 0
        self.right_mouse_down = False
        self.mouse_down = False

    def display(self):
        # Anzeigen der Szene
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [5, 1, 1, 0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(0, 0, -600 + self.zoom)
        glRotatef(self.xAngle, 1, 0, 0)
        glRotatef(self.yAngle, 0, 1, 0)
        self._draw_torus()
        self._draw_cube()
        self._draw_teapot()
        glPopMatrix()
        glutSwapBuffers()

    def reshape(self, w, h):
        # Anpassen der Szene bei Größenänderung des Fensters
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, w / h, 1, 10000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def mouse_button(self, button, state, x, y):
        # Verarbeiten des Mausbuttons
        if button == GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                self.right_mouse_down = True
            elif state == GLUT_UP:
                self.right_mouse_down = False
        elif button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_down = True
            elif state == GLUT_UP:
                self.mouse_down = False

    def mouse_motion(self, x, y):
        # Verarbeiten der Mausbewegung
        if self.mouse_down:
            self.xAngle = y / SIZE * 360
            self.yAngle = x / SIZE * 360
        elif self.right_mouse_down:
            self.zoom += (self.last_y - y) * ANGLE_INCREMENT
        self.last_y = y
        glutPostRedisplay()

    def keyboard(self, key, x, y):
        # Verarbeiten von Tastatureingaben
        if key == b'a':
            self.yAngle -= ANGLE_INCREMENT
        elif key == b'd':
            self.yAngle += ANGLE_INCREMENT
        elif key == b'w':
            self.xAngle -= ANGLE_INCREMENT
        elif key == b's':
            self.xAngle += ANGLE_INCREMENT
        elif key == b'+':
            self.zoom += ANGLE_INCREMENT
        elif key == b'-':
            self.zoom -= ANGLE_INCREMENT
        glutPostRedisplay()

    def special_keys(self, key, x, y):
        # Verarbeiten von speziellen Tastatureingaben (z.B. Pfeiltasten)
        if key == GLUT_KEY_UP:
            glTranslatef(0.0, ANGLE_INCREMENT, 0.0)
        elif key == GLUT_KEY_DOWN:
            glTranslatef(0.0, -ANGLE_INCREMENT, 0.0)
        elif key == GLUT_KEY_LEFT:
            glTranslatef(-ANGLE_INCREMENT, 0.0, 0.0)
        elif key == GLUT_KEY_RIGHT:
            glTranslatef(ANGLE_INCREMENT, 0.0, 0.0)
        glutPostRedisplay()

    def _draw_torus(self):
        # Zeichnen eines Torus
        glPushMatrix()
        glColor3f(1, 0, 0)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 0.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        glTranslatef(-200, 0, 0)
        glutSolidTorus(20, 50, 50, 50)
        glPopMatrix()

    def _draw_cube(self):
        # Zeichnen eines Würfels
        glPushMatrix()
        glColor3f(0, 1, 0)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.0, 1.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        glTranslatef(0, 200, 0)
        glutSolidCube(100)
        glutWireCube(100)
        glPopMatrix()

    def _draw_teapot(self):
        # Zeichnen einer Teekanne
        glPushMatrix()
        glColor3f(0, 0, 1)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.0, 0.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
        glTranslatef(200, 0, 0)
        glScalef(10, 10, 10)
        glutSolidTeapot(10)
        glPopMatrix()


def main():
    # Initialisierung der OpenGL-Bibliothek
    glutInit(sys.argv)
    glutInitWindowSize(SIZE, SIZE)
    window = glutCreateWindow(b"3D Scene (PyOpenGL)")
    glutInitDisplayString(b"double=1 rgb=1 samples=4 depth=16")
    glEnable(GL_DEPTH_TEST)
    # Erzeugung der Szene
    scene = Scene(window)
    # Registrierung von Callback-Funktionen
    glutMotionFunc(scene.mouse_motion)
    glutMouseFunc(scene.mouse_button)
    glutSpecialFunc(scene.special_keys)
    glutDisplayFunc(scene.display)
    glutReshapeFunc(scene.reshape)
    glutKeyboardFunc(scene.keyboard)
    # Haupt-Loop der OpenGL-Anwendung
    glutMainLoop()


if __name__ == "__main__":
    main()
