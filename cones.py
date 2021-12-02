from manim import *
import math, colorsys, matplotlib

FG = BLACK
BG = WHITE
config.background_color = BG
        
def hsl_disk(v=.5, R=3):
    ps = []
    rs = np.linspace(0,1,10)
    ts = np.linspace(0,2*PI,50)
    for r1,r2 in zip( rs[:-1], rs[1:] ):
        for t1,t2 in zip( ts[:-1], ts[1:] ):
            hue = (t1+t2)/2 /(2*PI)
            hue = hue -.18
            s = (r1+r2)/2
            color = colorsys.hls_to_rgb( hue, v, s )
            color = matplotlib.colors.to_hex(color)
            p = Polygon( 
                [ R * r1 * math.cos(t1), R * r1 * math.sin(t1), 4*v-2 ],
                [ R * r2 * math.cos(t1), R * r2 * math.sin(t1), 4*v-2 ],
                [ R * r2 * math.cos(t2), R * r2 * math.sin(t2), 4*v-2 ],
                [ R * r1 * math.cos(t2), R * r1 * math.sin(t2), 4*v-2 ],
                fill_color=color,
                fill_opacity=1,
                color=FG,
                stroke_width=.3,
            )
            ps.append(p)
    ps = VGroup(*ps)
    return ps

class HSLDisk(Scene):
    def construct(self):
        d = hsl_disk()
        self.play( Create(d) )
        self.wait(1)

        a = Arrow( [0,0,0], [4,0,0], color=FG )
        b = Tex("saturation", color=FG).move_to([4.5,.5,0])
        self.play( Create(a) )
        self.play( Write(b) )
        self.wait(1)
        self.play( FadeOut(a), FadeOut(b) )
        self.wait(1)
        x = 3.5 * math.sqrt(3)/2
        y = 3.5 * 1/2
        a = CurvedArrow( [x,-y,0], [x,y,0], radius=3.5, color=FG )
        b = Tex("hue", color=FG).move_to([4.2,0,0])
        self.play( Create(a) )
        self.play( Write(b) )
        self.wait(1)
        self.play( FadeOut(a), FadeOut(b) )
        self.wait(1)
        
        for c in [.6, .7, .8, .9 ]:
            self.play( Transform(d, hsl_disk(c)), rate_func=linear, run_time=.25)
        self.wait(1)
        for c in [.8, .7, .6, .5, .4, .3, .2, .1 ]:
            self.play( Transform(d, hsl_disk(c)), rate_func=linear, run_time=.25)        
        self.wait(1)
        for c in [.2, .3, .4, .5]:
            self.play( Transform(d, hsl_disk(c)), rate_func=linear, run_time=.25)
        self.wait(10)        

class HLSCone(ThreeDScene):
    def construct(self):
        label = Tex( r"HSL", color=BG ).scale(2).to_edge(UL)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        rs = np.linspace(0,1,10)
        ts = np.linspace(0,2*PI,50)
        current = None
        all  = []
        all2 = []
        all3 = []
        # Show a disk, moving upwards in HSL space
        for v in np.linspace(0,1,11):
            ps = []
            qs = []
            qqs= []
            for r1,r2 in zip( rs[:-1], rs[1:] ):
                for t1,t2 in zip( ts[:-1], ts[1:] ):
                    hue = (t1+t2)/2 /(2*PI)
                    hue = hue -.18
                    s = (r1+r2)/2
                    color = colorsys.hls_to_rgb( hue, v, s )
                    color = matplotlib.colors.to_hex(color)
                    R = 3
                    p = Polygon( 
                        [ R * r1 * math.cos(t1), R * r1 * math.sin(t1), 4*v-2 ],
                        [ R * r2 * math.cos(t1), R * r2 * math.sin(t1), 4*v-2 ],
                        [ R * r2 * math.cos(t2), R * r2 * math.sin(t2), 4*v-2 ],
                        [ R * r1 * math.cos(t2), R * r1 * math.sin(t2), 4*v-2 ],
                        fill_color=color,
                        fill_opacity=1,
                        color=FG,
                        stroke_width=.1,
                    )
                    s = 1 - 2 * abs(v-.5)
                    R = R * s
                    height = 4 * v - 2
                    height *= 1 + 2 * abs(v-.5)
                    q = Polygon( 
                        [ R * r1 * math.cos(t1), R * r1 * math.sin(t1), height ],
                        [ R * r2 * math.cos(t1), R * r2 * math.sin(t1), height ],
                        [ R * r2 * math.cos(t2), R * r2 * math.sin(t2), height ],
                        [ R * r1 * math.cos(t2), R * r1 * math.sin(t2), height ],
                        fill_color=color,
                        fill_opacity=1,
                        color=FG,
                        stroke_width=.1,
                    )
                    def tilt(x,y,z):
                        if R == 0:
                            return [x,y,z]
                        theta = PI/12
                        A = [x, y * math.cos(theta), z + y * math.sin(theta)]
                        A[2] *= 2
                        return A
                    qq = Polygon( 
                        tilt( R * r1 * math.cos(t1), R * r1 * math.sin(t1), 4*v-2 ),
                        tilt( R * r2 * math.cos(t1), R * r2 * math.sin(t1), 4*v-2 ),
                        tilt( R * r2 * math.cos(t2), R * r2 * math.sin(t2), 4*v-2 ),
                        tilt( R * r1 * math.cos(t2), R * r1 * math.sin(t2), 4*v-2 ),
                        fill_color=color,
                        fill_opacity=1,
                        color=FG,
                        stroke_width=.1,
                    )                    
                    ps.append(p)
                    qs.append(q)
                    qqs.append(qq)
            ps = VGroup(*ps)
            qs = VGroup(*qs)
            qqs = VGroup(*qqs)
            all.append(ps.copy())
            all2.append(qs.copy())
            all3.append(qqs.copy())
            if current is None:
                current = ps
                self.add(ps)
            else:
                self.play( Transform(current, ps), rate_func=linear, run_time=.5)
        self.wait(1)

        # Show n disks
        self.play( *[ FadeIn(a) for a in all ] )
        self.remove(current)
        self.wait(1)

        # Reduce the size of some of them to show a double cone
        self.play(
            *[ Transform(p,q) for p,q in zip(all,all2) ],
            label.animate.set_color(FG),
        )

        self.wait(1)

        # Only show the disk in the middle
        self.play(
            *[ FadeOut(all[i]) for i in range(len(all)) if i != len(all)//2 ],
            label.animate.set_color(BG),
        )            
        self.wait(1)

        # Put the disks back
        self.remove( *all )
        self.add( all[ len(all) // 2 ] )
        self.play( *[ FadeIn(all[i]) for i in range(len(all)) if i != len(all)//2 ] ) # BUG

        # The problem is clearer here:
        #for i in range(len(all)):
        #    if i != len(all)//2:
        #        self.play( FadeIn(all[i]) )
        
        self.remove( *all )
        self.add( *all )
        self.wait(1)

        # Tilt them
        self.play( *[ Transform(p,q) for p,q in zip(all,all3) ] )
        
        self.begin_ambient_camera_rotation(rate=TAU/30, about='theta')  # This REALLY slows things down...        
        self.wait(30)
        self.stop_ambient_camera_rotation()

        
class HSVCylinder(ThreeDScene):  # Not used
    def construct(self):
        label = Tex( r"HSV", color=FG ).scale(2).to_edge(UL)
        self.add_fixed_in_frame_mobjects(label)
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        rs = np.linspace(0,1,10)
        ts = np.linspace(0,2*PI,50)
        current = None
        all  = []
        all2 = []
        for v in np.linspace(0,1,9):
            ps = []
            qs = []
            for r1,r2 in zip( rs[:-1], rs[1:] ):
                for t1,t2 in zip( ts[:-1], ts[1:] ):
                    hue = (t1+t2)/2 /(2*PI)
                    s = (r1+r2)/2
                    color = colorsys.hsv_to_rgb( hue, s, v )
                    color = matplotlib.colors.to_hex(color)
                    R = 3
                    p = Polygon( 
                        [ R * r1 * math.cos(t1), R * r1 * math.sin(t1), 4*v-2 ],
                        [ R * r2 * math.cos(t1), R * r2 * math.sin(t1), 4*v-2 ],
                        [ R * r2 * math.cos(t2), R * r2 * math.sin(t2), 4*v-2 ],
                        [ R * r1 * math.cos(t2), R * r1 * math.sin(t2), 4*v-2 ],
                        fill_color=color,
                        fill_opacity=1,
                        color=FG,
                        stroke_width=.1,
                    )
                    ps.append(p)
            ps = VGroup(*ps)
            all.append(ps.copy())
            if current is None:
                current = ps
                self.add(ps)
            else:
                self.play( Transform(current, ps), rate_func=linear, run_time=.5)
        self.wait(1)
        self.play( *[ FadeIn(a) for a in all ] )
        self.wait(10)


class ColourSpaceNames(Scene):
    def construct(self):
        luv = Tex("LUV", color=FG).scale(1.5).move_to([-3,2,0])
        lab = Tex("Lab", color=FG).scale(1.5).move_to([+3,2,0])
        polar_luv = Tex(r"Polar-LUV\\=\\HCL", color=FG).scale(1.5).move_to([-3,-1,0])
        polar_lab = Tex(r"Polar-Lab",       color=GREY).scale(1.5).move_to([+3,-1,0])
        self.play( Write(luv) )
        self.play( Write(lab) )
        self.play(
            Write(polar_luv),
            Write(polar_lab),
            luv.animate.set_color(GREY),
            lab.animate.set_color(GREY),
        )
        self.play(
            polar_luv.animate.scale(1.125), 
            luv.animate.set_color(BG),
            lab.animate.set_color(BG),
            polar_lab.animate.set_color(BG),
            run_time=5, rate_func=linear            
        )
        self.play(
            polar_luv.animate.scale(1.5),
            run_time=15, rate_func=linear,
        )
            
            
        
        
