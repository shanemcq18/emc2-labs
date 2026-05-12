# Lab 19: Plotting Vector Valued Functions

In this lab you will create visualizations to help you understand vector fields. Before beginning the lab, please review how to create quiver plots in python.


<http://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.15-Quiver-and-Stream-Plots/>


A quiver plot is a plot that shows vectors as arrows and is especially useful when talking about vector fields.

To practice, plot the vector field $\mathbf F(x,y) = (y^2 - 2xy)\mathbf i + (3xy-6x^2)\mathbf j$. This won't be graded.

:::{admonition} Task 1a
:class: exercise


Write a function, `plot_vfield_2d(F, xa, xb, ya, yb, dx, dy, title)`, that plots the vector field for a vector-valued function, `F`, on the domain `[xa, xb] X [ya, yb]` with step sizes `dx` and `dy`. Recall that the tails of your vectors are the inputs to `F` and the tips of your vectors are the outputs from `F`. Be sure to set the aspect ratio of the plot to `"equal"` and to set the display bounds to `[xa - dx, xb + dx] X [ya - dy, yb + dy]` using `plt.axis([xa - dx, xb + dx, ya - dy, yb + dy])` and to set the title to `title` if provided. Do NOT change any other properties of the plot.

:::

:::{admonition} Task 1b
:class: exercise


Use your code from the previous exercise to visualize $\mathbf F(x) = (r^2 - 2r)\mathbf x$, where $\mathbf x = \langle x,y \rangle$ and $r = |\mathbf x|$. In NumPy, this might be written as `F = lambda x: np.linalg.norm(x, axis=0) * (np.linalg.norm(x, axis=0) - 2) * x`. Visualize this function on `[-1,1] X [-1,1]` with step sizes of `0.1` and `0.1`.

:::

:::{admonition} Task 1c
:class: exercise


Use your code from the previous exercise to visualize `F = lambda x: np.linalg.norm(x, axis=0) * (np.linalg.norm(x, axis=0) - 2) * x` on `[-5,5] X [-5,5]` with step sizes of `0.5` and `0.5`.


:::
## Gradient Vector Fields

In the next few tasks, we will plot the gradient vector field of $f$ together with a contour map of $f$ for:

- $f(x,y) = \ln(1+x^2+2y^2)$

- $f(x,y) = \cos x - 2 \sin y$



:::{admonition} Task 2a
:class: exercise


Write a function, `plot_sfield_2d(f, Df, xa, xb, ya, yb, dx, dy, title)`, that plots the scalar field for a two-dimensional, scalar-valued function, `f`, using a contour plot and plots the vector field of its gradient, `Df`, on top on the domain `[xa, xb] X [ya, yb]` with step sizes `dx` and `dy`. Be sure to set the aspect ratio of the plot to `"equal"` and to set the display bounds to `[xa - dx, xb + dx] X [ya - dy, yb + dy]` using `plt.axis([xa - dx, xb + dx, ya - dy, yb + dy])` and to set the title to `title` if provided and display the colorbar (using `plt.colorbar(ax)`). Do NOT change any other properties of the plot.

:::

:::{admonition} Task 2b
:class: exercise


Use your code from the previous exercise to visualize `f = lambda x: np.log(1 + x[0] ** 2 + 2 * x[1] ** 2)` and `Df = lambda x: 2 * np.array([x[0], 2 * x[1]]) / (1 + x[0] ** 2 + 2 * x[1] ** 2)` on `[-5,5] X [-5,5]` with step sizes of `0.5` and `0.5` and `16` levels.


:::

:::{admonition} Task 2c
:class: exercise


Use your code from the previous exercise to visualize `f = lambda x: np.cos(x[0]) - 2 * np.sin(x[1])` and `Df = lambda x: -np.array([np.sin(x[0]), 2 * np.cos(x[1])])` on `[-5,5] X [-5,5]` with step sizes of `0.5` and `0.5` and `16` levels.



:::
## Vector Fields in Higher Dimensions

Of course there are also vector fields in higher dimensions. See <http://matplotlib.org/3.1.1/gallery/mplot3d/quiver3d.html>

In the following tasks, we will plot these vector fields:

- $\mathbf F(x,y,z) = \mathbf i + 2\mathbf j + 3 \mathbf k$

- $\mathbf F(x,y,z) = \mathbf i + 2\mathbf j + z \mathbf k$

- $\mathbf F(x,y,z) = x\mathbf i + y\mathbf j + z \mathbf k$

- $\mathbf F(x,y,z) = \sin y\mathbf i + (x\cos y + \cos z)\mathbf j - y \sin z \mathbf k$


:::{admonition} Task 3a
:class: exercise


Write a function, `plot_vfield_3d(F, xa, xb, ya, yb, za, zb, dx, dy, dz, length, title)`, that plots the vector field for a vector-valued function, `F`, on the domain `[xa, xb] X [ya, yb] X [za, zb]` with step sizes `dx`, `dy`, and `dz` and a forced arrow length, `length` (set `normalize=True`). Recall that the tails of your vectors are the inputs to `F` and the tips of your vectors are the outputs from `F`. Be sure to set the aspect ratio of the plot to `"equal"` and to set the display bounds to `[xa - dx, xb + dx] X [ya - dy, yb + dy] X [za - dz, zb + dz]` using `plt.axis([xa - dx, xb + dx, ya - dy, yb + dy, za - dz, zb + dz])` and to set the title to `title` if provided. Use `plt.subplot(111, projection="3d")` to create a 3d plot in CodeBuddy. Do NOT change any other properties of the plot.

:::

:::{admonition} Task 3b
:class: exercise


Use your code from the previous exercise to visualize `F = lambda x: np.array([1, 2, 3])` on `[-1,1] X [-1,1] X [-1, 1]` with step sizes of `0.4`, `0.4`, and `0.4` and an arrow length of `0.2`.

:::

:::{admonition} Task 3c
:class: exercise


Use your code from the previous exercise to visualize `F = lambda x: np.array([np.ones_like(x[0]), 2 * np.ones_like(x[1]), x[2]])` on `[-1,1] X [-1,1] X [-1, 1]` with step sizes of `0.4`, `0.4`, and `0.4` and an arrow length of `0.2`.

:::

:::{admonition} Task 3d
:class: exercise


Use your code from the previous exercise to visualize `F = lambda x: x` on `[-1,1] X [-1,1] X [-1, 1]` with step sizes of `0.4`, `0.4`, and `0.4` and an arrow length of `0.2`.

:::

:::{admonition} Task 3e
:class: exercise


Use your code from the previous exercise to visualize `F = lambda x: np.array([np.sin(x[1]), x[0] * np.cos(x[1]) + np.cos(x[2]), -x[1] * np.sin(x[2])])` with step sizes of `0.4`, `0.4`, and `0.4` and an arrow length of `0.2`.

:::
