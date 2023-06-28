# Plug Problem

See [here](https://www.cs.umb.edu/~eb/plugs/) for more information.

This puzzle was inspired by the question ["Number of ways to arrange pairs of integers with distance constraint"](http://math.stackexchange.com/questions/4124452/number-of-ways-to-arrange-pairs-of-integers-with-distance-constraint) on StackExchange Math.

Note that most of the research/exploration is currently focused on trains of Cuisenaire rods.  Code relating to that research is in the [`cuisenaire`](/cuisenaire) directory.

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

## Directories

[`cuisenaire`](/cuisenaire) contains code related to research into trains of Cuisenaire rods (equivalent to plugs completely full of prongs).

[`other`](/other) contains one-off side projects.

[`plugs`](/plugs) contains code related to research into pronged plugs, as described above.

[`pseudocode`](/pseudocode) contains pseudocode and general brainstorming.

[`solutions`](/solutions) contains lists of solutions for different set of plugs.

[`unused`](/unused) contains code that has been integrated into active code and which no longer need be used.
