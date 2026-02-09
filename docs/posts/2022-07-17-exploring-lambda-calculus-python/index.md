# Exploring the Lambda Calculus with Python
Matt Hodges
2022-07-17

![](lambda-calculus-python.jpeg)

This post is adapted from a Jupyter [Notebook found on
GitHub](https://github.com/hodgesmr/python_lambda_calculus).

This post explores some basic ideas of the Lambda Calculus, and how to
use it to implement a computation system with it. We will define numbers
and operators from scratch, and use that to implement the `square_sum`
function.

If you’re new to the Lambda Calculus, or functional programming in
general, you may wish to start with some of these resources:

- [David Beazley’s Lambda Calculus from the Ground Up - PyCon
  2019](https://www.youtube.com/watch?v=pkCLMl0e_0k)
  - If you’re someone who learns well by watching and listening, I
    highly recommend that you watch this talk. A significant portion of
    the concepts below come from watching this talk more than once.
- [Ben Eater’s Making a computer Turing
  complete](https://www.youtube.com/watch?v=AqNDk_UJW4k)
- [Lambda Calculus \|
  Wikipedia](https://en.wikipedia.org/wiki/Lambda_calculus)
- [Currying \| Wikipedia](https://en.wikipedia.org/wiki/Currying)

This post assumes you are fairly familiar with Python and Python’s
[lambda
expressions](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions).

### Rules of Our System

The Lambda Calculus asserts that any computational system can be
implemented with a set of three simple rules:

- You can define variables
- You can define single-argument functions
- You can call single-argument functions

That’s it. **No numbers. No operators. No control flow. No data
structures.**

I find it fascinating that with these very minimal concepts, the Lambda
Calculus asserts that we can create a fully functional computer! This
is, of course, a very minimal explanation of the rules of the Lambda
Calculus, and I invite you to consult the references above for more
information and formal definitions!

### The Challenge

Using the rules described above, we want to create a system that can
calculate the square-sum of any inputs. Again, we *only* have
single-argument functions. That means we have no integers, no addition,
and no multiplication. We’re going to have to create those using nothing
but single-argument functions that accept single-argument functions as
input and can only return single-argument functions.

For reference, consider the `square_sum` function, that may be written
in Python as:

``` python
def square_sum(a, b):
    return (a*a) + (b*b)


square_sum(5, 2)
```

    29

#### Currying

As previously mentioned, our computation system requires that we can
only create functions and those functions must accept one and only one
argument. This may seem like a limiting requirement, but let’s take a
look at what we can do with the idea of
[Currying](https://en.wikipedia.org/wiki/Currying) — a method for
transforming multi-argument functions into a chain of single-argument
functions. This allows us to re-write our Python implementation as:

``` python
def square_sum(a):
    def inner(b):
        return (a*a) + (b*b)
    return inner


square_sum(5)(2)
```

    29

In our curried version above, `square_sum` accepts the first argument,
`a` and returns a function that accepts the second argument, `b`. We can
then call that returned `inner` function to complete our calculation.
Currying is a fundamental strategy for computation in the Lambda
Calculus.

### Our Basic Building Block

Unless you’re already familiary with the Lambda Calculus, or you’re a
veteran of functional programming, you’re probaby very accustomed to
computing by operating on *state*. You have data structures, or numbers,
or bits, and you operate on them and then you persist new data
structures, or numbers, or bits.

Our concept of integers is a perfect example. As children, we learned
that the concept of `3` can be represented by holding up three fingers
on our hand, and seeing all three of them, and pointing to them. The
Lambda Calculus asks us to adjust that concept away from *state* and
towards *behavior*. Instead of holding up three fingers, what if we held
up *one finger three times*. It may be harder for us see that idea of
`3`, but it is a representation of `3` nonetheless.

Sit with this idea of behavior representing integers, because behavior
will be how we represent *everything*. And in our system, functions are
behavior. Our function could be the act of holding up a finger, pressing
a button, or anything else we need it to be.

Let’s use that metaphor of pressing a button. The button press is our
behavior, and behaviors are functions. And arguments are functions. And
we can only return functions. So, let’s write that:

``` python
def button_press(f):
    def g(x):
        return f(x)
    return g
```

Not much to see here yet. In fact, our system isn’t designed to *see*
anything. It’s designed to do computations within a given set of rules.

We’re designing a system of computation, and we can think about this
system like instruction that run on a CPU. But we’re humans, and it’s
helpful for us to be able to see the results of our computation in ways
that we can understand. So, we’re going to introduce an external system
that is *not* within the Lambda Calculus, but can interface with it.
Think of this as a peripheral like a printer. It’s not used to *do* any
of our computation. It can do special things that our CPU can’t do, and
it’ll connect to our system as a function, because our system can only
work with functions.

Let’s pretend our system has a printer attached that can only print the
`*` character. We’ll interface with it via an `emit` function.

Here is our not-of-our-system `emit` function:

``` python
def emit(func):
    def asterisk(x):
        return f'{x}*'
    return func(asterisk)('')
```

This is kindof strange. Our external `emit` function takes in some
function and has an inner asterisk-generating function. Let’s hook it up
to our `button_press` function:

``` python
emit(button_press)
```

    '*'

What just happened here? We call our `emit` function (external from our
system) by passing in our `button_press` function (internal to our
system). We did it one time, and it yielded a single `*`. Again, this is
just a convenience interface so that we can see what’s going on, and
isn’t necessary to do any of our actual computation.

### Numbers

Above we began to describe how functions, or behaviors, can represent
numbers. A single call to `button_press` yielded some concept of `1`.
What if we didn’t think about it as one call to `button_press` anymore,
but as the idea of *one behavior*:

``` python
def ONE(f):
    def g(x):
        return f(x)
    return g

emit(ONE)
```

    '*'

If you’ve made it this far, you’re probably thinking, “Hey, Python has a
way to represent single-argument functions, and they’re called
*lambdas*!” Let’s start using that instead of the expanded
`button_press` function:

``` python
ONE = lambda f : lambda x : f(x)

emit(ONE)
```

    '*'

Cool. So we know how to represent the concept of `1` using only
single-argument functions. We can represent `2` by calling our function
twice, because in our system numbers are behaviors:

``` python
TWO = lambda f : lambda x: f(f(x))

emit(TWO)
```

    '**'

This is all well and good, but we’re not really going to try to
implement every single number are we? That wouldn’t make a very good
computer. How can we represent all countable numbers?

If you look closely at our definitions above, `ONE` is a single call to
`f()`, while `TWO` is `f(f())`. This means that if we’re at any given
number, we can get to the next number by calling `f()` again. We can
define an `INCREMENT()` function to do just that. I find it helpful to
start by looking at this through the expanded Python functions first:

``` python
def ONE(f):  # f is the behavior we want to do
    def g(x):  # x is the curried second argument
        return f(x)
    return g


def INCREMENT(n):  # n is the concept of the number we already have
    def g(f):  # f is the behavior we want to do
        def h(x):  # x is the curried second argument
            return f(n(f)(x))  # we call f() again on our n(f)(x)
        return h
    return g


emit(INCREMENT(ONE))
```

    '**'

Spend some time stepping through the above code to understand it. We’re
essentially wrapping nested functions as many times as we need to get to
the next number. Once you’ve wrapped your head around it, see that we
can re-write the above as lambdas:

``` python
ONE = lambda f : lambda x : f(x)

INCREMENT = lambda n : lambda f : lambda x : f(n(f)(x))

TWO = INCREMENT(ONE)  # our calculated TWO from ONE

emit(TWO)
```

    '**'

If we can calculate `TWO` from `ONE`, we can calculate `THREE`:

``` python
THREE = INCREMENT(TWO)

emit(THREE)
```

    '***'

Pretty neat! We can keep doing this to infinity, either by saving
values, or calculating them on the fly! But you may be wondering, what
about `ZERO`? Well, we’ve defined `ONE` as a single call to any behavior
`f()`, so `ZERO` would simply be no calls to that behavior:

``` python
ZERO = lambda f : lambda x : x

emit(ZERO)
```

    ''

See how `ZERO` doesn’t call `f()` at all? What’s fun here is that we no
longer need to have defined `ONE`, we can calculate it from `ZERO`!

``` python
ONE = INCREMENT(ZERO)

emit(ONE)
```

    '*'

### Operators

Now that we know we can represent numbers as function calls, let’s start
working on math operators. We’ve already introduced one critical
operator, `INCREMENT`, and we can use that to introduce others. Let’s
start with `ADD`. Addition is can be thought of as incrementing `M`
times on a number `N`. For example, `2 + 3` could be described as
incrementing 2, three times. Before we attempt to implement that in our
system, let’s look again to how we would Curry this in Python:

``` python
def add(a):
    def inner(b):
        return a + b
    return inner

add(2)(3)
```

    5

``` python
def ADD(a):  # Our first number, which is always a function
    def inner(b):  # Our second number, which is always a function
        return b(INCREMENT)(a)  # Increment a, b times
    return inner


FIVE = ADD(TWO)(THREE)
emit(FIVE)
```

    '*****'

Since *everything* is *always* a function, our numbers can be used not
only as representations of calculations, but also as executors. Here’s
our `ADD` as a lambda:

``` python
ADD = lambda a : lambda b: b(INCREMENT)(a)

FIVE = ADD(TWO)(THREE)
emit(FIVE)
```

    '*****'

The last missing operator of our computational system multiplication.
Multiplication should feel a lot like nested functions you see often in
programming.

``` python
def MULT(a):  # Our first number, which is always a function
    def outer(b):  # Our second number, which is always a function
        def inner(f):  # The function we want to do a*b times
            return b(a(f))  # do f, a times, and do that b times
        return inner
    return outer

SIX = MULT(TWO)(THREE)
emit(SIX)
```

    '******'

Again, we can represent `MULT` as a lambda:

``` python
MULT = lambda a : lambda b : lambda f : b(a(f))

SIX = MULT(TWO)(THREE)
emit(SIX)
```

    '******'

### Using Our Computer

We’ve now defined everything necessary to implement our `square_sum`
function in the Lambda Calculus. Let’s build it here from these basic
principles. We want to calculate `square_sum(5, 2)`.

``` python
ZERO = lambda f : lambda x : x
INCREMENT = lambda n : lambda f : lambda x : f(n(f)(x))
ADD = lambda a : lambda b: b(INCREMENT)(a)
MULT = lambda a : lambda b : lambda f : b(a(f))

square_sum = lambda a : lambda b : ADD(MULT(a)(a))(MULT(b)(b))

TWO = ADD(INCREMENT(ZERO))(INCREMENT(ZERO))
FIVE = INCREMENT(ADD(TWO)(TWO))

RESULT = square_sum(FIVE)(TWO)
```

And that’s it! Using nothing but single-argument lambda functions, we’ve
successfully defined non-negative integers, the addition and
multiplication operators, and the square-sum function. It’s a little
hard to visualize, but the actual answer *is* calcuated in our `RESULT`
variable. We can output it to our metaphorical printer:

``` python
emit(RESULT)
```

    '*****************************'

Our printer has output 29 asterisks! Pretty cool!

### What’s Next?

Our system barely scratches the surface, but you can continue to
implement more operators, comparators, control flow, and everything else
you might need for a full computer. I highly recommend consulting the
references at the top of the post for further reading!

### License

    Copyright (c) 2022, Matt Hodges
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

    * Neither the name of Exploring the Lambda Calculus with Python nor the names of its
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
