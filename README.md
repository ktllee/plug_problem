# Plug Problem

See [here](https://www.cs.umb.edu/~eb/plugs/) for more information.

This puzzle was inspired by the question ["Number of ways to arrange pairs of integers with distance constraint"](http://math.stackexchange.com/questions/4124452/number-of-ways-to-arrange-pairs-of-integers-with-distance-constraint) on StackExchange Math.

## Definitions

**In Progress**

## Organization

### Directories

[`solutions`](/solutions) contains lists of solutions for different set of plugs.

[`pseudocode`](/pseudocode) contains pseudocode and general brainstorming.

[`unused`](/unused) contains code that has been integrated into active code and which no longer need be used.

### Active Scripts

`original_plugs.py` is code to brute-force solutions with all distinct plugs (no repeats), where plugs are defined by number of prongs and gaps between prongs (and all gaps are equal).  **Stable. Soon to be superseeded.**

`recursive_solver.py` is code to recursively solve for valid arrangements of any given list of Plugs.  **In Progress.**

`plug_class.py` contains the Plug class.  **Active.**

`strip_class.py` contains the Strip class. **In Progress.**