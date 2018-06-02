######################################################
# FILE: ex6.py
# WRITER: Ido Natan
# EXERCISE: EX6 intro2cs2
# DESCRIPTION: a program that creates a photomosaic
######################################################
import sys
import mosaic as mos
import copy

BIGGEST_DIST_BTWN_PIXS = 765
INIT_NUM = 0
ZERO_DIST = 0
EMPTY_SPACE = ''
ONE_CANDIDATE = 1
STARTING_SENTRY = -1
RED_PART = 0
GREEN_PART = 1
BLUE_PART = 2

def biggest_dimention_detector(tiles):
    tile_row = STARTING_SENTRY
    tile_col = STARTING_SENTRY
    for i in range(len(tiles)):
        if tile_row <= len(tiles[i]):
            tile_row = len(tiles[i])
            for j in range(len(tiles[i])):
                if tile_col <= len(tiles[i][j]):
                    tile_col = len(tiles[i][j])
                    biggest_dimention_possible = tile_row*tile_col
        return biggest_dimention_possible


def compare_pixel(pixel1, pixel2):
    """finds a numerical distance between the color values of two pixels.
    :param pixel1: 1st tuple containing 3 color levels of red, green and blue
    :param pixel2: 2nd tuple containing 3 color levels of red, green and blue
    *color levels: each color is valued between 0-255
    Returns a number that represents the distance between the color values"""
    redDist = abs(pixel1[RED_PART]-pixel2[RED_PART])
    greenDist = abs(pixel1[GREEN_PART]-pixel2[GREEN_PART])
    blueDist = abs(pixel1[BLUE_PART]-pixel2[BLUE_PART])
    pixDist = redDist + greenDist + blueDist
    return pixDist


def compare(image1, image2):
    """calculates distance between all congruent pixels of two images.
    :param image1: a list of lists contaning all the pixels of one image
    :param image2: a list of lists contaning all the pixels of a second image
    Returns a number that represents the difference between the color values
    of all the pixels from these two images"""
    imgDist = ZERO_DIST
    for i in range(min(len(image1),len(image2))):
        for j in range(min(len(image1[i]),len(image2[i]))):
            imgDist += compare_pixel(image1[i][j],image2[i][j])
    return imgDist      


def get_piece(image, upper_left, size):
    """collects a fragment or a piece that is within the image.
    :param image: a path for an image from which a piece is to be collected.
    :param upper_left: the coordinates of the desired piece
    :param size: the desired area from the fragment, a continuation from
    it's coordinates.
    Returns the collected piece"""
    cropped_image = []
    cropped_image_col = []
    for i in range(size[0]):
        for j in range(size[1]):
            if upper_left[0]+i < len(image):    #border check
                if upper_left[1]+j < len(image[i]):
                    piece = image[upper_left[0]+i][upper_left[1]+j]
                    cropped_image_col.append(piece)
                else:
                    continue
    cropped_image.append(cropped_image_col)
    return cropped_image


def set_piece(image, upper_left, piece):
    """sets a fragment or a piece on top of an image.
    :param image: a path for an image for which a piece is to be put on.
    :param upper_left: the coordinates of the desired setting place
    :param piece: a part of an image 
    Returns None"""
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if upper_left[0]+i < len(image):
                if upper_left[1]+j < len(image[i]):
                    image[upper_left[0]+i][upper_left[1]+j] = piece[i][j]
                else:
                    continue


def average(image):
    """calculates the average level of each of the colors red, green and blue
    creating the image.
    :param image: a path for an image
    Returns a tuple containing the average level values of red, green, blue"""
    redLevel, blueLevel, greenLevel  = INIT_NUM, INIT_NUM, INIT_NUM 
    redCount, blueCount, greenCount  = INIT_NUM, INIT_NUM, INIT_NUM
    for i in range(len(image)):
        for j in range(len(image[0])):
            redLevel += image[i][j][RED_PART]   #numerical value of the color
            redCount += 1   #counts up number of color pixels
            greenLevel += image[i][j][GREEN_PART]
            greenCount += 1
            blueLevel += image[i][j][BLUE_PART]
            blueCount += 1
    if redCount!=0: #zero division disablers
        redAvg = redLevel/redCount
    else:
        redAvg = 0
    if greenCount!=0:
        greenAvg = greenLevel/greenCount
    else:
        greenAvg = 0
    if blueCount!=0:
        blueAvg = blueLevel/blueCount
    else:
        blueAvg = 0
    imgAvg = redAvg, greenAvg, blueAvg
    return imgAvg
       
 
def preprocess_tiles(tiles):
    """inserts each of the average color level from each tile to a list
    whereas each index represents a different tile.
    :param tiles: a list of images
    Returns a list of tuples which hold average values of color levels
    for each tile"""
    lst_of_avgs =[]
    for tile in tiles:
        lst_of_avgs.append(tuple(average(tile)))
    return lst_of_avgs


def get_best_tiles(objective, tiles, averages , num_candidates):
    """function compares between the average pixel color value of
    the original images to the average color level of the tiles,
    and creates a list numbered by num_candidates, containing these tiles.
    :param objective: path to the original image
    :param tiles: path to the tiles desired to be put on the image
    :param averages: list of tuples containing average color levels
    of an input to the previous function.
    :param num_candidates: number of potential tiles matching function's need
    Returns a list of tiles in the length of num_candidates that are the 
    closest in their average color to the average color of the original image.
    """
    best_tiles_lst = []
    smallest_dist = BIGGEST_DIST_BTWN_PIXS*biggest_dimention_detector(tiles)
    obj_avg = average(objective)
    if num_candidates:
        for i in range(len(tiles)):
            new_dist = compare_pixel(averages[i],obj_avg)
            if smallest_dist >= new_dist:
                smallest_dist = new_dist
                best_tiles_lst.append(tiles[i])
                num_candidates -= ONE_CANDIDATE
    return best_tiles_lst


def choose_tile(piece, tiles):
    """function seeks the closest tile to a piece of the original image,
    colorwise.
    :param piece: a fragment from the original image that is desired to be
    replaced.
    :param tiles: list of tiles that are to be checked.
    Returns the tile that is the closest in it's colors to the fragment of
    the original image."""
    smallest_dist = BIGGEST_DIST_BTWN_PIXS*biggest_dimention_detector(tiles)
    for i in range(len(tiles)):
        new_dist = compare(piece, tiles[i])
        if smallest_dist >= new_dist:
            smallest_dist = new_dist
            bestIndex = i
    return tiles[bestIndex]
          
  
def make_mosaic(image, tiles, num_candidates):
    """function collects the most colorwise matching tile to a certain part
    of the original image, and puts it on that part enough times to
    cover the whole image with tiles.
    :param image: path to the original image, a list of lists.
    :param tiles: path to different little images, a list of lists.
    :param num_candidates: number of the most matching tiles.
    Returns a list of lists, the original image made from the tiles"""
    averages = preprocess_tiles(tiles)
    tile_width = len(tiles[0][0])
    tile_height = len(tiles[0])
    image_height = len(image)
    image_width = len(image[0])
    photomosaic = copy.deepcopy(image) #copying so that the ranges won't be
    #mixing together
    for i in range(0, image_height, tile_height):
        for j in range(0, image_width, tile_width):
            frag = get_piece(image, (i,j), (tile_height, tile_width))
            bTiles = get_best_tiles(frag, tiles, averages, num_candidates)
            choosen_tile = choose_tile(frag, bTiles)
            set_piece(photomosaic, (i,j), choosen_tile)
    return photomosaic
            
        
if len(sys.argv) != 6:
    print("Wrong number of parameters. The correct usage is:")
    print("ex6.py <image_source> <images_dir> <output_name>"
    "<tile_height> <num_candidates>")
else:
    image_source = sys.argv[0]
    images_dir = sys.argv[1]
    output_name = sys.argv[2]
    tile_height = sys.argv[3]
    num_cadidates = sys.argv[4]