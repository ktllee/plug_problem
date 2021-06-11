# Plug Problem

See [here](https://www.cs.umb.edu/~eb/plugs/) for more information.

This puzzle was inspired by the question ["Number of ways to arrange pairs of integers with distance constraint"](http://math.stackexchange.com/questions/4124452/number-of-ways-to-arrange-pairs-of-integers-with-distance-constraint) on StackExchange Math.

## Organization

### Directories

[`solutions`](/solutions) contains lists of solutions for different set of plugs.

[`unused`](/unused) contains code that has been integrated into active code and which no longer need be used.

### Scripts

`original_plugs.py` is code to brute-force solutions with all distinct plugs (no repeats), where plugs are defined by number of prongs and gaps between prongs (and all gaps are equal).

`plug_class.py` contains the classes for plugs/strips to allow for more flexible future codes.  **In Progress.**