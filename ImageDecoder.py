"""
A program to decode images hidden in other images through LSB steganography.
"""

import imageio
import numpy as np

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
        Read pixels about a hidden image 
    """    
def readImagePixelsLSB(img, height, width, hidden_height, hidden_width, header_size=64):
    total_bits = (header_size-1) + (24 * hidden_height * hidden_width)
    # create a new  array to store the pixels.
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width): 
            if(len(chars) < total_bits):
                chars.append(str(img[r,c,0] & 1)) # get LSB of first channel
                chars.append(str(img[r,c,1] & 1)) # get LSB of second channel
                chars.append(str(img[r,c,2] & 1)) # get LSB of third channel
            else: 
                break_out_flag = True
                break

        if break_out_flag:
            break

    return chars[header_size:]


"""Reads pixels in a hidden image using the two least significant bits 
"""
def readImagePixelsLSB2(img, height, width, hidden_height, hidden_width, header_size=64):
    total_bits = (header_size-1) + (24 * hidden_height * hidden_width)
    # create a new  array to store the pixels.
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width): 
            if(len(chars) < total_bits):
                chars.append(str(img[r,c,0] & 1)) # get LSB of first channel                
                chars.append(str((img[r,c,0] & 2) >> 1)) # get 2nd LSB of first channel
                #get 3rd LSB of first channel
                chars.append(str((img[r,c,0] & 4) >> 2))
                
                chars.append(str(img[r,c,1] & 1)) # get LSB of second channel
                chars.append(str((img[r,c,1] & 2) >> 1)) # get 2nd LSB of second channel
                chars.append(str((img[r,c,1] & 4) >> 2))
                
                chars.append(str(img[r,c,2] & 1)) # get LSB of third channel
                chars.append(str((img[r,c,2] & 2) >> 1)) # get 2nd LSB of first channel
                chars.append(str((img[r,c,2] & 4) >> 2))
            else: 
                break_out_flag = True
                break

        if break_out_flag:
            break

    return chars[header_size:]


    """
        Given a char of bits, convert into an image.
    """
def convertBitsIntoImage(arr, height, width):

    chars = ''.join(arr)
    result = []
    starter = 0
    for c in range(len(chars)):
        if c % 8 == 0:
            x = binaryToInt(chars[starter:starter + 8])
            result.append(x)
            starter += 8

    # convert 1D array to 3D array.
    # https://stackoverflow.com/questions/32591211/convert-1d-array-to-3d-array
    return np.reshape(result, (height, width, 3)).astype(np.uint8)


    """
        Given a binary string, return an int
    """
def binaryToInt(binaryArray):
    return int(''.join(binaryArray), 2)


def main():
    img = imageio.imread("2LSB.png")
    height_1, width_2, channels = img.shape
    hidden_height, hidden_width = getImageHeaderFromMessage(img, height_1, width_2, 64)
    print("Hidden Height:", hidden_height, "Hidden Width:", hidden_width)

    # read pixels from hidingImage and write to img.
    chars = readImagePixelsLSB2(img, height_1, width_2, hidden_height, hidden_width)
    
    img = convertBitsIntoImage(chars, hidden_height, hidden_width)
    imageio.imwrite("2LSBSS.png", img)

if __name__ == '__main__':
    main()