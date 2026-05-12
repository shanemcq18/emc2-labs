# Lab 20: Approximate Integration


In our chapter on integration, we focused mainly on the theory.  We defined upper and lower sums and defined a function as integrable if the supremum of the lower sums equals the infimum of the upper sums. We also (thankfully) proved a number of results that allow us to evaluate integrals without explicitly computing this supremum of the lower sums. Of course the most important of these is the Fundamental Theorem of Calculus, which allows us to compute integrals by finding antiderivatives. Alas, many important functions do not have elementary antiderivatives and many others have antiderivatives that are hard to find. Thus it is important to have numerical procedures for approximating integrals. In this lab you will write code for the most basic algorithms for approximate integration and compare their results.

A word on hypotheses: Algorithms for approximate integration can only be expected to work on integrable functions. If a function is continuous on a closed and bounded interval, it is integrable. Less well-behaved functions can also be integrable, such as bounded monotone functions or bounded functions which are continuous except on a set of measure zero. Before you use any numerical techniques to approximate an integral, verify that your function is in fact integrable. All the functions considered in this lab are integrable.

## Two Simple Methods

Let $f$ be an integrable function on the closed interval $[a,b]$.  The two simplest ways to approximate an integral are the *left endpoint rule* and the *right endpoint rule*. For both of these methods, we begin by dividing the interval of integration $[a,b]$ into $n$ subintervals of equal length. For the left endpoint approximation $L_n$, we approximate $\int_a^b f(x) \, dx$ by a Riemann sum using as sample points the left endpoints of the intervals. Similarly for the right endpoint approximation $R_n$, we use as sample points the right endpoints of the subintervals.


## Task 1a
Write a function `left_riemann_sum(f, a, b, n)` that take as parameters a function `f`, the lower bound `a` and upper bound `b` for the interval of integration $[a,b]$, and an integer `n` for the number of subintervals, and returns the left endpoint approximation to $\int_a^b f(x)\, dx$.

## Task 1b

Write a function `right_riemann_sum(f, a, b, n)` that take as parameters a function `f`, the lower bound `a` and upper bound `b` for the interval of integration $[a,b]$, and an integer `n` for the number of subintervals, and returns the right endpoint approximation to $\int_a^b f(x)\, dx$.

## Two Improvements

The *midpoint rule* and the *trapezoid rule* are about as easy to use as the left endpoint and right endpoint rules but they have the advantage of increased accuracy. Furthermore, in the case in which the function being integrated is at least twice continuously differentiable, they come with associated error bound formulas that can further help us pin down the value of the integral.

As above, begin with an integrable function $f$ on the closed interval $[a,b]$. Subdivide the interval into $n$ subintervals of equal length.  For the midpoint approximation $M_n$, use as the sample points in the Riemann sum the midpoint of each interval. For the trapezoid approximation $T_n$, take the average of the left-enpoint approximation $L_n$ and the right-endpoint approximation $R_n$.

## Task 2

Write a function `trapezoid_sum(f, a, b, n)` that take as parameters a function `f`, the lower bound `a` and upper bound `b` for the interval of integration `[a,b]`, and an integer `n` for the number of subintervals and returns the trapezoid approximation to $\int_a^b f(x)\, dx$.

## Task 3

Write a function `midpoint_sum(f, a, b, n)` that take as parameters a function `f`, the lower bound `a` and upper bound `b` for the interval of integration `[a,b]`, and an integer `n` for the number of subintervals and returns the midpoint approximation to $\int_a^b f(x)\, dx.$

## Simpson's Rule

The approximation strategies discussed so far are similar in that they all essentially replace the function we wish to integrate with a piece-wise linear (often actually piece-wise constant) function.  One could image other schemes of approximating a function by simpler functions. *Simpson's rule* uses the fact that through any three points on the graph of a function, there is a unique function of degree at most two whose graph also passes through these points.

Let $f$ be an integrable function on the interval $[a,b]$. *For* $n$ *even*,  subdivide the interval $[a,b]$ into $n$ subintervals $[x_{i-1},x_i]$ of equal length.  Now take *pairs* of consecutive intervals $[x_{i-1},x_i]$ and $[x_i,x_{i+1}]$ and approximate $f$ on this pair of intervals by a quadratic function passing through $(x_{i-1},f(x_{i-1}))$, $(x_i,f(x_i))$, and $(x_{i+1},f(x_{i+1}))$.  By integrating this quadratic function, we find that $\int_a^b f(x) \,dx$ can be approximated by

```{math}
S_n=\frac{1}{3}\cdot \frac{b-a}{n}[f(x_0)+4f(x_1)+2f(x_2)+4f(x_3)+\ldots +2f(x_{n-2})+4f(x_{n-1})+f(x_n)].
```
It is a good idea to go through the derivation of this formula at least once in your life. See [Section 7.7 of Stewart](https://www.stewartcalculus.com/data/default/upfiles/09631_ApproximateIntegration_ptg1_hr_stu_001-022.pdf).

## Task 4

Write the formula for `S_n` in summation notation.
*Hint*: one can view $S_n$ as a sum of terms of the form $y_{2j-2}+4y_{2j-1}+y_{2j}.$

Write a function `simpsons_rule_sum(f, a, b, n)` that takes as parameters a function `f`, the lower bound `a` and upper bound `b` for the interval of integration $[a,b]$, and an integer `n` for the number of subintervals and returns the Simpson's rule approximation to $\int_a^b f(x)\, dx$. Raise a `ValueError` if `n` is not even (use `f"n {(n)} must be even"`)

## Error Bound Formulas

For the midpoint rule, the trapezoid rule, and Simpson's rule, there are formulas that give an upper bound on the error associated with using the method to approximate $\int_a^b f(x)\,dx$.  These formulas are in terms of the length of the interval, the number $n$ of subintervals used, and a bound on the absolute value of some derivative of $f$ on $[a,b]$. (Thus you should only use these formulas when $f$ has the appropriate number of derivatives.)

Suppose that $E_M$, $E_T$, and $E_S$ are the errors for the midpoint rule, trapezoid rule, and Simpson's rule, respectively.

First, that $\left\vert f''(x) \right\vert \leq K$ for $a \leq x \leq b$. Then we have the following bounds for the errors for the midpoint and trapezoid rules.

For the midpoint rule:

```{math}
|E_M|\leq \frac{K(b-a)^3}{24 n^2}.
```
For the trapezoid rule:

```{math}
|E_T|\leq \frac{K(b-a)^3}{12 n^2}.
```
Now suppose that $\left\vert f^{(4)}(x) \right\vert \leq K$ for $a \leq x \leq b$. Then we have the following bound for the error for Simpson's rule.

```{math}
|E_S|\leq \frac{K(b-a)^5}{180 n^4}.
```
## Task 5a

Use the trapezoid error bound formula to find an error bound on the trapezoid approximation of the integral of `f = lambda x: np.exp(-x ** 2)` on `[0, 0.5]` for `10` sub-intervals. Take `K` as the maximum of `|f''|` on `[0, 0.5]` (which is an integer in this case). Write your answer as a fraction in simplest terms. Format your answer EXACTLY as follows: `numerator` / `denominator`.


## Task 5b

Use the midpoint error bound formula to find an error bound on the midpoint approximation of the integral of `f = lambda x: np.exp(-x ** 2)` on `[0, 0.5]` for `10` sub-intervals. Take `K` as the maximum of `|f''|` on `[0, 0.5]` (which is an integer in this case). Write your answer as a fraction in simplest terms. Format your answer EXACTLY as follows: `numerator` / `denominator`.


## Task 5c

Use the Simpon's error bound formula to find an error bound on Simpon's approximation of the integral of `f = lambda x: np.exp(-x ** 2)` on `[0, 0.5]` for `10` sub-intervals. Take `K` as the maximum of `|f''''|` on `[0, 0.5]` (which is an integer in this case). Write your answer as a fraction in simplest terms. Format your answer EXACTLY as follows: `numerator` / `denominator`.


## Task 6


The true value of $\int_1^5 \frac{1}{x} \,dx$ is $\ln 5$. Use all five approximation methods to approximate the integral with $n=10$. For each method, compute the true error. For the midpoint, trapezoid, and Simpson's rules, check that the error bounds are larger than the absolute value of the true error.
