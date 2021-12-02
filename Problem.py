#
# Do not use ThreeDAxes.plot_parametric_curve: the coordinates are off
# (It is apparently a known problem.)
# 

from manim import *

def f(u,v):
    return np.array([
        u * np.cos(v),
        u * np.sin(v),
        .2 * u**1.5 * np.cos(3*v),
    ])
    
class Example(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        s = Surface( f, u_range = [0,4], v_range = [0, TAU] )
        c = axes.plot_parametric_curve( lambda v: f(4,v), t_range = [0,TAU] )
        c = ParametricFunction( lambda v: f(4,v), t_range = [0,TAU] )
        self.add(s)
        self.add(c)
        

