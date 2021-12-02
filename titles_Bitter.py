import math
import numpy as np
import scipy
import networkx as nx
from manim import *
import manimpango

config.background_color = BLACK

class Title0(Scene):
    def construct(self):
        assert manimpango.register_font('/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf' ), f"Cannot register font {font}"
        t = Text(r"Manifolds", font='Bitter', weight=BOLD ).scale(3.5)
        self.play( Write(t) )
        self.wait(10)

class Title1(Scene):
    def construct(self):
        assert manimpango.register_font('/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf' ), f"Cannot register font {font}"
        t = Text(r"Colours", font='Bitter', weight=BOLD ).scale(3.5)
        self.play( Write(t) )
        self.wait(10)

class Title2(Scene):
    def construct(self):
        assert manimpango.register_font('/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf' ), f"Cannot register font {font}"
        t1 = Text("Trees",  font='Bitter', weight=BOLD ).scale(3.5)
        t2 = Text("and",    font='Bitter', weight=BOLD ).scale(3.5)
        t3 = Text("Graphs", font='Bitter', weight=BOLD ).scale(3.5)
        t1.next_to(t2,UP)
        t3.next_to(t2,DOWN)
        self.play( Write(t1), Write(t2), Write(t3) )
        self.wait(10)

class Title3(Scene):
    def construct(self):
        assert manimpango.register_font('/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf' ), f"Cannot register font {font}"
        t1 = Text(r"Statistical", font='Bitter', weight=BOLD ).scale(3.5)
        t2 = Text(r"Manifolds",   font='Bitter', weight=BOLD ).scale(3.5)
        t1.move_to( 1.5 * UP )
        t2.move_to( 1.5 * DOWN )
        self.play( Write(t1), Write(t2) )
        self.wait(10)

class TitleN(Scene):
    def construct(self):
        assert manimpango.register_font('/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf' ), f"Cannot register font {font}"
        t = Text(r"Conclusion", font='Bitter', weight=BOLD ).scale(3.5)
        self.play( Write(t) )
        self.wait(10)

class TitleRef(Scene):
    def construct(self):
        assert manimpango.register_font('/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf' ), f"Cannot register font {font}"
        t = Text(r"References", font='Bitter', weight=BOLD ).scale(3.5)
        self.play( Write(t) )
        self.wait(10)

class TitleDef(Scene):
    def construct(self):
        assert manimpango.register_font('/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf' ), f"Cannot register font {font}"
        t = Text(r"Definitions", font='Bitter', weight=BOLD ).scale(3.5)
        self.play( Write(t) )
        self.wait(10)
        
