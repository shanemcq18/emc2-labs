# Lab 24: Basins of Attraction

In {doc}`lab11` you were first introduced to Newton's method.
When there is only one solution to an equation, then for almost every initial condition we will be able to find this solution.
However, if there is more than one solution, the solution that we find is dependent on our choice of a starting point $x_0$.
For example, the function $f(x)=x^2-1$ has zeros at $-1$ and $1$.
If $x_0<0$, then Newton's method converges to $-1$; if $x_0 > 0$ then it converges to $1$.

```{figure} _static/figures/Basins-1.png
:width: 45%
:align: center

Basins of attraction for $f(x) = x^2 - 1$

```
The regions $(-\infty, 0)$ and $(0, \infty)$ are called the *basins of attraction* of $f$.
Starting in one basin of attraction leads to finding one zero, while starting in another basin yields a different zero. In this lab, we will write code to graph the basins of attraction for a given function. This lab is an ACME lab with more explanation added where necessary.

The basins of attraction for $f(x) = x^2 - 1$ are very straightforward, but the basins of attraction for polynomials of degree at least $3$ are more interesting. We can see in the figure below that the basis of attraction for the zeros $-1$ (in blue) and $1$ (in green) are disconnected but share a kind of symmetry.



```{figure} _static/figures/Basins-2.png
:width: 45%
:align: center

Basins of attraction for `f(x) = x^3 - x`


```
So far we have performed Newton's method on functions from $\mathbb R$ to $\mathbb R$.
However, the same algorithm also works on functions from $\mathbb C$ to $\mathbb C$, and we may similarly find basins of attraction.
In the complex case, the basins of attraction are now $2$ dimensional regions in the complex plane instead of sections on a line, so the graphs of the basins of attraction can be both interesting and beautiful.
Recall from Lab {doc}`lab21` that every complex number $c$ can be written as $c = a + bi$ where $a,b$ are real numbers.
We can plot $c$ in a plane (the complex plane) by taking the $x$-coordinate to be the real part of $c$ (which is $a$) and taking the $y$-coordinate to the be imaginary part of $c$ (which is $b$).

To construct a plot of the basins of attraction for a complex function, we are going to use the `numpy` library.
In all the example code given below, we will assume that `numpy` was imported as `np`.
We can easily construct a real plane with $x$- and $y$-axes with the following code:

```python
x = np.linspace(-1.5, 1.5, 500)
y = x.copy()
X, Y = np.meshgrid(x, y)
```
Generally, we could then create an output list (usually `Z` as a function of `X` and `Y`) and plot all three `X`, `Y`, `Z` as a heatmap, contour plot, or 3D plot.
However, a complex function is a function of a single complex variable and not two real variables, even though we often think of those as equivalent.
Thus we will use `linspace` and `meshgrid` to construct `X_real` and `X_imag` and combine these to create a grid of complex points.
In the following example, the imaginary unit $i = \sqrt{-1}$ is instead written as `j` in Python.
*Note*: Generally in Python you must always write a multiplication sign `*` between any number and variable, but in the case of `j` you do not. In fact, you must always have a number attached to `j` otherwise it will be assumed to be a variable.

```python
x_real = np.linspace(-1.5, 1.5, 500)  # Real parts.
x_imag = np.linspace(-1.5, 1.5, 500)  # Imaginary parts.
X_real, X_imag = np.meshgrid(x_real, x_imag)
X_0 = X_real + 1j*X_imag              # Combine real and imaginary parts.
```
Now we have one variable `X_0` which contains a `500 x 500` grid of complex numbers as opposed to two variables  `X` and `Y` which together make a grid of tuples of real numbers.
We can calculate using this grid in exactly the same way that we could with the grid of `X` and `Y`.
If we have some $f: \mathbb C \to \mathbb C$, we may compute an output grid by writing `Z = f(X_0)`.


:::{admonition} Task 1
:class: exercise


Write a function, `comspace(a, b, c, d, n, m, axes)`, that uses `np.linspace` and `np.meshgrid` to create an array of complex numbers distributed uniformly on `{x + 1j * y: a <= x <= b, c <= y <= d}` with `n` terms on the real axis and `m` terms on the imaginary axis. Also, accept a boolean value `axes` that returns the axis grids (the outputs of `np.meshgrid`) when `True`.

:::

:::{admonition} Task 2a
:class: exercise


Write a function, `newton(f, df, x0, tol, maxiter)`, that implements Newton's method and returns the solution only. If you have completed {doc}`lab11`, you are welcome to reuse that implementation of Newton's Method.

:::

:::{admonition} Task 2b
:class: exercise


Vectorize your implementation of `newton(f, df, x0, tol, maxiter)` by adding `@np.vectorize(excluded={0, 1, 3, 4, "f", "df", "tol", "maxiter"})` to the line directly above the function declaration. This allows your function to properly handle vector inputs.


:::

## Basins of Attraction


If we repeat this, we can create many grids `X_1`, `X_2`, `X_3`, and so on until we have `k` iterations. After enough iterations, the `(i,j)` th element of `X_k` will be very near to one of the zeros of `f`, which means that using the `(i,j)` th element of `X_0` as a starting point for Newton's method will converge to that zero. The zeros of $f(x) = x^3 - 1$ are $1$, $-\frac{1}{2} + \frac{\sqrt{3}}{2} i$, and $-\frac{1}{2} - \frac{\sqrt{3}}{2} i$, where the last two zeros are complex. Performing Newton's method for this function, `(i,j)` th element of `X_k` will be close to one of these zeros. We can then assign a value `0`, `1`, or `2` to each element of `X_k` depending on which zero it is closest to and save these values into a new array `Y`.

We then have an array `Y` where all the elements are `0`, `1` or `2`. Plotting this array with each number corresponding to a different color gives us a plot of the basins of attraction.

```{figure} _static/figures/Basins-Complex.png
:width: 45%
:align: center

Basins of attraction for $f(x) = x^3 - 1$

```
```{figure} _static/figures/Basins-Complex-2.png
:width: 45%
:align: center

Basins of attraction for $f(x) = x^3 - x$



```
:::{admonition} Note
Notice that in some portions of the first figure, whenever red and blue try to come together, a patch of green appears between. This behavior repeats on an infinitely small scale, producing a fractal. Because it arises from Newton's method, this kind of fractal is called a *Newton fractal*.

Newton fractals show that the long-term behavior of Newton's method is *extremely* sensitive to the initial guess $x_0$. Changing $x_0$ by a small amount can change the output of Newton's method in a seemingly random way. This phenomenon is called *chaos* in mathematics.
:::
:::{admonition} Task 3
:class: exercise


Write a function, `basins(f, df, X, zeros)`, that finds the basins of attraction for `X` by running Newton's method on `X` for `f, df` and finding the indices of the zeros that are closest to the output.

Hint: Consider using `np.abs` and `np.argmin` (with `axis=0`) and `np.expand_dims` to ensure array broadcasting functions properly.


:::

:::{admonition} Task 4a
:class: exercise


Using all the functions you have made so far, write a function, `plot_basins(f, df, zeros, bounds, res)`, that plots the basins of attraction, using `plt.pcolormesh` (with `cmap="brg"`), of `f` applied to the complex region defined by `bounds` and `res` where `bounds` is a tuple containing `(a, b, c, d)` and `res` is the number of points to generate for each axis.


:::

:::{admonition} Task 4b
:class: exercise


Use your code from the previous exercise to visualize the basins of attraction for `f = lambda x: x ** 3 - 1` on `{x + yi: -1.5 <= x, y <= 1.5}` with `res=500`.

:::

:::{admonition} Task 4c
:class: exercise


Use your code from the previous exercise to visualize the basins of attraction for `f = lambda x: x ** 3 - x` on `{x + yi: -1.5 <= x, y <= 1.5}` with `res=500`.

:::

:::{admonition} Task 4d
:class: exercise


Use your code to plot the Newton fractal (basins of attraction) for a function of your choice.

If you wish to use functions that are not polynomials, make sure to use NumPy's version of the function instead of the `math` library's. For example, use `np.sin` instead of `math.sin` since the first will work for complex numbers and the second will not. You are welcome to use online calculators to compute the zeros of complex functions. Change the domain variables `[r_min, r_max, i_min, i_max]` so that all the zeros of the function `f` are within the domain of the plot.

:::
