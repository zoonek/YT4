import math
import numpy as np
from manim import *

config.background_color = WHITE
FG = BLACK

class GaussianFormula(Scene):
    def construct(self):
        t1 = MathTex(r"N(\mathbf{\mu},V)").set_color(FG).scale(3)
        t2 = MathTex(r"N(\mu,\sigma^2)").set_color(FG).scale(3)
        self.play( Write(t1) )
        self.wait(3)
        self.play( Transform(t1,t2) )
        self.wait(10)

def gaussian_distribution(self, x0=0, y0=0, s=1):
    "Draw a Gaussian density"
    axis = Line( [-3*s+x0,y0,0], [3*s+x0,y0,0] ).set_color(FG)
    self.play( Create(axis) )
    xmin = -3
    xmax = 3
    x = np.linspace(xmin,xmax,100)
    y = 3 * np.exp( - x ** 2 / 2 )
    p = [ [x0+s*u,y0+s*v,0] for (u,v) in zip(x,y) ]
    curve = [ Line(u,v).set_stroke(DARK_BLUE) for u,v in zip( p[:-1], p[1:] ) ]
    curve = VGroup(*curve)
    self.play(Create(curve))
    points = p + [ [x0+s*xmax,y0,0], [x0+s*xmin,y0,0] ]
    self.add( Polygon(*points, fill_color=BLUE, stroke_width=0, fill_opacity=.2) )

class GaussianDistribution(Scene):
    def construct(self):
        gaussian_distribution(self, y0=-1)
        self.wait(10)

class GaussianPlane(Scene):
    def construct(self):
        y0 = -2
        xaxis  = Arrow( [-6,y0,0], [6,y0,0], stroke_width=3, buff=0, color=FG )
        yaxis  = Arrow( [ 0,y0,0], [0,3,0], stroke_width=3, buff=0, color=FG )
        yaxis2 = Arrow( [ 0,-3.5,0], [0,3,0], stroke_width=3, buff=0, color=FG )
        self.play( Create(xaxis) )
        self.play( Create(yaxis) )
        xlabel = MathTex(r"\mu").set_color(FG).shift( [6,y0+.5,0] )
        ylabel1 = MathTex(r"\sigma^2"    ).set_color(FG).shift( [.5,3.2,0] )
        ylabel2 = MathTex(r"\sigma"      ).set_color(FG).shift( [.5,3.2,0] )
        ylabel3 = MathTex(r"\log\sigma^2").set_color(FG).shift( [.5,3.5,0] )
        d = Dot( [3,y0+3,0], color=FG )
        label = MathTex(r"N(\mu,\sigma^2)").set_color(FG).shift( [3,y0+3.5,0] )
        self.play( Write(xlabel) )
        self.play( Write(ylabel1) )
        self.play( Create(d) )
        self.play( Write(label) )
        self.wait(1)
        self.play( Transform(ylabel1,ylabel2) )
        self.wait(1)
        self.play( Transform(ylabel1,ylabel3), Transform(yaxis,yaxis2) )
        self.wait(10)

class GaussianPlane2(Scene):
    def construct(self):
        y0 = -2
        xaxis  = Arrow( [-6,y0,0], [6,y0,0], stroke_width=3, buff=0, color=FG )
        yaxis  = Arrow( [ 0,y0,0], [0,3,0], stroke_width=3, buff=0, color=FG )
        xlabel = MathTex(r"\mu"   ).set_color(FG).shift( [6,y0+.5,0] )
        ylabel = MathTex(r"\sigma").set_color(FG).shift( [.5,3.2,0] )
        d1  = Dot( [3,y0+3,0], color=FG )
        d1a = Dot( [3,y0+1/3,0], color=FG )
        d1b = Dot( [3,y0+3,0], color=FG )
        d2  = Dot( [-3,y0+3,0], color=FG )
        d2a = Dot( [-3,y0+1/3,0], color=FG )
        d2b = Dot( [-3,y0+3,0], color=FG )
        label1 = MathTex(r"N(\mu,\sigma_1^2)").set_color(FG).shift( [ 3,y0+3.5,0] )
        label2 = MathTex(r"N(\mu,\sigma_2^2)").set_color(FG).shift( [-3,y0+3.5,0] )
        self.play( Create(xaxis), Create(yaxis), Write(xlabel), Write(ylabel) )
        self.play( Create(d1), Create(d2) )
        self.play( Write(label1), Write(label2) )
        self.wait(1)

        k = 10
        N = 100
        np.random.seed(1)
        mu_hat    = np.zeros(N)
        sigma_hat = np.zeros(N)
        for n in range(N):
            x = np.random.normal(size=k)
            mu_hat[n] = x.mean()
            sigma_hat[n] = x.std()
        a = ( max(mu_hat) - min(mu_hat) ) / 2
        b = -a
        bar1  = DoubleArrow( [-3+a/3, y0+1/3,0], [3+b/3, y0+1/3,0], stroke_width=3, buff=0, color=FG )
        bar1a = DoubleArrow( [-3+a/3, y0+1/3,0], [3+b/3, y0+1/3,0], stroke_width=3, buff=0, color=FG )
        bar1b = DoubleArrow( [-3+a*3, y0+3,  0], [3+b*3, y0+3,  0], stroke_width=3, buff=0, color=FG )
        dd1  = VGroup( *[ Dot([-3+u/3, y0+v/3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd1a = VGroup( *[ Dot([-3+u/3, y0+v/3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd1b = VGroup( *[ Dot([-3+3*u, y0+3*v, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd2  = VGroup( *[ Dot([3+u/3, y0+v/3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd2a = VGroup( *[ Dot([3+u/3, y0+v/3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd2b = VGroup( *[ Dot([3+3*u, y0+3*v, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        self.play( FadeOut(label1), FadeOut(label2) )
        self.play( Transform(d1,d1a), Transform(d2,d2a) )
        self.wait(1)
        self.play(Create(dd1), Create(dd2), Create(d1a), Create(d2a), FadeOut(d1), FadeOut(d2))
        self.wait(1)
        self.play(Create(bar1))
        self.wait(1)
        self.play(
            Transform(dd1,dd1b), Transform(dd2,dd2b),
            Transform(d1a,d1b), Transform(d2a,d2b),
            Transform(bar1,bar1b)
        )
        self.wait(10)

class GaussianPlane3(Scene):
    def construct(self):
        y0 = -2
        xaxis  = Arrow( [-6,y0,0], [6,y0,0], stroke_width=3, buff=0, color=FG )
        yaxis  = Arrow( [ 0,y0,0], [0,3,0], stroke_width=3, buff=0, color=FG )
        xlabel = MathTex(r"\mu"   ).set_color(FG).shift( [6,y0+.5,0] )
        ylabel = MathTex(r"\sigma").set_color(FG).shift( [.5,3.2,0] )
        d1  = Dot( [3,y0+3,0], color=FG )
        d1a = Dot( [3,y0+3,0], color=FG )
        d1b = Dot( [3,y0+1/3,0], color=FG )
        d2  = Dot( [-3,y0+3,0], color=FG )
        d2a = Dot( [-3,y0+3,0], color=FG )
        d2b = Dot( [-3,y0+1/3,0], color=FG )
        label1 = MathTex(r"N(\mu,\sigma_1^2)").set_color(FG).shift( [ 3,y0+3.5,0] )
        label2 = MathTex(r"N(\mu,\sigma_2^2)").set_color(FG).shift( [-3,y0+3.5,0] )
        self.play( Create(xaxis), Create(yaxis), Write(xlabel), Write(ylabel) )
        self.play( Create(d1), Create(d2) )
        self.play( Write(label1), Write(label2) )
        self.wait(1)

        k = 10
        N = 100
        np.random.seed(1)
        mu_hat    = np.zeros(N)
        sigma_hat = np.zeros(N)
        for n in range(N):
            x = np.random.normal(size=k)
            mu_hat[n] = x.mean()
            sigma_hat[n] = x.std()
        a = ( max(mu_hat) - min(mu_hat) ) / 2
        b = -a
        bar1  = DoubleArrow( [-3+a*3, y0+3,  0], [3+b*3, y0+3,  0], stroke_width=3, buff=0, color=FG )
        bar1a = DoubleArrow( [-3+a*3, y0+3,  0], [3+b*3, y0+3,  0], stroke_width=3, buff=0, color=FG )
        bar1b = DoubleArrow( [-3+a/3, y0+1/3,0], [3+b/3, y0+1/3,0], stroke_width=3, buff=0, color=FG )
        dd1  = VGroup( *[ Dot([-3+u*3, y0+v*3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd1a = VGroup( *[ Dot([-3+u*3, y0+v*3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd1b = VGroup( *[ Dot([-3+u/3, y0+v/3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd2  = VGroup( *[ Dot([+3+u*3, y0+v*3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd2a = VGroup( *[ Dot([+3+u*3, y0+v*3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        dd2b = VGroup( *[ Dot([+3+u/3, y0+v/3, 0], color=GREY, fill_opacity=.5) for u,v in zip(mu_hat, sigma_hat) ] )
        self.play( FadeOut(label1), FadeOut(label2) )
        #self.play( Transform(d1,d1a), Transform(d2,d2a) )
        self.wait(1)
        self.play(Create(dd1), Create(dd2), Create(d1a), Create(d2a), FadeOut(d1), FadeOut(d2))
        self.wait(1)
        self.play(Create(bar1))
        self.wait(1)
        self.play(
            Transform(dd1,dd1b), Transform(dd2,dd2b),
            Transform(d1a,d1b), Transform(d2a,d2b),
            Transform(bar1,bar1b)
        )
        self.wait(10)
        
class DistancesDifferent(Scene):
    def construct(self):
        a  = MathTex(r" d\bigl( N(a,\sigma_1^2) , N(b,\sigma_1^2) \bigr) ", color=FG).shift(UP)
        a  = MathTex(r"d\bigl( N(a,", r"\sigma_1^2", r") , N(b,", r"\sigma_1^2", r") \bigr) ", color=FG).shift(UP)
        b  = MathTex(r"d\bigl( N(a,", r"\sigma_1^2", r") , N(b,", r"\sigma_1^2", r") \bigr) ", color=FG).shift(UP)
        b1  = MathTex(r"d\bigl( N(a,", r"\sigma_2^2", r") , N(b,", r"\sigma_2^2", r") \bigr) ", color=FG).shift(DOWN)
        c = MathTex(r"\neq", color=FG)
        a.set_color_by_tex(r"\sigma_1", RED)
        b.set_color_by_tex(r"\sigma_1", RED)
        b1.set_color_by_tex(r"\sigma_2", BLUE)
        self.play( Write(a) )
        self.wait(1)
        self.add(b)
        self.play( Transform(b, b1) )
        self.wait(1)
        self.play( Write(c) )
        self.wait(10)
        
