import math
import numpy as np
import scipy
import networkx as nx
from manim import *

config.background_color = WHITE
#config.frame_width=4   # Enlarges everything, including the stroke width. Default: 128/9≈14.222

FG = BLACK

class Tree(Scene):
    def f(self, position = [0,0,0], direction = 0, span = 2*PI, degree=3, length=1):
        step = 2/degree
        start = -1 + step/2
        angles = [ start + k*step for k in range(degree) ]
        angles = [ span * a for a in angles ]
        angles = [ direction + a for a in angles ] 
        xs = [ position[0] + length * math.cos(angle) for angle in angles ]
        ys = [ position[1] + length * math.sin(angle) for angle in angles ]
        points = [ [x,y,0] for x,y in zip(xs,ys) ]
        lines = [ Line(position,p).set_stroke(FG) for p in points ]
        return lines

    def g(self, lines, span, degree, length): 
        new_lines = []
        for l in lines:
            position = l.end
            x1,y1,_ = l.start
            x2,y2,_ = l.end
            direction = math.atan2( y2-y1, x2-x1 )
            print( direction )
            new_lines += self.f(position, direction, span, degree, length)
        return new_lines

    def h(self, lines):
        self.play( Create( VGroup(*lines) ) )
        #for line in lines:
        #    self.add(line)
    
    def construct(self):
        lines = self.f(degree=5,length=.8)
        self.h(lines)
        self.wait(1)

        lines = self.g( lines, span = 2*PI / 7, degree=4, length=.8 )
        self.h(lines)
        self.wait(1)

        lines = self.g( lines, span = 2*PI / 12, degree=4, length=.6 )
        self.h(lines)
        self.wait(1)

        lines = self.g( lines, span = 2*PI / 15, degree=4, length=.3 )
        self.h(lines)
        self.wait(10)
        
class Circles(Scene):
    def construct(self):
        def f(R=1, n=5, offset=0):       
            c = Circle().scale(R).set_stroke(GREY, width=10)
            self.play( Create(c) )

            angles = np.linspace(0,2*PI,n+1)[:-1] + offset
            dots = [ Dot([R * math.cos(a), R * math.sin(a),0]).set_color(FG).scale(2) for a in angles ]
            self.play( Create( VGroup(*dots) ) )
            self.wait(1)
            return dots

        def g(a,b):
            lines = []
            def d(u,v):
                dx = ( u.get_center()[0] - v.get_center()[0] ) **2 
                dy = ( u.get_center()[1] - v.get_center()[1] ) **2
                dz = ( u.get_center()[2] - v.get_center()[2] ) **2 
                return dx + dy + dz
            for u in b:
                print( f"{u.get_center()}" )
                dist = np.inf
                w = None
                for v in a:
                    if d(u,v) < dist:
                        w = v
                        dist = d(u,v)
                lines += Line( w.get_center(), u.get_center() ).set_stroke(FG)
            self.play( Create( VGroup(*lines) ) )
            self.wait(1)

        if True:

                k = 4
                a = [ Dot([0,0,0]).set_color(FG).scale(2) ]
                self.add( a[0] )
                self.wait(1)

                b = f(1,k,0)
                g(a,b)
                c = f(2,k*(k-1),0)
                g(b,c)
                d = f(3,k*(k-1)**2,0)
                g(c,d)
                e = f(4,k*(k-1)**3,0)
                g(d,e)

        text1 = MathTex( r"2\pi", "R" ).set_color(FG).shift(6*LEFT+3*UP)
        text2 = MathTex( r"2\pi", "n" ).set_color(FG).shift(6*LEFT+3*UP)
        self.play(Write(text1))
        self.wait(1)
        self.play(Transform(text1, text2))
        self.wait(1)        

        text = MathTex( r"4\times3^{n-1}" ).set_color(FG).shift(6*LEFT+2*UP)
        self.play(Write(text))
        self.wait(1)
                
        self.wait(10)


class MST(Scene):
    def construct(self):

        def f(A): 
            g = nx.Graph()
            for i in range(A.shape[0]):
                g.add_node(i)
            for i in range(A.shape[0]):
                for j in range(A.shape[1]):
                    if ( A[i,j] or A[j,i] ) and i<j:
                        g.add_edge(i,j)
            return g

        k = 100
        x = np.random.normal(size=(k,2*k))
        C = np.corrcoef(x)
        A = scipy.sparse.csgraph.minimum_spanning_tree(1-C)
        g = f(A)
        xy = nx.kamada_kawai_layout(g)
        xy = np.array(list(xy.values()))
        xy = xy - xy.min(axis=0)
        xy = xy / xy.max(axis=0)
        xy = 2 * xy - 1
        xy[:,0] = 6*xy[:,0]
        xy[:,1] = 3*xy[:,1]
        print(xy)
        objects = []
        for i in range(k):
            d = Dot( [ xy[i,0], xy[i,1], 0 ] ).set_color(FG).scale(1)
            objects += d
            for j in range(i):
                if A[i,j] == 0 and A[j,i] == 0:
                    continue
                line = Line( [ xy[i,0], xy[i,1], 0 ], [ xy[j,0], xy[j,1], 0 ] ).set_color(FG)
                objects += line
        self.play( Create(VGroup(*objects)) )

        self.wait(10)

        
from scipy.optimize import fsolve

def poincare_disk_compute_line( x1,y1, x2,y2 ):
    """
    Given two points (x1,y1), (x2,y2) in the unit disk, 
    compute the parameters the circle going through them
    and orthogonal to the unit circle.

    I assume that the line is not a diameter: the circle would be at infinity
    
    Inputs:  x1,y1: first point (cartesian coordinates, i.e., x^2+y^2<=1)
             x2,y2: second point
    Outputs: x0,y0: center of the circle (outside the unit circle)
             r: radius
             theta1, theta2: angles at which the two points are
    """
    def f(x):
        a,b = x
        return np.array([
            x1**2 + y1**2 + a*x1 + b*y1 + 1,
            x2**2 + y2**2 + a*x2 + b*y2 + 1,
        ])
    x0 = np.random.uniform(-1,1,2)
    a,b = fsolve(f,x0)
    x0, y0 = -a/2, -b/2
    r = math.sqrt( a**2/4 + b**2/4 - 1 )
    theta1 = math.atan2( y1-y0, x1-x0 )
    theta2 = math.atan2( y2-y0, x2-x0 )
    if theta1 <= theta2:
        if theta2 - theta1 > PI:
            theta2 = theta2 - 2*PI
    else:
        if theta1 - theta2 > PI:
            theta1 = theta1 - 2 * PI
    return x0, y0, r, theta1, theta2

def poincare_disk_line(x0, y0, r, scale=1):
    return Circle().scale(r*scale).shift([x0*scale,y0*scale,0]).set_color(GREY)

def poincare_disk_segment(x0, y0, r, theta1, theta2, n=10, scale=1):
    ts = np.linspace( theta1, theta2, n )
    lines = []
    for t1,t2 in zip( ts[:-1], ts[1:] ):
        lines += Line(
            scale * np.array([ x0 + r * math.cos(t1), y0 + r*math.sin(t1), 0 ] ),
            scale * np.array([ x0 + r * math.cos(t2), y0 + r*math.sin(t2), 0 ] ),
        ).set_color(FG)
    return lines

class PoincareDisk(Scene):
    SCALE = 3
    def construct(self):
        c = Circle().scale(self.SCALE).set_color(FG)
        self.play( Create(c) )
        self.wait(1)

        def random_point():
            done = False
            while not done:
                x = np.random.uniform(-1,+1)
                y = np.random.uniform(-1,+1)
                done = x**2 + y**2 <= 1
            return x,y

        for _ in range(5):
            x1,y1 = random_point()
            x2,y2 = random_point()
            dots = [
                Dot( self.SCALE * np.array([x1,y1,0]) ).set_color(FG),
                Dot( self.SCALE * np.array([x2,y2,0]) ).set_color(FG)
            ]
            self.play( Create(VGroup(*dots)) )
            x0, y0, r, theta1, theta2 = poincare_disk_compute_line( x1,y1, x2,y2 )
            c = poincare_disk_line( x0, y0, r, scale=self.SCALE )
            self.play( Create(c) )
            lines = poincare_disk_segment(x0, y0, r, theta1, theta2, n=10, scale=self.SCALE)
            self.play( Create(VGroup(*lines)) )
            self.wait(1)
        
def poincare_half_plane_compute_line(x1,y1, x2,y2):
    def f(x):
        x0, r, theta1, theta2 = x
        return [
            x0 + r * math.cos(theta1) - x1,
            0  + r * math.sin(theta1) - y1,
            x0 + r * math.cos(theta2) - x2,
            0  + r * math.sin(theta2) - y2,
        ]
    code = 0
    while code != 1:
        x0 = np.array([
            np.random.uniform(x1,x2),
            np.random.uniform(0,3),   # TODO
            np.random.uniform(0,PI),
            np.random.uniform(0,PI),
        ])    
        (x0, r, theta1, theta2), _, code, msg= fsolve(f,x0, full_output=True)
    
    theta1 = theta1 % TAU
    theta2 = theta2 % TAU
    print( f"x0={x0} r={r} theta1={theta1} theta2={theta2}" )    
    return x0, r, theta1, theta2

def poincare_half_plane_line( x0, r, shift=0 ):
    return Arc( radius=r, start_angle = 1e-4, angle=PI-2e-4, arc_center=[x0,shift,0] ).set_color(GREY)  # There is also a num_component=9 argument

def poincare_half_plane_segment( x0, r, theta1, theta2, shift=0 ):
    if theta1 > theta2:
        theta1, theta2 = theta2, theta1
    return Arc( radius=r, start_angle=theta1, angle=theta2-theta1, arc_center=[x0,shift,0] ).set_color(FG)
    
class PoincareHalfPlane(Scene):
    SHIFT = -2.5
    def construct(self):
        l = Line( [-7,self.SHIFT,0], [7,self.SHIFT,0] ).set_color(FG)
        self.play( Create(l) )

        def random_point():
            return np.random.uniform(-6,6), np.random.uniform(0,3)
            
        for _ in range(5):
            x1,y1 = random_point()
            x2,y2 = random_point()
            dots = [
                Dot( [x1,y1+self.SHIFT,0] ).set_color(FG),
                Dot( [x2,y2+self.SHIFT,0] ).set_color(FG)
            ]
            self.play( Create(VGroup(*dots)) )
            x0, r, theta1, theta2 = poincare_half_plane_compute_line( x1,y1, x2,y2 )
            c = poincare_half_plane_line( x0, r, shift=self.SHIFT )
            self.play( Create(c) )
            lines = poincare_half_plane_segment(x0, r, theta1, theta2, shift=self.SHIFT)
            self.play( Create(VGroup(*lines)) )
            self.wait(1)

        self.wait(10)


class PoincareHalfPlane2(Scene):
    SHIFT = -2.5
    def construct(self):
        l = Line( [-7,self.SHIFT,0], [7,self.SHIFT,0] ).set_color(FG)
        self.play( Create(l) )

        def random_point():
            return np.random.uniform(-6,6), np.random.uniform(0,3)

        def f(x1,y1,x2,y2,run_time=.5):
            x0, r, theta1, theta2 = poincare_half_plane_compute_line( x1,y1, x2,y2 )
            lines = poincare_half_plane_segment(x0, r, theta1, theta2, shift=self.SHIFT)
            self.play( Create(VGroup(*lines)), run_time = run_time )
            
        x1,y1 = -3,1
        x2,y2 = +3,1
        dots = [
            Dot( [x1,y1+self.SHIFT,0] ).set_color(FG),
            Dot( [x2,y2+self.SHIFT,0] ).set_color(FG),
        ]
        self.play( Create( VGroup(*dots) ) )
        self.wait(1)
        f(x1,y1,x2,y2,1)
        self.wait(1)
        for x in [-6,-5,-4,-2,-1,0,1,2,4,5,6]:
            f(x1,y1,x,1e-4)
        self.play( Create( Line( [x1,self.SHIFT,0], [x1,6,0] ).set_color(FG) ) )
        for x in [10,-10,20,-20,30,-30,-50]:            
            f(x1,y1, x,1e-4, .1)
        self.wait(10)
        
