"""
File: util.py
Authors: Ahmed Aly & Brandon Ngacho
Date: 06 November 2022
Description: This file contains utility functions to aid in decoding images that have hidden information 
             in them, a concept known as steganography.
"""
import imageio
import numpy as np
import cv2 # pip install opencv-python  
import matplotlib.pyplot as plt
"""
_______________________________________________________________________________________________________________________
THE FOLLOWING METHODS READ BYTES FROM LEFT TO RIGHT THEN FROM TOP TO BOTTOM

""" 


"""Reads the first n bytes from the passed in image using LSB 
"""
def read_n_bytes_LSB(image, height, width, n):
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(chars) < n:
                # read the first LSB for each color channel                
                chars.append(str(image[r,c,0] & 1))
                chars.append(str(image[r,c,1] & 1))
                chars.append(str(image[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars


"""Reads the first n bytes from the passed in image using the two LSBs
"""
def read_n_bytes_2_LSB(image, height, width, n):
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(chars) < n:
                # read the first 2 LSBs for each color channel from highest to lowest
                
                # first color channel
                chars.append(str((image[r,c,0] & 2) >> 1))
                chars.append(str(image[r,c,0] & 1))
                
                # second color channel
                chars.append(str((image[r,c,1] & 2) >> 1))
                chars.append(str(image[r,c,1] & 1))
                
                # third color channel
                chars.append(str((image[r,c,2] & 2) >> 1))
                chars.append(str(image[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars


"""Reads the first n bytes from the passed in image using the two LSBs
"""
def read_n_bytes_3_LSB(image, height, width, n):
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(chars) < n:
                # read the first 3 LSBs for each color channel from highest to lowest
                
                # first color channel
                chars.append(str((image[r,c,0] & 4) >> 2))
                chars.append(str((image[r,c,0] & 2) >> 1))
                chars.append(str(image[r,c,0] & 1))
                
                # second color channel
                chars.append(str((image[r,c,1] & 4) >> 2))
                chars.append(str((image[r,c,1] & 2) >> 1))
                chars.append(str(image[r,c,1] & 1))
                
                # third color channel 
                chars.append(str((image[r,c,2] & 4) >> 2))
                chars.append(str((image[r,c,2] & 2) >> 1))
                chars.append(str(image[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars


""" EXPERIMENTAL: Reads n bytes from the image using lsbNum least significant bits from each color channel 
"""
def read_n_bytes_y_LSB(image, height, width, n, lsbNum, num_color_channels=3): 
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(chars) < n:
                # read the first 3 LSBs for each color channel from highest to lowest
                for i in range(num_color_channels):
                    for j in range(lsbNum):
                        chars.append(str((image[r,c,i] & (2**(lsbNum-j-1))) >> (lsbNum-j-1)))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars

def read_n_bytes_y_LSB_snake(image, height, width, n, lsbNum, num_color_channels=3):
    chars = []
    break_out_flag = False
    for r in range(height):
        if r % 2 == 0: # even row
            for c in range(width): # read left to right
                if len(chars) < n:
                    # read the first 3 LSBs for each color channel from highest to lowest
                    for i in range(num_color_channels):
                        for j in range(lsbNum):
                            chars.append(str((image[r,c,i] & (2**(lsbNum-j-1))) >> (lsbNum-j-1)))
                else: 
                    break_out_flag = True
                    break
        else: # odd row
            for c in range(width-1, -1, -1): # read right to left (reverse order)
                if len(chars) < n:
                    # read the first 3 LSBs for each color channel from highest to lowest
                    for i in range(num_color_channels):
                        for j in range(lsbNum):
                            chars.append(str((image[r,c,i] & (2**(lsbNum-j-1))) >> (lsbNum-j-1)))
                else: 
                    break_out_flag = True
                    break
        if break_out_flag:
            break
    return chars


"""
isolates n color channels and returns a matrix of the color channels independent of each other where a color channel is a 2D matrix of rows and columns
"""
def read_n_color_channels_individually(image, height, width, n=3):
    channels = []
    for i in range(n): # isolate each color channel
        channels.append(np.zeros((height, width))) # create a new channel for each color channel 
    for r in range(height): # iterate through each pixel
        for c in range(width): # iterate through each pixel
            for i in range(n): # isolate each color channel
                channels[i][r,c] = image[r,c,i] # add the pixel value to the channel
    return channels # return the list of color channels

"""

similar to read_n_color_channels_individually but instead of returning a matrix of color channels,
it returns a list of n lists where each of the n lists represent pixels in its respective color channel (rgb) 
"""
def read_n_color_channels_individually_as_bytes(image, height, width, n=3):
    channels = [] # list of color channels
    # create a list of n empty lists
    for i in range(n):
        channels.append([])
    for r in range(height): # iterate through each pixel
        for c in range(width): # iterate through each pixel
            for i in range(n): # isolate each color channel
                channels[i].append(image[r,c,i]) # add the pixel value to the channel

def read_n_color_channels_individually_snake(image, height, width, n=3):
    channels = []
    for i in range(n): # isolate each color channel
        channels.append(np.zeros((height, width))) # create a new channel for each color channel 
    for r in range(height): # iterate through each pixel
        if r % 2 == 0: # even row
            for c in range(width): # iterate through each pixel
                for i in range(n): # isolate each color channel
                    channels[i][r,c] = image[r,c,i] # add the pixel value to the channel
        else: # odd row
            for c in range(width-1, -1, -1): # iterate through each pixel (reverse order)
                for i in range(n): # isolate each color channel
                    channels[i][r,c] = image[r,c,i] # add the pixel value to the channel
    return channels # return the list of color channels

def read_n_color_channels_individually_as_bytes_snake(image, height, width, n=3):
    channels = [] # list of color channels
    # create a list of n empty lists
    for i in range(n):
        channels.append([])
    for r in range(height): # iterate through each pixel
        if r % 2 == 0: # even row
            for c in range(width): # iterate through each pixel
                for i in range(n): # isolate each color channel
                    channels[i].append(image[r,c,i]) # add the pixel value to the channel
        else: # odd row
            for c in range(width-1, -1, -1): # iterate through each pixel (reverse order)
                for i in range(n): # isolate each color channel
                    channels[i].append(image[r,c,i]) # add the pixel value to the channel
    


"""Assumes we can have n image headers encoded right after each other as in the following format:
        [header1][header2][header3]...[headerN] [contents1][contents2][contents3]...[contentsN]
"""
def read_n_image_headers(image, height, width, n):
    #create an array of tuples of the form (height, width) for each image
    headers = []
    for _ in range(n):
        #read the first 32 bits for the height
        #read the next 32 bits for the width
        #add the tuple to the array
        nBytes = read_n_bytes_LSB(image, height, width, 64*n) # read 64 bits for n image header
        temp = nBytes[:64] # get the first 64 bits
        nBytes = nBytes[64:] # remove the first 64 bits from the array
        headers.append((binaryToInt(temp[:32]), binaryToInt(temp[32:]))) # append the image header to headers array
    return headers

"""
    Method to try extract header from an image.
"""
def getImageHeaderFromMessage(img, height, width, header_size):
    image_metadata = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(image_metadata) < header_size:
                image_metadata.append(str(img[r,c,0] & 1))
                image_metadata.append(str(img[r,c,1] & 1))
                image_metadata.append(str(img[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
           
    image_metadata = ''.join(image_metadata)[0:header_size] 
    height, width = binaryToInt(image_metadata[:header_size//2]), binaryToInt(image_metadata[header_size//2:])
    return height, width   


"""
    Given a binary string, return an int
"""
def binaryToInt(binaryArray):
    return int(''.join(binaryArray), 2) 


"""
_______________________________________________________________________________________________________________________
THE FOLLOWING METHODS READ BYTES FROM UP TO DOWN THEN FROM LEFT TO RIGHT
"""

def read_n_bytes_LSB_UP_DOWN(image, height, width, n):
    chars = []
    break_out_flag = False
    for c in range(width):
        for r in range(height):
            if len(chars) < n:
                # read the first LSB for each color channel                
                chars.append(str(image[r,c,0] & 1))
                chars.append(str(image[r,c,1] & 1))
                chars.append(str(image[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars


def read_n_bytes_2_LSB_UP_DOWN(image, height, width, n):
    chars = []
    break_out_flag = False
    for c in range(width):
        for r in range(height):
            if len(chars) < n:
                # read the first 2 LSBs for each color channel from highest to lowest
                
                # first color channel
                chars.append(str((image[r,c,0] & 2) >> 1))
                chars.append(str(image[r,c,0] & 1))
                
                # second color channel
                chars.append(str((image[r,c,1] & 2) >> 1))
                chars.append(str(image[r,c,1] & 1))
                
                # third color channel
                chars.append(str((image[r,c,2] & 2) >> 1))
                chars.append(str(image[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars


def read_n_bytes_3_LSB_UP_DOWN(image, height, width, n):
    chars = []
    break_out_flag = False
    for c in range(width):
        for r in range(height):
            if len(chars) < n:
                # read the first 3 LSBs for each color channel from highest to lowest
                
                # first color channel
                chars.append(str((image[r,c,0] & 4) >> 2))
                chars.append(str((image[r,c,0] & 2) >> 1))
                chars.append(str(image[r,c,0] & 1))
                
                # second color channel
                chars.append(str((image[r,c,1] & 4) >> 2))
                chars.append(str((image[r,c,1] & 2) >> 1))
                chars.append(str(image[r,c,1] & 1))
                
                # third color channel 
                chars.append(str((image[r,c,2] & 4) >> 2))
                chars.append(str((image[r,c,2] & 2) >> 1))
                chars.append(str(image[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars


def read_n_bytes_4_LSB_UP_DOWN(image, height, width, n):
    chars = []
    break_out_flag = False
    for c in range(width):
        for r in range(height):
            if len(chars) < n:
                # read the first 3 LSBs for each color channel from highest to lowest
                
                # first color channel
                chars.append(str((image[r,c,0] & 8) >> 3))
                chars.append(str((image[r,c,0] & 4) >> 2))
                chars.append(str((image[r,c,0] & 2) >> 1))
                chars.append(str(image[r,c,0] & 1))
                
                # second color channel
                chars.append(str((image[r,c,1] & 8) >> 3))
                chars.append(str((image[r,c,1] & 4) >> 2))
                chars.append(str((image[r,c,1] & 2) >> 1))
                chars.append(str(image[r,c,1] & 1))
                
                # third color channel 
                chars.append(str((image[r,c,2] & 8) >> 3))
                chars.append(str((image[r,c,2] & 4) >> 2))
                chars.append(str((image[r,c,2] & 2) >> 1))
                chars.append(str(image[r,c,2] & 1))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars


""" EXPERIMENTAL: Reads n bytes from the image using lsbNum least significant bits from each color channel 
"""
def read_n_bytes_y_LSB_UP_DOWN(image, height, width, n, lsbNum, num_color_channels=3): 
    chars = []
    break_out_flag = False
    for c in range(width):
        for r in range(height):
            if len(chars) < n:
                # read the first 3 LSBs for each color channel from highest to lowest
                for i in range(num_color_channels):
                    for j in range(lsbNum):
                        chars.append(str((image[r,c,i] & (2**(lsbNum-j-1))) >> (lsbNum-j-1)))
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break
    return chars

"""
Reads n bytes from the image using lsbNum least significant bits from each color channel in 
a snake pattern(from up to down then down to up).
"""
def read_n_bytes_y_LSB_snake_UP_DOWN(image, height, width, n, lsbNum, num_color_channels=3): 
    chars = []
    break_out_flag = False
    # loop over the pixels in a snake pattern (up, down, up, down, etc.)
    for c in range(width):
        if c % 2 == 0: # odd columns go up to down
            for r in range(height):
                if len(chars) < n:
                    # read the first 3 LSBs for each color channel from highest to lowest
                    for i in range(num_color_channels):
                        for j in range(lsbNum):
                            chars.append(str((image[r,c,i] & (2**(lsbNum-j-1))) >> (lsbNum-j-1)))
                else: 
                    break_out_flag = True
                    break
        else: # odd columns go down to up
            for r in reversed(range(height)):
                if len(chars) < n:
                    # read the first 3 LSBs for each color channel from highest to lowest
                    for i in range(num_color_channels):
                        for j in range(lsbNum):
                            chars.append(str((image[r,c,i] & (2**(lsbNum-j-1))) >> (lsbNum-j-1)))
                else: 
                    break_out_flag = True
                    break
        if break_out_flag:
            break
    return chars        


"""
READS UP_DOWN isolates n color channels and returns a matrix of the color channels independent of each other where a color channel is a 2D matrix of rows and columns
"""
def read_n_color_channels_individually_UP_DOWN(image, height, width, n=3):
    channels = []
    for i in range(n): # isolate each color channel
        channels.append(np.zeros((height, width))) # create a new channel for each color channel 
    for c in range(width): # iterate through each pixel
        for r in range(height): # iterate through each pixel
            for i in range(n): # isolate each color channel
                channels[i][r,c] = image[r,c,i] # add the pixel value to the channel
    return channels # return the list of color channels


"""
READS UP_DOWN similar to read_n_color_channels_individually but instead of returning a matrix of color channels,
it returns a list of n lists where each of the n lists represent pixels in its respective color channel (rgb) 
"""
def read_n_color_channels_individually_as_bytes_UP_DOWN(image, height, width, n=3):
    channels = [] # list of color channels
    # create a list of n empty lists
    for i in range(n):
        channels.append([])
    for c in range(width): # iterate through each pixel
        for c in range(height): # iterate through each pixel
            for i in range(n): # isolate each color channel
                channels[i].append(image[r,c,i]) # add the pixel value to the channel


"""
READS UP_DOWN snake isolates n color channels and returns a matrix of the color channels independent of each other where a color channel is a 2D matrix of rows and columns
"""    
def read_n_color_channels_individually_UP_DOWN_snake(image, height, width, n=3):
    channels = []
    for i in range(n): # isolate each color channel
        channels.append(np.zeros((height, width))) # create a new channel for each color channel 
    for c in range(width): # iterate through each pixel
        if c % 2 == 0: # odd columns go up to down
            for r in range(height): # iterate through each pixel
                for i in range(n): # isolate each color channel
                    channels[i][r,c] = image[r,c,i] # add the pixel value to the channel
        else: # odd columns go down to up
            for r in reversed(range(height)): # iterate through each pixel
                for i in range(n): # isolate each color channel
                    channels[i][r,c] = image[r,c,i] # add the pixel value to the channel
    return channels # return the list of color channels


"""
READS up_down snake similar to read_n_color_channels_individually but instead of returning a matrix of color channels,
it returns a list of n lists where each of the n lists represent pixels in its respective color channel (rgb) 
"""
def read_n_color_channels_individually_as_bytes_UP_DOWN_snake(image, height, width, n=3):

    channels = [] # list of color channels
    # create a list of n empty lists
    for i in range(n):
        channels.append([])
    for c in range(width): # iterate through each pixel
        if c % 2 == 0: # odd columns go up to down
            for r in range(height): # iterate through each pixel
                for i in range(n): # isolate each color channel
                    channels[i].append(image[r,c,i]) # add the pixel value to the channel
        else: # odd columns go down to up
            for r in reversed(range(height)): # iterate through each pixel
                for i in range(n): # isolate each color channel
                    channels[i].append(image[r,c,i]) # add the pixel value to the channel
    

"""
_____________________________________________________________________________________________
STATISTICAL FUNCTIONS
"""

"""
EXPERIMENTAL: uses 2d discrete cosine transform to decode the image
"""
def dct_decode(image):
    
    # get the 2d discrete cosine transform of the image
    dct = cv2.dct(np.float32(image))
    
    # get the first n coefficients of the 2d dct
    dct = dct.flatten()
    
    # convert the coefficients to binary
    return [str(int(c)) for c in dct]

"""
____________________________________________________________________________________________________________________
VISUALIZATION TOOLS
"""

"""
Runs visual histograms to determine which pixels most likely have data hidden in them.
"""
def plot_histograms(image):
    # plot the image
    plt.imshow(image)
    plt.show()
    
    # plot the first color channel
    plt.imshow(image[:,:,0])
    plt.show()
    
    # plot the second color channel
    plt.imshow(image[:,:,1])
    plt.show()
    
    # plot the third color channel
    plt.imshow(image[:,:,2])
    plt.show()
    
    # plot the first color channel histogram
    plt.hist(image[:,:,0].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.show()
    
    # plot the second color channel histogram
    plt.hist(image[:,:,1].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.show()
    
    # plot the third color channel histogram
    plt.hist(image[:,:,2].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.show()
    
    # plot the first color channel histogram with a log scale
    plt.hist(image[:,:,0].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.yscale('log')
    plt.show()
    
    # plot the second color channel histogram with a log scale
    plt.hist(image[:,:,1].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.yscale('log')
    plt.show()
    
    # plot the third color channel histogram with a log scale
    plt.hist(image[:,:,2].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.yscale('log')
    plt.show()
    
    # plot the first color channel histogram with a log scale
    plt.hist(image[:,:,0].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()
    
    # plot the second color channel histogram with a log scale
    plt.hist(image[:,:,1].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()
    
    # plot the third color channel histogram with a log scale
    plt.hist(image[:,:,2].flatten(), bins=256, range=(0,256), fc='k', ec='k')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()
    
"""
plot the image accounting for different ranges of LSBs to see if there is a pattern of which LSBs are used
"""
def plot_LSBs(image, num_color_channels=3):
    # plot the first color channel
    plt.imshow(image[:,:,0])
    plt.show()
    
    # plot the second color channel
    plt.imshow(image[:,:,1])
    plt.show()
    
    # plot the third color channel
    plt.imshow(image[:,:,2])
    plt.show()
    
    # plot the first color channel LSBs
    for i in range(num_color_channels):
        for j in range(8):
            plt.imshow((image[:,:,i] & (2**(8-j-1))) >> (8-j-1))
            plt.show()
    
    # plot the second color channel LSBs
    for i in range(num_color_channels):
        for j in range(8):
            plt.imshow((image[:,:,i] & (2**(8-j-1))) >> (8-j-1))
            plt.show()
    
    # plot the third color channel LSBs
    for i in range(num_color_channels):
        for j in range(8):
            plt.imshow((image[:,:,i] & (2**(8-j-1))) >> (8-j-1))
            plt.show()

"""
plot lines over lsbs to see if there is a pattern of which LSBs are used
"""
def plot_LSB_lines(image, num_color_channels=3):
    # plot the first color channel
    plt.imshow(image[:,:,0])
    plt.show()
    
    # plot the second color channel
    plt.imshow(image[:,:,1])
    plt.show()
    
    # plot the third color channel
    plt.imshow(image[:,:,2])
    plt.show()
    
    # plot the first color channel LSBs
    for i in range(num_color_channels):
        for j in range(8):
            plt.imshow((image[:,:,i] & (2**(8-j-1))) >> (8-j-1))
            plt.axhline(0, color='r', linestyle='-', linewidth=1)
            plt.axhline(1, color='r', linestyle='-', linewidth=1)
            plt.show()
    
    # plot the second color channel LSBs
    for i in range(num_color_channels):
        for j in range(8):
            plt.imshow((image[:,:,i] & (2**(8-j-1))) >> (8-j-1))
            plt.axhline(0, color='r', linestyle='-', linewidth=1)
            plt.axhline(1, color='r', linestyle='-', linewidth=1)
            plt.show()
    
    # plot the third color channel LSBs
    for i in range(num_color_channels):
        for j in range(8):
            plt.imshow((image[:,:,i] & (2**(8-j-1))) >> (8-j-1))
            plt.axhline(0, color='r', linestyle='-', linewidth=1)
            plt.axhline(1, color='r', linestyle='-', linewidth=1)
            plt.show()
