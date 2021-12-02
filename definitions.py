import math
import numpy as np
import scipy
import networkx as nx
from manim import *

config.background_color = WHITE
FG = BLACK

class Def1(Scene):
    def construct(self):
        t = Tex(r"""
\begin{minipage}{7cm}
A \textbf{metric space} $(X,d)$ is a set $X$ and a map $d: X \times X \to \mathbf{R}_+$
such that
\\\rlap{(i)}\qquad $\forall x,y \in X \quad d(x,y) = d(y,x)$
\\\rlap{(ii)}\qquad $\forall x,y \in X \quad d(x,y) = 0 \Longleftrightarrow x = y$
\\\rlap{(iii)}\qquad $\forall x,y,z \in X \quad d(x,z) \leqslant d(x,y) + d(y,z)$
\end{minipage}
        """ ).set_color(FG)
        self.play( FadeIn(t) )
        self.wait(1)
        self.play( FadeOut(t) )
        
        t2 = Tex(r"""
\begin{minipage}{7cm}
A \textbf{continuous map} $f: (X,d) \to (Y,d)$\\
between metric spaces is a map\\ 
$f:X \to Y$ such that 
\\\mbox{}\qquad $\forall x \in X \quad \forall \epsilon > 0 \quad \exists \eta > 0 \quad \forall x' \in X$
\\\mbox{}\qquad $d(x,x') < \eta \ \implies\  d\bigl( f(x), f(x') \bigr) < \epsilon$
\end{minipage}
        """ ).set_color(FG)
        self.play( FadeIn(t2) )
        self.wait(1)
        self.play( FadeOut(t2) )

        t3 = Tex(r"""
\begin{minipage}{7cm}
A \textbf{homeomorphism} is a bijective map between topological spaces,
$f: (X,d) \to (Y,d)$, such that both $f$ and $f^{-1}$ be continuous.
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t3) )
        self.wait(1)
        self.play( FadeOut(t3) )

        t4 = Tex(r"""
\begin{minipage}{8cm}
An \textbf{open set} in a metric space $(X,d)$ is a subset $U \subset X$
such that 
\\\mbox{}\qquad$\forall x \in U \quad \exists \epsilon>0 \quad B(x,\epsilon) \subset U$
\\where $B(x,\epsilon)$ is the \textbf{ball} of radius $\epsilon$ centered on $x$,
\\\mbox{}\qquad$ B(x,\epsilon) = \{ \, y \in X \ :\ d(x,y) \leq \epsilon \, \}. $
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t4) )
        self.wait(1)
        self.play( FadeOut(t4) )
        
        t5 = Tex(r"""
\begin{minipage}{8cm}
A \textbf{manifold} is the datum of 
\\\rlap{(i)}\qquad A metric space $(X,d)$
\\\rlap{(ii)}\qquad Open sets $U_i \subset X$, $i \in I$, covering $X$,
\\\mbox{}\qquad i.e., 
$\bigcup_{i\in I} = X$
\\\rlap{(iii)}\qquad Homeomorphisms $\phi_i : U_i \to V_i$ between
\\\mbox{}\qquad the $U_i$'s and opens sets $V_i \subset \mathbf{R}^n$
\\such that, for all $i,j \in I$, 
\\\mbox{}\quad$
\phi_i(U_i \cap U_j ) 
\xrightarrow{\phi_i^{-1}}
U_i \cap U_j 
\xrightarrow{\phi_j}
\phi_j( U_i \cap U_j )
$
\\be differentiable.\\
Each $\phi_i$ is called a \textbf{chart}; 
a set of charts, an \textbf{atlas}.
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t5) )
        self.wait(1)
        self.play( FadeOut(t5) )

        t6 = Tex(r"""
\begin{minipage}{8cm}
A \textbf{differentiable map} between 
manifolds
\\$\bigl(X, (\phi_i: U_i \to \mathbf{R}^n)_i\bigr)$ 
and $\bigl(Y, (\psi_j: V_j \to \mathbf{R}^m)_j \bigr)$ is a map $f:X\to Y$
such that the $\psi_j \circ f \circ \phi_i$ be diffenrentiable.

A \textbf{diffeomorphism} is a bijective differentiable map 
whose inverse is also differentiable.
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t6) )
        self.wait(1)
        self.play( FadeOut(t6) )

        t7 = Tex(r"""
\begin{minipage}{8cm}
A \textbf{tangent vector} at a point $x\in X$ of a manifold
is an equivalence class of curves $c: [-1,1] \to X$
such that $c(0)=x$ for the equivalence relation 
$c \sim d$ iff 
$( \phi \circ c )' (0) = ( \phi \circ d )' (0)$
for a chart $\phi: U \to \mathbf{R}^n$ 
with $x \in U$.\\ 
The set of tangent vectors forms a vector space, $T_xX$.
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t7) )
        self.wait(1)
        self.play( FadeOut(t7) )

        t8 = Tex(r"""
\begin{minipage}{8cm}
The \textbf{tangent bundle} of a manifold $X$
is the disjoint union of its tangent spaces, 
$ TX = \bigsqcup_{x\in X} T_x X; $
it can be endowed with a differentiable manifold structure.

\medskip
A \textbf{vector bundle} over a manifold $X$ 
is a differentiable surjection $\pi: Y \to X$
and a vector space structure on each $\pi^{-1}(x)$, 
such that there exists an open cover
$X = \bigcup_i U_i$
and diffeomorphisms
$\phi: U \times \mathbf{R}^k \to \pi^{-1}(U)$
such that $\pi \circ \phi = \text{pr}_1$
and the maps $v \mapsto \phi(y,v)$ be linear.
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t8) )
        self.wait(1)
        self.play( FadeOut(t8) )

        t9 = Tex(r"""
\begin{minipage}{8cm}
Operations on vector spaces (dual, tensor product, etc.)
can be generalized to vector bundles.

The \textbf{cotangent bundle} of a manifold $X$ is the dual ${T^*}\hspace*{-2pt}X$ of its tangent bundle.

\medskip
A \textbf{section} of a vector bundle $f : Y \to X$
is a differentiable map $s: X \to Y$ such that $f \circ s = \text{Id}_X$.

A \textbf{vector field} is a section of the tangent bundle.
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t9) )
        self.wait(1)
        self.play( FadeOut(t9) )

        t10 = Tex(r"""
\begin{minipage}{8cm}
A \textbf{Riemann metric} on a differentiable manifold $X$ is a 
section of $({T^*}\hspace*{-2pt}X)^{\otimes2}$ whose value at each point is positive definite.
\end{minipage}
        """).set_color(FG)
        self.play( FadeIn(t10) )
        self.wait(1)
        self.play( FadeOut(t10) )

        self.wait(10)

        
        
