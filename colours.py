import math
import numpy as np
from manim import *

config.background_color = WHITE
FG = BLACK

class ColourAxesRGB(Scene):
    def construct(self):
        r  = Arrow( [-6,0,0], [6,0,0], stroke_width=3, buff=0, color=RED )
        g  = Arrow( [0,-3,0], [0,3,0], stroke_width=3, buff=0, color=GREEN )
        b  = Arrow( [3,2,0], [-4.5,-3,0], stroke_width=3, buff=0, color=BLUE )
        rl = Tex("Red",   color=RED  ).shift([6,-.5,0])
        gl = Tex("Green", color=GREEN).shift([0,3.3,0])
        bl = Tex("Blue",  color=BLUE ).shift([-5,-2.5,0])
        self.play( Create(r), Write(rl) )
        self.play( Create(g), Write(gl) )
        self.play( Create(b), Write(bl) )
        self.wait(10)

def lune(A,B,r, color='white'):
    "Intersection of two disks, of centers A and B, with the same radius r"
    A = np.array(A)
    B = np.array(B)
    d = math.sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 )
    assert d < 2*r, "The circles do not intersect: the distance between the centers should be at most 2*r={2*r}; it is {d}"
    alpha = math.acos(d/2/r)
    beta = math.atan2(B[1]-A[1], B[0]-A[0])
    thetas_A = np.linspace(beta-alpha, beta+alpha, 20)
    thetas_B = np.linspace( PI+beta-alpha, PI+beta+alpha, 20)
    p_A = [ [ A[0] + r*math.cos(u), A[1] + r*math.sin(u), 0 ] for u in thetas_A ]
    p_B = [ [ B[0] + r*math.cos(u), B[1] + r*math.sin(u), 0 ] for u in thetas_B ]

    if False: 
        # Lines -- I want a polygon...
        l_A = [ Line(u,v) for u,v in zip(p_A[:-1],p_A[1:]) ]
        l_B = [ Line(u,v) for u,v in zip(p_B[:-1],p_B[1:]) ]
        l = l_A + l_B
        l = VGroup(*l)

    return Polygon( *(p_A + p_B), fill_opacity=1, color=color)

def center(x0, y0, r, R, color=WHITE):
    "Intersection of the three disks"
    d = 2 * r * math.cos(PI/6)
    assert d < 2*R
    alpha = math.acos(d/2 / R)
    c = ( R * math.cos(7*PI/6-alpha) + r * math.cos(PI/6) ) / R
    s = ( R * math.sin(7*PI/6-alpha) - r*(1+math.sin(PI/6)) ) / R
    print( math.acos(c) )
    print( math.asin(s) )
    print( math.atan2(s,c) )
    #beta = math.acos(c)
    beta = math.asin(c)
    #beta = math.atan2(s,c))
    thetas = np.linspace(-alpha,beta)
    C = [ x0 - r * math.cos(PI/6), y0 + r * math.sin(PI/6), 0 ]
    p = [ [ C[0] + R * math.cos(u), C[1] + R * math.sin(u), 0 ] for u in thetas ]
    theta = 2*PI/3
    p2 = [ [
        x0 + math.cos(theta) * (u-x0) - math.sin(theta) * (v-y0),
        y0 + math.sin(theta) * (u-x0) + math.cos(theta) * (v-y0),
        0
    ] for u,v,_ in p ]
    theta = 4*PI/3
    p3 = [ [
        x0 + math.cos(theta) * (u-x0) - math.sin(theta) * (v-y0),
        y0 + math.sin(theta) * (u-x0) + math.cos(theta) * (v-y0),
        0
    ] for u,v,_ in p ]
    return Polygon( *(p+p2+p3), fill_opacity=1, color=color)

def colour_disk(
    x0 = 0,
    y0 = .5,
    r = 2,
    R = 2.45,
    colours = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF'],
):
    O = [x0,y0,0]
    A = [ x0, y0 - r, 0 ]
    B = [ x0 + r * math.cos(PI/6), y0 + r * math.sin(PI/6), 0 ]
    C = [ x0 - r * math.cos(PI/6), y0 + r * math.sin(PI/6), 0 ]

    CR = Circle(R,fill_opacity=1).shift(A).set_color(colours[0])
    CG = Circle(R,fill_opacity=1).shift(B).set_color(colours[1])
    CB = Circle(R,fill_opacity=1).shift(C).set_color(colours[2])

    RG = lune(A,B,R, colours[3])
    RB = lune(A,C,R, colours[4])
    GB = lune(B,C,R, colours[5])

    return VGroup( CR, CB, CG, RG, RB, GB, center(x0, y0, r, R, colours[6]) )
    
class ColourDisksRGB(Scene):
    def construct(self):
        self.add( colour_disk() )
        self.wait(10)

class ColourDisksCYM(Scene):
    def construct(self):
        self.add( colour_disk( colours=[
            '#FF00FF', # M
            '#FFFF00', # Y
            '#00FFFF', # C
            '#FF0000', # Y+M
            '#0000FF', # C+M
            '#00FF00', # C+Y
            '#000000'            
        ] ) )
        self.wait(10)
        
class ColourDisksPaint(Scene):
    def construct(self):
        self.add( colour_disk( colours=[
            '#FF0000', # Red
            '#FFED00', # Yellow
            '#0047AB', # Blue
            '#FF7700', # Red + Yellow = Orange
            '#802456', # Red + Blue
            '#809A56', # Blue + Yellow
            '#AA6739'            
        ] ) )
        self.wait(10)

YELLOW_COOL = '#ffcc00'  # Cadmium Yellow Primary
YELLOW_WARM = '#ffb400'  # Cadmium Yellow Dark
RED_WARM    = '#be000b'  # Pyrolle Red
RED_COOL    = '#900b25'  # Quinacridone Red
BLUE_WARM   = '#253cac'  # Ultramarine blue (?)
BLUE_COOL   = '#0159a1'  # Phtalo blue, green shade

# Colours from https://trembelingart.com/warm-cool-colors-tell-difference/
BLUE_   = '#0b18ff'
RED_    = '#ff0100'
YELLOW_ = '#fffe00'
GREEN_  = '#02bf3b'
BLUE_COOL   = '#03aaff'
BLUE_WARM   = '#5516ff'
RED_COOL    = '#d40247'
RED_WARM    = '#ff5502'
YELLOW_COOL = '#d4d400'
YELLOW_WARM = '#ffab00'

class ColourTriangle(Scene):
    def construct(self):
        x0 = 0
        y0 = 0
        r = 3
        R = .7
        O = [x0,y0,0]
        
        def f(theta):
            return np.array( [ x0 + r * math.cos(theta), y0 + r * math.sin(theta), 0 ] )
        
        A = f(-PI/2)
        B = f(PI/6)
        C = f(5*PI/6)

        epsilon = PI/10
        AB = f(-PI/2  + epsilon)
        AC = f(-PI/2  - epsilon)
        BA = f(PI/6   - epsilon)
        BC = f(PI/6   + epsilon)
        CA = f(5*PI/6 + epsilon)
        CB = f(5*PI/6 - epsilon)

        G = f(PI/2)
        
        red    = Circle(R, color=RED_,    fill_opacity=1).shift(A)
        yellow = Circle(R, color=YELLOW_, fill_opacity=1).shift(B)
        blue   = Circle(R, color=BLUE_,   fill_opacity=1).shift(C)
        
        red_warm    = Circle(R, color=RED_WARM,    fill_opacity=1).shift(AB)
        red_cool    = Circle(R, color=RED_COOL,    fill_opacity=1).shift(AC)
        yellow_warm = Circle(R, color=YELLOW_WARM, fill_opacity=1).shift(BA)
        yellow_cool = Circle(R, color=YELLOW_COOL, fill_opacity=1).shift(BC)
        blue_warm   = Circle(R, color=BLUE_WARM,   fill_opacity=1).shift(CA)
        blue_cool   = Circle(R, color=BLUE_COOL,   fill_opacity=1).shift(CB)

        green = Circle(R, color=GREEN_, fill_opacity=1).shift(G)

        p = [AB,BA,BC,CB,CA,AC,AB]
        q = [AB,BA,BC,G,CB,CA,AC,AB]
        triangle = VGroup( *[ Line(u,v,color=FG) for u,v in zip([A,B,C],[B,C,A]) ] )
        hexagon  = VGroup( *[ Line(u,v,color=FG) for u,v in zip(p[:-1],p[1:])    ] )
        polygon  = VGroup( *[ Line(u,v,color=FG) for u,v in zip(q[:-1],q[1:])    ] )
        
        self.add(triangle)
        self.add(red)
        self.add(yellow)
        self.add(blue)
        self.wait(1)

        self.play(
            Transform( triangle, hexagon ),
            Transform( red,    VGroup(red_warm,    red_cool  ) ),
            Transform( blue,   VGroup(blue_warm,   blue_cool  ) ),
            Transform( yellow, VGroup(yellow_warm, yellow_cool) ),
        )
        self.wait(1)

        self.play(
            Transform( triangle, polygon ),
            FadeIn( green )
        )
        
        self.wait(10)


