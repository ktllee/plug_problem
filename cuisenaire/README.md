Code supporting brute-force exploration of trains composed of Cuisenaire rods.  Scripts generally floating around are the most recent iterations of code intended to find certain kinds of rod sets or similar.

## Directories

[`Ethan`](\Ethan) contains older code written by Ethan, which all works together and is known to work.

[`trees`](\trees) contains the scripts for a Shiny app that displays trees based on rod set input by the user.

## Scripts

`brute.py` contains functions that, as it sounds, brute-force certain problems.  Based on Rodset class in `rods.py`.

`cuisenaire.py` is an old script that combines Ethan's work with Katie's work.

`minimals.py` is a one-off script to find certain kinds of rodsets from a large set of data (created using the `multi` function in `brute.py`).

`rods.py` contains the Rodset class.