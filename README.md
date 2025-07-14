# Py-Katas

Katas in python

## Install

Recommend using [uv](https://docs.astral.sh/uv/) to run any scripts

## Table of Contents
- [Numeric Combinations](#numeric-combinations)
- [Collinear Points](#)

### Numeric Combinations
#### Description:

This is a problem of my own, that I received in 3rd grade, the assignment, was to find a sequence of numbers using the digits 9,8,7,6,5,4,3,2,1, in that order, using at minimum three `+` operations and at least one `-` operation, and as many `✕` and/or `÷` as you wish, to equal `100`.

After some time, the answer provided by the teacher was 98 - 76 + 54 + 3 + 21, she didn't explain how to solve it, or expand on the answer, just gave us 20 minutes to work on it, I suspect she had a hangover and wanted some quiet time, she was a terrible teacher (Ms. Stith, Mantua Elementary, Fairfax, VA). 

The problem stuck with me, because I wanted to find OTHER answers to this problem. So, in this project I've removed the operator constraints for the three `+` and one `-` that to find any and all permutations.

Additionally, I did not wish to limit to 987654321 and 100, so while that is the default settings, you can provide any digits and target number you wish. 

> _Fun fact:_
>
> `98-76+54+3+21` is the 53,017th combination of this problem of 69,190

#### Usage:
```sh
uv run numeric-combinations.py 987654321 100
```

#### Results:
Results are added to a file, with the digits provided and the target number separated by a `_` 

`uv run numeric-combinations.py 987654321 100` will write to `987654321_100.txt` which I've renamed and commited to this repo [here](987654321_100_result.txt).

### Collinear Points

#### Description:

A script to determine if a set of points are collinear (lie on the same straight line). The algorithm works by:

1. Taking the first two points to establish an initial slope
2. Checking if all subsequent points maintain the same slope relative to the first point
3. If any point deviates from this slope, the points are not collinear

The script accepts points as command line arguments or runs predefined examples when no arguments are provided.

#### Usage:

**Run with examples (no arguments):**
```sh
uv run collinear.py
```

**Check custom points:**
```sh
uv run collinear.py <x1> <y1> <x2> <y2> <x3> <y3> ...
```

**Examples:**
```sh
# Check if points (1,1), (2,2), (4,4), (-10,-10) are collinear
uv run collinear.py 1 1 2 2 4 4 -10 -10

# Check if points (1,0), (2,0), (3,1) are collinear  
uv run collinear.py 1 0 2 0 3 1
```

#### Output Format:
```
Points: [(x1, y1), (x2, y2), (x3, y3), ...]
Collinear: True/False
```