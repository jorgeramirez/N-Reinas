#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# Importamos el módulo pygtk y le indicamos que use la versión 2
import pygtk
pygtk.require("2.0")

# Luego importamos el módulo de gtk y el gtk.glade, este ultimo que nos sirve
# para poder llamar/utilizar al archivo de glade
import gtk
import gtk.glade

from multiprocessing import Process, Queue
from backtracking import *
from minconflicts import *
from vegas import *
from board import *

# Creamos la clase de la ventana principal del programa
class MainWin:

    def __init__(self):
        # Le decimos a nuestro programa que archivo de glade usar (puede tener
        # un nombre distinto del script). Si no esta en el mismo directorio del
        # script habría que indicarle la ruta completa en donde se encuentra
        self.widgets = gtk.glade.XML("board.glade")
        
        signals = { "on_combobox1_changed" : self.seleccion_algoritmo,
                    "on_button1_clicked" : self.ejecutar,
                    "on_window1_destroy" : self.salir }

        self.widgets.signal_autoconnect(signals)
        combo1 = self.widgets.get_widget("combobox1")
        combo1.set_active(0)
        combo2 = self.widgets.get_widget("combobox2")
        combo2.set_active(0)

        
    def seleccion_algoritmo(self, b):
        combo1 = self.widgets.get_widget("combobox1")
        label4 = self.widgets.get_widget("label4")
        combo2 = self.widgets.get_widget("combobox2")
        if combo1.get_active() == 1:
            label4.set_visible(True)
            combo2.set_visible(True)
        else:
            label4.set_visible(False)
            combo2.set_visible(False)
    def ejecutar(self, b):
        combo1 = self.widgets.get_widget("combobox1")
        combo2 = self.widgets.get_widget("combobox2")
        spin1 = self.widgets.get_widget("spinbutton1")
        n = spin1.get_value()
        n = int(n)
        if combo1.get_active() == 0:
            p1 = Process(target=solve, args=(n,))
            p1.start()
                    
        if combo1.get_active() == 1:
            if combo2.get_active() == 0:
                p1 = Process(target=backtracking, args=(n,True))
            else:
                p1 = Process(target=backtracking, args=(n,False))
            p1.start()
            
        if combo1.get_active() == 2:
            p1 = Process(target=vegas, args=(n,))
            p1.start()
            
            
    def salir(self, b):
        gtk.main_quit()
        
if __name__ == "__main__":
    MainWin()
    gtk.main()

                    
