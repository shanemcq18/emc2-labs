
# Lab 21: Iterating Functions

We have seen many types of sequences so far, and in this lab we will introduce another: the sequence of iterates of a function $f$ for some fixed $x \in \mathbb{R}$. We have often been concerned about whether a sequence converges or diverges. For the sequences that we will consider in this lab, we will ask the related question of whether the sequence is bounded or whether it diverges to infinity.

First, we define an iterate. Let $f: \mathbb{R} \to \mathbb{R}$. Define $f^2 = f \circ f$, $f^3 = f \circ f \circ f$, and so on, so that $f^n = f\circ f \circ \dots \circ f$ is the composition involving $n$ copies of $f$. We call $f^n$ the $n$-th *iterate* of $f$. Recall that $\circ$ denotes function composition, so $f^2(x) = (f \circ f) (x) = f(f(x))$.


:::{admonition} Task 1
:class: exercise


Let $f(x) = x^2 - 1$. By hand, compute at least the first four terms of the sequence of iterates of $f$ (starting at $x$) for $x = 0$ and $x = 1$.

:::

:::{admonition} Task 2
:class: exercise


Write a function, `iterate(f, x, n)`, that computes the first `n` iterates of `f` evaluated at `x`. You should consider doing this using bottom-up dynamic programming, i.e. create a list of terms and use the terms you have already computed to compute the next term.

:::

:::{admonition} Task 3
:class: exercise


Use your code from the previous exercise to write a function, `plot_iterates(f, x, n)`, that plots the first `n` terms of the sequence of iterates evaluated at `x`. Use `plt.plot(a, ".")` where `a` is the terms of your sequence. Remember to label the axes of your plots (use `plt.xlabel("$n$")` and `plt.ylabel("$f_n(x)$")`).

:::

:::{admonition} Task 4a
:class: exercise


Use your code from the previous exercises to study the sequences of iterates of $f(x)=x^2-1$ for the fixed input of `x in [1 + i / 10 for i in range(1, 8)]` and describe your results.

:::

:::{admonition} Task 4b
:class: exercise


Further explore the sequence from the previous exercise for different positive values of `x` and make a conjecture of what the largest value `x` can take such that this sequence of iterates is bounded.

:::

:::{admonition} Task 4c
:class: exercise


Further explore the sequence from the previous exercise for different negative values of `x` and make a conjecture of what the smallest value `x` can take such that this sequence of iterates is bounded.

:::

:::{admonition} Task 5
:class: exercise


A fixed point of a function, $f$, is some input, $x$, such that $f(x)=x$. Find all fixed points of $f(x)=x^2-1$. How does the sequence of iterates of `f` behave if we take the initial input, $x$, to be a fixed point of $f$? With this new information, modify your conjectures from the previous exercises (if necessary).

:::

## Complex Numbers


In the problems above, we observed that there appears to be an interval $I$ on the real line with the property that for all $x \in I$, $\{f^n(x)\}$ remains bounded and for all $x \notin I$, $\{f^n(x)\}$ is unbounded. The endpoints of this interval are interesting numbers, but the problem is just one-dimensional and so not really that interesting. If we extend this idea to the complex plane, then we can get far more interesting sets. First, we make a few comments about complex numbers and graphing.

A *complex number* is an object of the form $a + bi$ where $a,b\in \mathbb{R}$ and $i^2 = -1$. If $b = 0$, then $a + bi$ is real. We often identify the complex number $a+bi$ with the ordered pair $(a,b)$ and plot it the same way we plot a point in $\mathbb{R}^2$. We then often refer to the $xy$-plane as the  *complex plane*, the $x$-axis as the *real axis* and the $y$-axis as the *imaginary axis*. For example, $2 + 3i$ is plotted as $(2,3)$. We let $\mathbb{C} = \{a + bi: a,b \in \mathbb{R}\}$ be the set of all complex numbers and we consider functions $f : \mathbb{C} \to \mathbb{C}$.  We often write the domain variable as $z=x+iy$. Thus the function defined by $f(z) = z^2$ takes as input a complex number and returns its square.  You should check that $f(2)=4$, $f(2i)=-4$, and $f(1+i)=2i$. One can extend the definitions of continuity, differentiability, and integrability to functions of a complex variable.  The branch of mathematics concerned with these ideas is *complex analysis*.

When graphing a function $f: \mathbb{R} \to \mathbb{R}$, we consider the $x$-axis to represent the domain and the $y$-axis to represent the codomain. However, for functions $f: \mathbb{C} \to \mathbb{C}$, the domain and codomain are best represented by a plane instead of a line. Thus, we can't plot graphs of complex functions in the same way that we plot graphs of real functions because it would require $4$ dimensions. We often use other tricks to discover information about complex functions, such as using colors to tell us how near the output is to $0$, plotting only the real or the imaginary part of the output, or only plotting the values that satisfy certain criteria, as we will do below.

To extend the idea of iterates to the complex plane, we introduce the *Mandelbrot set*. For any $c=a+bi \in \mathbb{C}$, consider $f_c: \mathbb{C} \to \mathbb{C}$ defined by $f_c(z) = z^2 + c$. Then the Mandelbrot set is the set of all $c \in \mathbb{C}$ for which the sequence $\{f_c(0), f_c^2(0), f_c^3(0), \ldots\}$ is bounded in absolute value, where the absolute value of a complex number is its distance from $0$. In other words, the Mandelbrot set is the set of all complex $c$ such that the iterates of $f_c$ are bounded in absolute value for $z = 0$. You have probably seen this set before; it is very beautiful and the boundary is a fractal curve.

Then, we will define the related *Julia set*. Once again, we will let $f_c(z) = z^2 + c$, but in this case we will fix $c \in \mathbb{C}$. Then the filled Julia set for this $c$ is the set of all $z \in \mathbb{C}$ such that $\{f_c(z), f_c^2(z), f_c^3(z), \dots\}$ is bounded in absolute value. The Julia set for this $c$ is the boundary of the filled Julia set.

:::{admonition} Task 6
:class: exercise



Use [this online tool](https://marksmath.org/visualization/julia2.html) to explore Julia sets for different values of $c$. On the left is the Mandelbrot set. Select a point somewhere in the plane on the left side of the screen, whether within the Mandelbrot set (the black region) or outside of it (the gray and white regions). On the right, the Julia set for that $c$ will be drawn. You can then select a point $z$ on the right side of the screen and it will show the sequence $\{f_c(z), f_c^2(z), f_c^3(z), \dots\}$. Choose a point within the Julia set (this is easier to do if you choose a $c$ within the Mandelbrot set) and observe where the values of the sequence $\{f_c(z), f_c^2(z), f_c^3(z), \dots\}$ are. Now choose a point outside the Julia set. Comment on which sequences appear to be bounded in absolute value and which do not. Press the clear button, and keep playing around with this tool and see what beautiful Julia sets you can create!

:::
