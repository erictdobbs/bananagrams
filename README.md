Bananagrams
===========                                       

bananagrams.py is a single-player implementation of the tile-based word game. 

Setup and Requirements
----------------------

This program requires Python 2.7 (free download at http://www.python.org) and pygame (free download at http://www.pygame.org). It was created for version 1.9.1 of pygame, but may work with newer versions. Once those are installed, you can launch this program with the command 

    python bananagrams.py

once you navigate to the directory that you've downloaded the file to.

How To Play
-----------

The object of Banagrams is to arrange all the provided letters into a single crossword made up of English words. Once the tiles are in a valid arrangement, you can draw another tile, then try to rearrange the puzzle to fit it. 

Controls
--------

I've left in some of the debugging keys, but the following covers everything you'll need to actually play: 

<dl>
  <dt>Left-click</dt>
  <dd>Click a letter tile to pick it up. Click again to place it on a blank tile.</dd>
  <dt>Space</dt>
  <dd>When you have the board arranged in a valid crossword, press space to draw another letter. If an invalid word is detected, the offending tiles will flash.</dd>
</dl>