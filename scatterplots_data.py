import os, pickle, re, datetime, sys
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP 

def LOG(s):
    print(s)

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

if not os.path.exists('mnist_x.pickle') or not os.path.exists('mnist_y.pickle'):
    LOG( "Fetch MNIST data" )
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    LOG( "  Save MNIST data" )
    save(X, 'mnist_x.pickle')
    save(y, 'mnist_y.pickle')
    LOG( "  Done" ) 

LOG( "Load MNIST data" )    
X = load('mnist_x.pickle')
y = load('mnist_y.pickle')

if not os.path.exists('mnist_umap.pickle'):
    LOG( "UMAP" )
    LOG( "  Computations" )
    xy = UMAP().fit(X).embedding_
    LOG( "  Save the result" )
    save( xy, 'mnist_umap.pickle' )
    LOG( "  Done" )

p = 30
if not os.path.exists(f'mnist_tsne_p={p}.pickle'):
    LOG( "TSNE [LONG and CPU-intensive]" )
    LOG( "  Computations" )

    LOG( f"  Perplexity={p}" )
    xy = TSNE(n_components=2, perplexity = p).fit_transform(X)
    LOG( "  Save" )
    save( xy, f'mnist_tsne_p={p}.pickle' )

    LOG( "  Done" )

LOG( "PCA" )
LOG( "  Computations" )
xy = PCA(n_components=2).fit_transform(X)
LOG( "  Save" )
save( xy, 'mnist_pca.pickle' )
LOG( "  Done" )

LOG( "Done." )


