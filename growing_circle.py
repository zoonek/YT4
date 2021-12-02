#
# I tried to use OpenGL instead of Cairo, with little success.
# Add the following line: 
#   from manim.opengl import *
# Replace Surface with OpenGLSurface.
# The checkerboard_colors argument has disappeeared.
# Generate the videos with:
#   manim -pql --renderer=opengl --write_to_movie growing_circle_opengl.py CircleNegative
# 

from manim import *

FG = BLACK
BG = WHITE
config.background_color = BG

def f(u,v):
    "Negative curvature surface"
    return np.array([
        u * np.cos(v),
        u * np.sin(v),
        .2 * u**1.5 * np.cos(5*v),
    ])

def cross_product(a,b):
    return np.array( [
        a[1] * b[2] - b[1] * a[2],
        b[0] * a[2] - a[0] * b[2],
        a[0] * b[1] - b[0] * a[1],
    ] )

def normalize(a):
    n = np.sqrt( a[0] ** 2 + a[1] ** 2 + a[2] ** 2 )
    return a/n

def d1(f,t,h=1e-6):
    return ( f(t+h) - f(t-h) ) / (2*h)

def d2(f,t,h=1e-6):
    return ( f(t+h) - 2 * f(t) + f(t-h) ) / ( h**2 )
    
def tube(f, t_range, **kwargs):
    return ParametricFunction(f, t_range, **kwargs).set_shade_in_3d(True)

def tube( f, t_range, r = .1, **kwargs):    
    def g(u,v):
        f1 = normalize( d1(f,u) )
        f2 = normalize( d2(f,u) )   # Not stable enough (it is zero at each inflexion point)
        a = normalize( cross_product(f1,f2) )
        b = normalize( cross_product(f1,a) )
        assert abs( a[0]**2 + a[1]**2 + a[2]**2 - 1 ) < 1e-6
        assert abs( b[0]**2 + b[1]**2 + b[2]**2 - 1 ) < 1e-6
        if False: 
            print(f"u = {u}")
            print(f"v = {v}")
            print(f"a = {a}")
            print(f"b = {b}")
            print(f"{u} f1 = {f1}")
        return f(u) + r * np.cos(v) * a + r * np.sin(v) * b
    return Surface(
        g,
        u_range = t_range,
        v_range = [0, TAU],
        checkerboard_colors = False,
        resolution = (200,5),
        fill_opacity = 1,
    )

def tube( f, t_range, r = .1, **kwargs):
    previous = None
    def g(u,v):
        nonlocal previous
        f1 = normalize( d1(f,u) )
        if previous is None: 
            f2 = normalize( d2(f,u) )
            a = normalize( cross_product(f1,f2) )
        else:
            a = normalize( cross_product(f1,previous) )
            a = -normalize( cross_product(f1,a) )
        previous = a
        b = normalize( cross_product(f1,a) )
        return f(u) + r * np.cos(v) * a + r * np.sin(v) * b
    return Surface(
        g,
        u_range = t_range,
        v_range = [0, TAU],
        checkerboard_colors = False,
        stroke_width = 0,
        fill_color = BLUE,
        resolution = (100,10),
        fill_opacity = 1,
    )
    
class CircleNegative(ThreeDScene):
    def construct(self):
        label = MathTex( r"L > 2\pi R", color=BG ).to_edge(UL)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        s = always_redraw( lambda : Surface(
            f, u_range = [0,4], v_range = [0, TAU],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,50),
            fill_opacity = 1,
        ) )
        radius = ValueTracker(.5)
        c = always_redraw( lambda : tube(
            lambda v: f(radius.get_value(),v),
            t_range = [0,TAU],
            color = DARK_BLUE
        ).set_shade_in_3d(True) )
        self.play( Create(s) )
        self.add(c)
        self.add(radius)
        self.play(radius.animate.set_value(4), run_time=5)

        self.play(label.animate.set_color(FG), run_time=2)
        #self.play(Write(label))
        
        self.begin_ambient_camera_rotation(rate=TAU/30, about='theta')  # This REALLY slows things down...
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(10)

def f_sphere(u,v, R=3):
    "Positive curvature surface"
    return np.array([
        R * np.sin(u) * np.cos(v),
        R * np.sin(u) * np.sin(v),
        R * np.cos(u),
    ])
        
class CirclePositive(ThreeDScene):
    def construct(self):
        label = MathTex( r"L < 2\pi R", color=BG ).to_edge(UL)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        s = always_redraw( lambda : Surface(
            f_sphere, u_range = [0,4], v_range = [0, TAU],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,20),
            fill_opacity = 1,
        ) )
        radius = ValueTracker(.1)
        c = always_redraw( lambda : tube(
            lambda v: f_sphere(radius.get_value(),v, R=3.1),
            t_range = [0,TAU],
            color = DARK_BLUE
        ).set_shade_in_3d(True) )
        self.play( Create(s) )
        self.add(c)
        self.add(radius)
        self.play(radius.animate.set_value(1.7), run_time=5)
        self.play(label.animate.set_color(FG), run_time=2)
        self.wait(10)
        

class CircleFlat(Scene):
    def construct(self):
        r = ValueTracker(3)
        c = always_redraw( lambda : Circle( radius = r.get_value(), stroke_color = FG ))
        label = MathTex( r" L = 2 \pi R " ).to_edge(UL).set_color(FG)
        self.play( Create(c) )
        self.wait(1)
        self.play( Write(label) )
        self.play( r.animate.set_value(.5), run_time=3 )
        self.wait(1)
        self.play( r.animate.set_value(3), run_time=2 )
        self.wait(10)
        

class CurvaturePositive(ThreeDScene):
    def construct(self):
        label = Tex( r"Positive\\curvature", color=BG ).to_edge(UR)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        s = Surface(
            f_sphere, u_range = [0,4], v_range = [0, TAU],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,20),
            fill_opacity = 1,
        )
        self.play( Create(s), run_time=2 )
        self.play(label.animate.set_color(FG), run_time=1)
        self.wait(10)
        
class CurvatureNegative(ThreeDScene):
    def construct(self):
        label = Tex( r"Negative\\curvature", color=BG ).to_edge(UR)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        s = Surface(
            f, u_range = [0,4], v_range = [0, TAU],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,50),
            fill_opacity = 1,
        )
        self.play( Create(s), run_time=2 )
        self.play(label.animate.set_color(FG), run_time=1)
        self.wait(10)

class Flat1(ThreeDScene):
    def construct(self):
        label = Tex( r"Zero\\curvature", color=BG ).to_edge(UR)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        r1 = 2
        r2 = ValueTracker(2)
        h = 3
        def f(u,v):
            lam = (v+h) / (2*h)
            r = (1-lam) * r1 + lam * r2.get_value()
            return np.array([ r*np.cos(u), r*np.sin(u), v])
        s = always_redraw( lambda: Surface(
            lambda u,v: f(u,v),
            u_range = [0, TAU],
            v_range = [-h,h],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (50,20),
            fill_opacity = 1,
        ) )
        self.play( Create(s), run_time=2 )
        self.play(label.animate.set_color(FG), run_time=1)
        self.wait(1)
        self.play(r2.animate.set_value(0), run_time=3 )
        self.wait(10)
        
class Flat2(ThreeDScene):
    def construct(self):
        label = Tex( r"Zero\\curvature", color=BG ).to_edge(UR)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        r1 = 2
        r2 = ValueTracker(2)
        h = 3
        def f(u,v):
            lam = (v+h) / (2*h)
            r = (1-lam) * r1 + lam * r2.get_value()
            return np.array([ r*np.cos(u), r*np.sin(u), v])
        s = Surface(
            lambda u,v: f(u,v),
            u_range = [0, TAU],
            v_range = [-h,h],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (50,20),
            fill_opacity = 1,
        )
        s3 = Surface(
            lambda u,v: f(u,v),
            u_range = [0, TAU],
            v_range = [-h,h],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (50,20),
            fill_opacity = 1,
        )
        theta = -PI/3
        s2 = Surface(
            lambda u,v: np.array([u*np.cos(theta),u*np.sin(theta),v]),
            u_range = [-PI, PI],
            v_range = [-h,h],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (50,20),
            fill_opacity = 1,
        )
        s4 = always_redraw( lambda: Surface(
            lambda u,v: f(u,v),
            u_range = [0, TAU],
            v_range = [-h,h],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (50,20),
            fill_opacity = 1,
        ) )
        
        self.play( Create(s), run_time=1 )
        self.play(label.animate.set_color(FG), run_time=1)
        self.wait(1)
        self.play( Transform(s,s2), run_time=3 )
        self.wait(1)
        self.play( Transform(s,s3), run_time=2 )
        self.wait(1)
        self.add(s4)
        self.remove(s)
        self.play(r2.animate.set_value(0), run_time=3 )
        self.wait(10)

class Hyperboloid(ThreeDScene):
    def construct(self):
        Axes = ThreeDAxes()        
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        a = b = .7
        c = .75
        s = Surface(
            lambda u,v: np.array([
                a * np.cosh(v) * np.cos(u),
                b * np.cosh(v) * np.sin(u),
                c * np.sinh(v),
            ]),
            u_range = [-PI, PI],
            v_range = [-2,2],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (50,20),
            fill_opacity = 1,
        )
        self.play(Create(s))
        self.wait(10)
        
class Saddle(ThreeDScene):
    def construct(self):
        Axes = ThreeDAxes()        
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        a = .5
        b = 1.4
        s = Surface(
            lambda u,v: b * np.array([ u, v, a * ( u ** 2 - v ** 2 ) ]) + .4 * np.array([0,0,1]),
            u_range = [-2,2],
            v_range = [-2,2],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,20),
            fill_opacity = 1,
        )
        self.play(Create(s))

        self.begin_ambient_camera_rotation(rate=TAU/30, about='theta')  # This REALLY slows things down...
        self.wait(10)
        self.stop_ambient_camera_rotation()
        
        self.wait(10)


class SurfaceExamples(ThreeDScene):
    def construct(self):
        
        Axes = ThreeDAxes()        
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)

        sphere = Sphere(radius=2, checkerboard_colors = [RED_D, RED_E] )

        torus = Torus( major_radius=3, minor_radius=1, checkerboard_colors = [RED_D, RED_E] )
        
        a = b = .7
        c = .75
        hyperboloid = Surface(
            lambda u,v: np.array([
                a * np.cosh(v) * np.cos(u),
                b * np.cosh(v) * np.sin(u),
                c * np.sinh(v),
            ]),
            u_range = [-PI, PI],
            v_range = [-2,2],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (50,20),
            fill_opacity = 1,
        )
        
        a = .5
        b = 1.4
        saddle = Surface(
            lambda u,v: b * np.array([ u, v, a * ( u ** 2 - v ** 2 ) ]) + .4 * np.array([0,0,1]),
            u_range = [-2,2],
            v_range = [-2,2],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,20),
            fill_opacity = 1,
        )

        o = sphere.copy()
        self.begin_ambient_camera_rotation(rate=TAU/30, about='theta')  # This REALLY slows things down...        
        self.play( Create(o) )
        self.wait(1)
        self.play( Transform(o, torus) )
        self.wait(1)
        self.play( Transform(o, hyperboloid) )
        self.wait(1)
        self.play( Transform(o, saddle) )
        self.wait(1)
        self.stop_ambient_camera_rotation()
        
class CurvatureExamples(ThreeDScene):
    def construct(self):
        
        Axes = ThreeDAxes()        
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)

        plane = Surface(
            lambda u,v: np.array([u, v, 0]),
            u_range = [-3,3],
            v_range = [-3,3],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,20),
            fill_opacity = 1,
        )

        sphere = Sphere(radius=3, checkerboard_colors = [RED_D, RED_E] )
        
        a = .5
        b = 1.4
        saddle = Surface(
            lambda u,v: b * np.array([ u, v, a * ( u ** 2 - v ** 2 ) ]) + .4 * np.array([0,0,1]),
            u_range = [-2,2],
            v_range = [-2,2],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,20),
            fill_opacity = 1,
        )

        o = plane.copy()
        self.begin_ambient_camera_rotation(rate=TAU/30, about='theta')  # This REALLY slows things down...        
        self.play( Create(o) )
        label = MathTex( r"R=0", color=FG ).to_edge(UR)
        self.add_fixed_in_frame_mobjects(label)
        self.wait(1)
        self.remove(label)
        
        self.play( Transform(o, sphere) )
        label = MathTex( r"R>0", color=FG ).to_edge(UR)
        self.add_fixed_in_frame_mobjects(label)           
        self.wait(1)
        self.remove(label)
        
        self.play( Transform(o, saddle) )
        label = MathTex( r"R<0", color=FG ).to_edge(UR)
        self.add_fixed_in_frame_mobjects(label)           
        self.wait(10)
        
        self.stop_ambient_camera_rotation()
