# Plug Problem

See [here](https://www.cs.umb.edu/~eb/plugs/) for more information.

This puzzle was inspired by the question ["Number of ways to arrange pairs of integers with distance constraint"](http://math.stackexchange.com/questions/4124452/number-of-ways-to-arrange-pairs-of-integers-with-distance-constraint) on StackExchange Math.

## Current Definitions

+ Plug - an object with connected prongs and gaps, where prongs can take up spaces in a strip
	+ Plugs can be represented as:
		+ binary where prongs are '1' and gaps are '0' (e.g. '1011')
		+ base 10 equivalent to the binary representation (e.g. '1011' = 11)
	+ length - total length of the plug, counting end prongs
+ Strip - an object with slots for plugs to be fit into
	+ Strips can be represented as:
		+ an ordered list of all prongs in the strip, by the plug the prong belongs to (verbose)
		+ an ordered list of plugs, by the first occurence of a prong from that plug
	+ length - total length of the strip
	+ thickness - total number of plugs bridging a space between slots
+ Solutions are considered those arrangements of plugs that fill all slots of a given strip.


## Organization

### Directories

[`solutions`](/solutions) contains lists of solutions for different set of plugs.

[`pseudocode`](/pseudocode) contains pseudocode and general brainstorming.

[`unused`](/unused) contains code that has been integrated into active code and which no longer need be used.

### Active Scripts

`recursive_solver.py` is code to recursively solve for valid arrangements of any given list of Plugs.  **In Progress. Functional.**

`plug_class.py` contains the Plug class.  **Functional.**

`strip_class.py` contains the Strip class. **Functional.**