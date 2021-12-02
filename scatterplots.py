from manim import *
import pickle, re, datetime

FG = BLACK
BG = WHITE
config.background_color = BG

def load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def save( data, filename, message = None ):
    log_file = re.sub('[.].pickle$', '', filename) + '.log'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write( f"{timestamp} {' '.join(sys.argv)}\n" )
        if message is not None:
            f.write( f"{timestamp} {message}\n" )
    with open(filename, 'wb') as f:
        pickle.dump(data,f)

def normalize(u):
    return u / np.sqrt( (u**2).sum() )

def random_unit_vector(k): 
    u = np.random.normal(size=k)
    u = normalize(u)
    return u

def random_projection_matrix(k):
    u = random_unit_vector(k)
    v = random_unit_vector(k)
    v = v - (u*v).sum() * u
    v = normalize(v)
    P = np.stack([u,v]).T
    return P

def random_projection(X):
    x = X @ random_projection_matrix( X.shape[1] )
    x = x - x.mean(axis=0)
    x = 3 * x
    print( x.max() )
    return x
    
class Mnist(Scene):
    def construct(self):
        X = load('mnist_x.pickle')
        y = load('mnist_y.pickle')
        
        # Reduce the volume of data
        n = 1000
        X = X[:n,:]
        y = y[:n]

        # Normalize (bad idea: there were mostly zeroes, so now have mostly -1's...)
        X = 2*X/255 - 1
       
        # Plot
        colours = {
            '0': BLUE,
            '1': RED,
            '2': YELLOW,
            '3': GREEN,
            '4': TEAL,
            '5': PINK,
            '6': ORANGE,
            '7': MAROON,
            '8': GOLD,
            '9': PURPLE,
        }

        def f(): 
            x = random_projection(X)        
            points = []
            for i in range(n):
                points.append( Dot( [ x[i,0], x[i,1], 0 ], color=colours[y[i]]) )
            points = VGroup(*points)
            return points

        points = f()
        self.add(points)
        self.wait(1)
        label = Tex("MNIST data",color=FG).scale(.5).to_edge(-UR)
        self.play( Write(label) )
        self.wait(1)

        self.wait(1); self.play( Transform(points, f()) )
        self.wait(1); self.play( Transform(points, f()) )
        self.wait(1); self.play( Transform(points, f()) )
        self.wait(1)
            
        self.play( FadeOut(label) )
        self.wait(1)

        # PCA
        xy = load( 'mnist_pca.pickle' )
        xy = xy - xy.mean(axis=0)
        xy = 3e-3 * xy        
        pca = []
        for i in range(n):
            pca.append( Dot( [ xy[i,0], xy[i,1], 0 ], color=colours[y[i]]) )
        pca = VGroup(*pca)        
        label = Tex( "PCA", color=FG ).scale(2).to_edge(UR)
        self.play( Transform(points, pca), Write(label), run_time=2 )        
        self.wait(2)

        # TSNE
        p=30
        xy = load( f'mnist_tsne_p={p}.pickle' )
        xy = xy - xy.mean(axis=0)
        xy = .08 * xy        
        tsne = []
        for i in range(n):
            tsne.append( Dot( [ xy[i,0], xy[i,1], 0 ], color=colours[y[i]]) )
        tsne = VGroup(*tsne)
        label2 = Tex( "t-SNE", color=FG ).scale(2).to_edge(UR)
        self.play( Transform(points, tsne), Transform(label,label2), run_time=2 )        
        self.wait(2)
        
        # UMAP
        xy = load( 'mnist_umap.pickle' )
        xy = xy - xy.mean(axis=0)
        xy = .3 * xy        
        umap = []
        for i in range(n):
            umap.append( Dot( [ xy[i,0], xy[i,1], 0 ], color=colours[y[i]]) )
        umap = VGroup(*umap)

        label2 = Tex( "UMAP", color=FG ).scale(2).to_edge(UR)
        self.play( Transform(points, umap), Transform(label,label2), run_time=2 )

        self.wait(10)
        
        
        
