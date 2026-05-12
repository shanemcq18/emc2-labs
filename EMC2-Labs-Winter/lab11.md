# Lab 11: Root Finding and Newton's Method

Solving equations is an important practical problem. Much of high school algebra is aimed at developing techniques for accomplishing this task. However, solving equations is hard.  Although there are some useful results like the quadratic formula and analogous formulas for solving cubic and quartic equations, it is a famous fact that no corresponding quintic formula can exist. Thus if we want to solve real problems, we will need efficient algorithms for approximating solutions to equations.

This lab is by no means a thorough introduction to root-finding. Instead, it discusses two very simple ideas and explores their limitations. It is also designed to reinforce the ideas discussed in the text related to continuous and differentiable functions.

## Root-Finding by the IVT


If you were trying to find a solution to

```{math}
f(x):=x^5+2x^3-x-1=0,
```
and if you only had access to a scientific calculator, you might proceed as follows:

Clearly $f(0)<0$ and $f(1)>0$.

Because $f$ is continuous, by the Intermediate Value Theorem (IVT), there exists some solution in the interval $(0,1)=(a_0,b_0)$. Consider $x_1=0.5$ (the midpoint of $[0,1]$). We find that $f(0.5)=-1.21875$. Set $a_1=0.5$ and $b_1=1$.  Then $f(a_1) < 0$ and $f(b_1)>0$, so again by the IVT, there is some solution in $[a_1,b_1]$.

Repeat the process; at the $n$-th step, the input to the process is the interval $[a_{n-1}, b_{n-1}]$ and $f$ is known to have opposite signs at the endpoints.  Let $x_n$ be the midpoint of the interval. Find $f(x_n)$. If $f(x_n)=0$, return $x_n$ as a root. If $f(x_n) \neq 0$, either set $a_n=a_{n-1}$ and $b_n=x_n$ if $f(a_{n-1})$ and $f(x_n)$ have opposite sign or set $a_n=x_n$ and $b_n=b_{n-1}$ if $f(x_n)$ and $f(b_{n-1})$ have opposite sign.

Unless the process terminates because an exact solution has been found, the process produces two sequences ${a_n}$ and ${b_n}$ that both converge to a solution of the equation, and we can stop the process when $n$ is large enough that $b_n-a_n$ is less than the degree of accuracy we desire in our approximation of the solution.

## Task 1

Write a function, `ivt_ex(tol, maxiter)`, that solves `-1 - x + 2 * x ** 3 + x ** 5 = 0` in the domain `(0, 1)` within an error of `tol` (defaulting to `1e-8`) using a maximum of `maxiter` iterations (defaulting to `100`). Return both the root and whether your code met the error condition within `maxiter` iterations. The error condition is met when you find a value of `x` where `|-1 - x + 2 * x ** 3 + x ** 5| < tol`.

## Task 2a

Write a function `make_poly(coef_list)` that takes a list of coefficients in increasing degree-order as an input and returns a function for the polynomial defined by those coefficients.

## Task 2b

Write a function `find_interval(f)` which takes a function, `f` as input and returns a tuple, `(a, b)`, representing an interval, `[a, b]`, on which the polynomial changes sign (meaning that `f(a)<0<f(b)` or `f(a)>0>f(b)`. Do not worry about checking for functions that do not change sign globally as we will guarantee that all inputs to this function will do so in a later exercise.

To help you think about how to find such an interval, try the following: fix an initial value for `M` (e.g. `M=1`) and test the endpoints of the interval `[-M,M]`. If $f$ changes sign, you're done. If not, replace `M` with `2*M` and repeat.

## Task 2c

Every polynomial of odd degree has at least one real root. (Why?)
Adapt your code from Task 1, using your code from Tasks 2a and 2b, to write a function, `ivt_poly(coef_list, tol, maxiter)`, that finds a root of the polynomial defined by `coef_list` within an error of `tol` (defaulting to `1e-8`) using a maximum of `maxiter` iterations (defaulting to `100`). Return both the root and whether your code met the error condition within maxiter iterations.


To test your code:

1. The real roots of $1-2 x+3 x^2-4 x^3-5x^4+6x^5$ are approximately $-0.963448, 0.545323, 1.15814$
2. The real roots of $-0.1 - x + 1000 x^2 + 10000 x^3 + 0.1 x^4 + x^5$ are approximately $-0.1, -0.01, 0.01$


## Newton's Method

The idea of Newton's method is simple: Suppose $f$ is differentiable and suppose we want to solve $f(x)=0$. Start with a "guess" $x_0$ for the solution. Form the tangent line approximation to the graph of $y=f(x)$ at $(x_0,f(x_0))$.  Then our improved guess for the solution is the $x$-intercept of the tangent line, which we call $x_1$.  Repeat this process so that the input at step $n$ is the output $x_{n-1}$ from the previous step and the output is $x_n$, the $x$-intercept of the tangent line to the graph of $y=f(x)$ at $(x_{n-1}, f(x_{n-1}))$.


## Task 3

Write a function, `newton(f, df, x0, tol, maxiter)`, that a takes a differentiable function, `f`, its derivative, `df`, an initial guess, `x0`, an error condition, `tol` (defaulting to `1e-8`), and a maximum number of iterations, `maxiter`, as inputs and uses Newton's method to approximate the solution to `f(x) = 0` within an error of `tol` using a maximum of `maxiter` iterations. Return both the solution and whether it met the error condition with `maxiter` iterations. You will need to do some algebra to write a recursive formula for $x_{n + 1}$ in terms of $x_{n}$.


There is a solution to $\sin(x^2)+x^2-x-1=0$ between $-1$ and $0$.  Use Newton's method to find it.


## Task 4

When an equation has multiple solutions, which one Newton's method finds depends on the choice of $x_0$.
Consider $x^3+0.1x^2-x-0.2=0$. Make a graph. (Revisit {doc}`lab02` if you need a refresher on how to do this.) How many solutions do you see? Find initial conditions that work to find each solution and obtain approximations to these solutions. Are there any initial conditions that will not work to find any solution?
