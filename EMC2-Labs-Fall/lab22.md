# Lab 22: The Lean Theorem Prover Part I

From the Lean Theorem Prover community website:
> A proof assistant is a piece of software that provides a language for defining objects, specifying properties of these objects, and proving that these specifications hold. The system checks that these proofs are correct down to their logical foundation.
>
> These tools are often used to verify the correctness of programs. But they can also be used for abstract mathematics.... In a formalization, all definitions are precisely specified and all proofs are virtually guaranteed to be correct.
In this lab, we will get a sense of how a theorem prover works by proving basic properties of the natural numbers in the interactive theorem prover Lean.
Visit

<https://adam.math.hhu.de/#/g/leanprover-community/nng4>

Start by reading the instructions on the left-hand side of the page, under "Welcome to the Natural Number Game."

## Successor Function

In order to rigorously define the natural numbers through the Lean theorem prover, we start with two concepts: the number $0$, and the **successor function** on a natural number $n$, $s(n)$.
Think of $s(n)$ as the number that comes “after” $n$, whatever that means.

Note that we haven’t defined addition yet (we don’t even know what the numbers are!) so $s(n)$ doesn’t mean $n$ “plus” $1$.
Yet. Informally (but less informally than before), we will define the natural numbers as the
set containing $0$, the successor $s(0)$, the successor $s(s(0))$, the successor $s(s(s(0)))$, etc. This
leads to two axioms used for constructing the natural numbers.

* **Axiom 1:** $0$ is a natural number.
* **Axiom 2:** If $n$ is a natural number, then $s(0)$ is a natural number.

By Axioms 1 and 2, we see that $s(s(s(s(s(s(s(0)))))))$ is a natural number. Don’t worry, we won’t write numbers like this; instead we’ll use the
notation we’re all familiar with. So the number above is called $7$. But for now, the symbol
$7$ means nothing other than a shorthand notation for the successor of the successor of the
successor of the successor of the successor of the successor of the successor of $0$.

It may seem like this is enough to define the natural numbers, but through this lab (and the subsequent Lean Lab), we will see that we need a few more axioms.

## Task 1

Complete every level from each of the following worlds:

#. Tutorial World
#. Addition World
#. Multiplication World

In the next 290 lab, ({doc}`lab24`), you will complete worlds 4-6.
