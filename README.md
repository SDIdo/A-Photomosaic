# A-Photomosaic
Intro to CS assignment in Python

This program runs a photomosaic on a given images by several tiles image like
that cover it, creating it by combining their own photo-data together
according to the algorithm:
It does so by comparing the color values of each pixel of a certain area
of the image, to every pixel of the more probable tiles to find the most 
appropriate one. Beforehand the program creates a list of the more probable
tiles that could be appropriate to fit a certain part of the original image.
This is done by listing all the average color values of all the tiles
and comparing them to the average color value of a certain part of the 
original image. comparing is done according to a distance fomula.
User can choose which image to photomosaic and where to save it, user
can also choose tiles height and number of tiles to be checked - 
num_candidates.
To run this program please type in these parameters at the command prompt:
ex6.py <image_source> <images_dir> <output_name> <tile_height>
<num_candidates>
