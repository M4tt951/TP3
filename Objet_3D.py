#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
from Outils import create_program_from_file
import pyrr
from ctypes import *

rot3 = pyrr.matrix33.create_from_z_rotation(np.pi/2)
rot4 = pyrr.matrix44.create_from_matrix33(rot3)                  

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()    
        self.color = (1, 0, 0)
        self.Position = [0, 0, -5]
        self.theta = 0
        self.projection = 0


    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)   #permet de repérer la profondeur et d'avoir un effet 3D

    def init_programs(self):
        id = create_program_from_file("phong.vert", "phong.frag")    #Renvoie l'id du GPU   #bien se mettre sur le dossier /TP3 !
        GL.glUseProgram(id)
        
    def init_data(self):
        sommets = np.array(((0, 0, 0),(0, 0, 1),
                        (1, 0, 0), (-0.5774,-0.5774,-0.5774),
                        (0, 1, 0),(-0.5774,-0.5774,-0.5774),
                        (0, 0, 1) ,(-0.5,-0.5,0.707)), np.float32)
        index=np.array(((0, 1, 2), (1, 3, 2)), np.uint32)

        # attribution d'une liste d'´ etat (1 indique la cr´ eation d'une seule liste)
        vao = GL.glGenVertexArrays(1)
        # affectation de la liste d'´ etat courante
        GL.glBindVertexArray(vao)
        # attribution d’un buffer de données (1 indique la cr´ eation d’un seul buffer)
        vbo = GL.glGenBuffers(1)
        # affectation du buffer courant
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)

        # copie des donnees des sommets sur la carte graphique
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)

        # Les deux commandes suivantes sont stockées dans l'´ etat du vao courant


        # Active l'utilisation des donn´ ees de positions
        # (le 0 correspond ` a la location dans le vertex shader)
        GL.glEnableVertexAttribArray(0)    #positions
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 2*3*sizeof(c_float()), None)

        # Indique comment le buffer courant (dernier vbo "bind´ e")
        # est utilis´ e pour les positions des sommets
        sizefloat = sizeof(c_float())
        GL.glEnableVertexAttribArray(1)   #normales
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 2*3*sizeof(c_float()), c_void_p(3*sizefloat))

        # attribution d’un autre buffer de donnees
        vboi = GL.glGenBuffers(1)
        # affectation du buffer courant (buffer d’indice)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,vboi)
        # copie des indices sur la carte graphique
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,index,GL.GL_STATIC_DRAW)

    def run(self):

        prj1 = pyrr.matrix44.create_perspective_projection(50, 1, 0.5, 10.0, dtype=None)
        prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
        loc3 = GL.glGetUniformLocation(prog, "projection")
        if loc3 ==-1 :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc3, 1, GL.GL_FALSE, prj1)

        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # choix de la couleur de fond
            GL.glClearColor(1, 0.7, 0.1, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.Position[1] += 0.01
            if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.Position[1] -= 0.01
            if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.Position[0] += 0.01
            if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
                self.Position[0] -= 0.01
            
            if glfw.get_key(self.window, glfw.KEY_P) == glfw.PRESS:
                self.Position[2] += 0.1
            if glfw.get_key(self.window, glfw.KEY_M) == glfw.PRESS:
                self.Position[2] -= 0.1

            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
            loc1 = GL.glGetUniformLocation(prog, "translation")
            if loc1 ==-1 :
                print("Pas de variable uniforme : translation")
            GL.glUniform4f(loc1, self.Position[0], self.Position[1], self.Position[2], 0)


            if glfw.get_key(self.window, glfw.KEY_I) == glfw.PRESS:
                self.theta += 0.1
            if glfw.get_key(self.window, glfw.KEY_J) == glfw.PRESS:
                self.theta -= 0.1
            rot3 = pyrr.matrix33.create_from_x_rotation(self.theta)
            rot4 = pyrr.matrix44.create_from_matrix33(rot3)
            
            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
            loc2 = GL.glGetUniformLocation(prog, "rotation")
            if loc2 ==-1 :
                print("Pas de variable uniforme : rotation")
            GL.glUniformMatrix4fv(loc2, 1, GL.GL_FALSE, rot4)


            # Modifie la variable pour le programme courant
            GL.glDrawElements(GL.GL_TRIANGLES, 2*3, GL.GL_UNSIGNED_INT, None)
            self.sendcolor()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
            

    def key_callback(self, win, key, scancode, action, mods):
            # sortie du programme si appui sur la touche 'echap'
            if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
                glfw.set_window_should_close(win, glfw.TRUE)
            if key == glfw.KEY_R and action == glfw.PRESS :
                self.color = (0, 1, 0)

            self.sendcolor()



    def sendcolor(self):
            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
            loc = GL.glGetUniformLocation(prog, "color1")
            if loc ==-1 :
                print("Pas de variable uniforme : color1")
            GL.glUniform4f(loc, self.color[0], self.color[1], self.color[2], 0)
            
                

def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()
