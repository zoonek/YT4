from manim import *
import manimpango

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters.pangomarkup import PangoMarkupFormatter
from pygments.styles import get_all_styles

config.background_color, FG = BLACK, WHITE

class ExampleText(Scene):
    def construct(self):
        # To see the available fonts:
        #   import manimpango
        #   manimpango.list_fonts()
        # If you change the font and do not see any change,
        # it could be that manim is reusing old files: delete the media/ directory
        for font in [
            '/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Regular.ttf',                
            #'/usr/local/share/fonts/GoogleFonts/Bitter/Bitter-Bold.ttf',
            '/usr/local/share/fonts/GoogleFonts/Alegreya/Alegreya-Regular.ttf',
        ]:
            assert manimpango.register_font(font), f"Cannot register font {font}"
        t  = Text( "Non-LaTeX text", font='Alegreya' ).scale(2)
        t2 = Text( "Non-LaTeX text", font='Bitter', weight=BOLD ).scale(2)
        self.play( Write(t) )
        self.wait(1)
        self.play( Transform(t,t2) )
        self.wait(1)
        self.play(ApplyMethod(t.scale, 1.3),run_time=10)

class ExampleTeX(Scene):
    # Tex() for text, MathTex() for math; the math is typset in align*: you can use & and \\
    # Non-LaTeX: Text()
    # Add to the scene: self.add(t) or self.play(Write(t))
    # Write() can be replaced by Create, FadeIn, etc.
    # To add packages:
    #     myTemplate = TexTemplate()
    #     myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    #     tex = Tex(..., tex_template=myTemplate)
    def construct(self):
        t1 = Tex( r"Text with \LaTeX", font_size=96 )
        t2 = MathTex( r"x = \dfrac{ -b \pm \sqrt{ b^2 - 4 ac } }{ 2a }", font_size=96 )
        t = VGroup( t1, t2 ).arrange(DOWN) 
        self.play( Write(t) )
        self.wait(10)

class ExampleCode(Scene):
    # Use "Pygments" to typeset code into PangoMarkup; feed the result to MarkupText
    def construct(self):
        code = r"""
class Example(Scene):
  def construct(self):
    t = Tex(r"Text with \LaTeX")        
    self.play( Write(t) )
    self.wait(10)
        """
        style = 'inkpot'
        label = Text(style, color=FG).move_to([0,3.5,0])
        t = highlight(code, PythonLexer(), PangoMarkupFormatter(style=style))
        t = MarkupText(t)  # Not HTML, but "PangoMarkup"
        self.add(t.shift([0,-.5,0]), label)

        # On a black background, the following styles are more readable than the default:
        #   material, native, fruity, paraiso-dark, inkpot, gruvbox-dark
        # On a white background, most of the styles are readable:
        #   emacs, autumn, default, friendly, colorful, murphy, perfdoc,
        #   igor, paraiso-light, rainbow_dash, gruvbox-light
        for style in get_all_styles():
            print( style )
            u = highlight(code, PythonLexer(), PangoMarkupFormatter(style=style))
            u = MarkupText(u, color=FG).shift([0,-.5,0])
            l2 = Text( str(style), color=FG ).move_to([0,3.5,0])
            self.play( Transform(t,u), Transform(label,l2) )
            self.wait(1)
    
        self.wait(10)

class Example3DSphere(ThreeDScene):
    # From the tutorial
    def construct(self):
        axes = ThreeDAxes()
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]),
            v_range = [0, TAU],
            u_range = [-PI / 2, PI / 2],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (15, 32)
        )
        self.renderer.camera.light_source.move_to(3*IN)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play( Create(axes) )
        self.play( Create(sphere) )
        self.wait(10)

class Example3DSaddle1(ThreeDScene):
    def construct(self):

        if False: 
            s = Surface(
                lambda u, v: np.array([ u, v, u**2 - v**2 ]),
                v_range = [-1.5,1.5],
                u_range = [-1.5,1.5],
                checkerboard_colors = [RED_D, RED_E],
                resolution = (20,20),
            )
            self.renderer.camera.light_source.move_to(3*IN)
            self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
            self.play( Create(s) )
            self.wait(1)
            self.remove(s)
        
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        s = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                #.2 * u**1.5 * ( np.cos(v) **2 - np.sin(v) ** 2 ),
                .2 * u**1.5 * np.cos(3*v),
            ]),
            u_range = [0,4],
            v_range = [0, 2*PI],
            checkerboard_colors = [RED_D, RED_E],
            resolution = (20,50),
        )
        u = .1
        c = axes.plot_parametric_curve(
            lambda v: [
                u * np.cos(v),
                u * np.sin(v),
                #.2 * u**1.5 * ( np.cos(v) **2 - np.sin(v) ** 2 ),
                .2 * u**1.5 * np.cos(3*v),
            ],
            t_range = [0,TAU],
            color = DARK_BLUE,
        )
        u = 3.5
        c1 = axes.plot_parametric_curve(
            lambda v: [
                u * np.cos(v),
                u * np.sin(v),
                #.2 * u**1.5 * ( np.cos(v) **2 - np.sin(v) ** 2 ),
                .2 * u**1.5 * np.cos(3*v),
            ],
            t_range = [0,TAU],
            color = DARK_BLUE,
        )

        self.add(s)
        self.add(c1)
        
        if False: 
            self.play( Create(s) )
            self.add(s)
            self.play( Create(c) )
            #self.move_camera(phi=60 * DEGREES, theta=TAU, run_time=5)

            self.play( Transform(c,c1), run_time=10 )

            #self.begin_ambient_camera_rotation(rate=TAU/10, about='theta')  # This REALLY slows things down...
            #self.wait(1)
            #self.stop_ambient_camera_rotation()
        self.wait(10)
        

