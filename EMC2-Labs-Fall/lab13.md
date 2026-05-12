# Lab 13: Linear Transformations

Linear transformations are at the heart of linear algebra and its applications. For example, they define how geometric shapes in $\mathbb{R}^n$ stretch, rotate, reflect, and shear.
In this lab, we explore the geometric power of linear transformations and how matrix multiplication implements them computationally.

## Linear Transformations

A *linear transformation* is a mapping between vector spaces that preserves vector addition and scalar multiplication.
More precisely, let $V$ and $W$ be vector spaces over $\mathbb{R}^n$.
A map $L:V\rightarrow W$ is a linear transformation from $V$ into $W$ if
$L(a \mathbf{x}_1 + b \mathbf{x}_2) = a L \mathbf{x}_1 + b L \mathbf{x}_2$ for all vectors $\mathbf{x}_1, \mathbf{x}_2 \in V$ and scalars $a, b \in \mathbb{R}$.

Every linear transformation $L$ from an $n$-dimensional vector space into an $m$-dimensional vector space can be represented by an $m \times n$ matrix $A$, called the *matrix representation* of $L$.
To apply $L$ to a vector $\mathbf{x}$, left multiply by its matrix representation.
This results in a new vector $\mathbf{x}'$, where each component is some linear combination of the elements of $\mathbf{x}$.
For linear transformations from $\mathbb{R}^2$ to $\mathbb{R}^2$, this process has the form

```{math}
A \mathbf{x} =
\left[\begin{array}{cc}
a & b \\
c & d \\
\end{array}\right]
\left[\begin{array}{c}
x \\
y
\end{array}\right]
=
\left[\begin{array}{cc}
a x + b y \\
c x + d y
\end{array}\right]
=
\left[\begin{array}{cc}
x' \\
y'
\end{array}\right]
= \mathbf{x}'.
```
```{image} _static/turtle1.png
:align: center
:width: 40%
```
Linear transformations can be interpreted geometrically.
To demonstrate this, consider an array of points $T$ that collectively form the picture of the BYU Turtle above.
The coordinate pairs $\mathbf{x}_i$ are organized by column, so the array has two rows: one for $x$-coordinates, and one for $y$-coordinates.
Matrix multiplication on the left transforms each coordinate pair, resulting in another matrix $T'$ whose columns are the transformed coordinate pairs:

```{math}
A T = A \left[\begin{array}{cccc}
x_1 & x_2 & x_3 & \ldots \\
y_1 & y_2 & y_3 & \ldots
\end{array}\right]
=
A \left[\begin{array}{c|c|c|c}
 & & & \\
\mathbf{x}_1 & \mathbf{x}_2 & \mathbf{x}_3 & \ldots \\
 & & & 
\end{array}\right]
=
\left[\begin{array}{c|c|c|c}
 & & & \\
A \mathbf{x}_1 & A \mathbf{x}_2 & A \mathbf{x}_3 & \ldots \\
 & & &
\end{array}\right] \\
 =
\left[\begin{array}{c|c|c|c}
 & & & \\
\mathbf{x}_1' & \mathbf{x}_2' & \mathbf{x}_3' & \ldots \\
 & & &
\end{array}\right]
=
\left[\begin{array}{cccc}
x_1' & x_2' & x_3' & \ldots \\
y_1' & y_2' & y_3' & \ldots
\end{array}\right]
= T'.
```
### Types of Linear Transformations

Linear transformations from $\mathbb{R}^2$ into $\mathbb{R}^2$ can be classified in a few ways.

- **Stretch**: Stretches or compresses the vector along each axis.
> The matrix representation is diagonal:
>
> ```{math}
> \left[\begin{array}{rr}
> a & 0  \\
> 0 & b
> \end{array}\right].
> ```
> If $a=b$, the transformation is called a *dilation*.
- **Shear**: Slants the vector by a scalar factor horizontally or vertically (or both simultaneously).
> The matrix representation is
>
> ```{math}
> \left[\begin{array}{cc}
> 1 & a \\
> b & 1
> \end{array}\right].
> ```
> Pure horizontal shears ($b = 0$) skew the $x$-coordinate of the vector while pure vertical shears ($a = 0$) skew the $y$-coordinate.
- **Reflection**: Reflects the vector about a line that passes through the origin.
> The reflection about the line spanned by the vector $[a, b]^\mathrm{T}$ has the matrix representation
>
> ```{math}
> \frac{1}{a^2 + b^2}
> \left[\begin{array}{cc}
> a^2 - b^2 & 2 a b \\
> 2 a b       & b^2 - a^2
> \end{array}\right].
> ```
- **Rotation**: Rotates the vector around the origin.
> A counterclockwise rotation of $\theta$ radians has the following matrix representation:
>
> ```{math}
> \left[\begin{array}{rr}
> \cos\theta & -\sin\theta \\
> \sin\theta &  \cos\theta
> \end{array}\right]
> ```
> A negative value of $\theta$ performs a clockwise rotation.
> Choosing $\theta = \frac{\pi}{2}$ produces a rotation of 90 degrees counterclockwise.
> Below is an example of each of these linear transformations.
```{image} _static/6turtles.png
:align: center
```
## Task 1

Write a function for each type of linear transformation.
(`stretch(X, a, b)`, `shear(X, a, b)`, `reflection(X, a, b)`, `rotation(X, theta)`).
Each function should accept an array to transform and the scalars that define the transformation ($a$ and $b$ for stretch, shear, and reflection, and `theta` for rotation).
Construct the matrix representation, multiply it with the input array, and return a transformation of the data.
Make sure to copy the array before transforming it.

### Compositions of Linear Transformations

Let $V$, $W$, and $Z$ be finite-dimensional vector spaces.
If $L:V\rightarrow W$ and $K:W\rightarrow Z$ are linear transformations with matrix representations $A$ and $B$, respectively, then the *composition* function $K L:V\rightarrow Z$ is also a linear transformation, and its matrix representation is the matrix product $B A$.

For example, if $S$ is a matrix representing a shear and $R$ is a matrix representing a rotation, then $R S$ represents a shear followed by a rotation.
In fact, any linear transformation $L:\mathbb{R}^2 \rightarrow\mathbb{R}^2$ can be written as a composition of the four transformations.


## Affine Transformations

All linear transformations map the origin to itself, since for any $\mathbf{x} \not= 0$ we have $L(0) = L(0 \mathbf{x}) = 0 L(\mathbf{x}) = 0$ for any linear transformation $L$.
An *affine transformation* is a mapping between vector spaces that preserves the relationships between points and lines, but may not preserve the origin.
Every affine transformation $T$ can be represented by a matrix $A$ and a vector $\mathbf{b}$.
To apply $T$ to a vector $\mathbf{x}$, calculate $A \mathbf{x} + \mathbf{b}$.
If $\mathbf{b} = 0$ then the transformation is a linear transformation, and if $A = I$ but $\mathbf{b} \neq 0$ then it is called a *translation**.

For example, if $T$ is the translation with $b = [\frac{3}{4}, \frac{1}{2}]^\mathrm{T}$, then applying $T$ to an image will shift it right by $\frac{3}{4}$ and up by $\frac{1}{2}$.

```{image} _static/2turtles.png
:align: center
:width: 80%
```
Affine transformations include all compositions of stretches, shears, rotations, reflections, and translations.
For example, if $S$ represents a shear and $R$ a rotation, and if $\mathbf{b}$ is a vector, then $R S \mathbf{x} + \mathbf{b}$ shears, then rotates, then translates $\mathbf{x}$.

## Task 2

Write a function `translation(X, b)` that takes in an array `X` and the vector `b` for the translation.
The function should return the translation of the data.


## Linear Transformations in 3-D

In the same way that linear transformations from $\mathbb{R}^2$ to $\mathbb{R}^2$ can be represented by $2 \times 2$ matrices, linear transformations from $\mathbb{R}^3$ to $\mathbb{R}^3$ can be represented by $3 \times 3$ matrices.
For this part of the lab we will be using data points from the [Global Hawk aircraft](https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Global%20Hawk).

```{image} _static/Global_Hawk.png
:align: center
:width: 60%
```
This is what the data points look like plotted with 50,000 points in 3-D.

```{image} _static/plane_normal.png
:align: center
```
We will simply deal with rotation transformations in $\mathbb{R}^3$.
While in 2-D we could only rotate on the X-Y plane, in 3-D we can rotate on the X-Y plane, the Y-Z plane, and the X-Z plane making 3 different rotations.
With all 3 of these rotations, we can achieve any rotation in 3-D.
Here is what the 3 different rotations look like.

```{image} _static/rotations2.png
:align: center
:width: 50%
```
Below are the matrix representations for each of these 3 kinds of rotations in $\mathbb{R}^3$:

- **X-Y plane rotation**:

```{math}
\left[\begin{array}{ccc}
\cos\theta & -\sin\theta & 0 \\
\sin\theta & \cos\theta & 0 \\
0 & 0 & 1
\end{array}\right]
```
- **Y-Z plane rotation**:

```{math}
\left[\begin{array}{ccc}
1 & 0 & 0 \\
0 & \cos\theta & -\sin\theta \\
0 & \sin\theta & \cos\theta
\end{array}\right]
```
- **X-Z plane rotation**:

```{math}
\left[\begin{array}{ccc}
\cos\theta & 0 & -\sin\theta \\
0 & 1 & 0 \\
\sin\theta & 0 & \cos\theta
\end{array}\right]
```
Below is an example of each of the 3 rotations.

```{image} _static/plane_normal_rotations.png
:align: center
:width: 100%
```
## Task 3

Write a function for each 3-D rotation
(`rotate_xy(X, theta)`, `rotate_yz(X, theta)`, `rotate_xz(X, theta)`).
Each function should accept an array to transform and the angle $\theta$ for the rotation.
Construct the matrix representation, multiply it with the input array, and return a transformation of the data.
Make sure to copy the array before transforming it.

## Task 4

Take the data points from the Global Hawk aircraft and apply a combination of these 3 rotations so that the plane faces in the direction of the vector `[7, -5, -1]` and save it to the variable `X_rotated`.
Assume the plane is already facing in the direction of the vector `[1, 0, 0]`.
Remember that `cos(theta) = u*v / ||u||*||v||`.
Make sure to round both theta values to 2 decimal places to avoid rounding errors using `round(theta, 2)`.
(The data will be in the file `plane.csv`.)
