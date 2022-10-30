import binascii
from email.mime import image
from importlib.metadata import metadata
import numpy as np
import imageio.v2 as imageio 


def main():
    img = imageio.imread("sampleImages/hide_text.png")
    height, width, _ = img.shape
    print("Height:", height, "Width:", width)
    chars = getLSBchannels(img, height, width)
    #assert(len(chars) == 32 * 3)
    # get header.
   

    # convert binary to ASCII
    chars = binaryToAsciiString(''.join(chars))
    writeToFile(chars, "message.txt")

    # get hidden image.
    hidingImage = imageio.imread("sampleImages/hide_image.png")
    height_1, width_2, channels = img.shape
    hidden_height, hidden_width = getImageHeaderFromMessage(hidingImage, height_1, width_2, 64)
    getImage(img, height, width, hidden_height, hidden_width)
    
    print("Hidden Image has height: ", hidden_height, " width ", hidden_width)
    # print("Height:", height, "Width:", width, "Number of Channels:", channels)

def binaryToASCII(chars):
    # convert binary to ASCII
    # https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
    n = binaryToInt(''.join(chars))
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode() # buggy code


def binaryToAsciiString(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

    """
        Given a binary string, return an int
    """
def binaryToInt(binaryArray):
    return int(''.join(binaryArray), 2)


    """
    Method that returns an array with the value of the least significant bit of each pixel channel until it can construct three double-words.
    """
def getLSBchannels(img, height, width):
    chars = []
    count = 0
    textSize = getTextHeaderFromImage(img, height, width, 32)
    for r in range(height):
        for c in range(width):
            if count < 1526: # string ends at char 1526 i think.
                chars.append(str(img[r,c,0] & 1)) # get LSB of first channel
                chars.append(str(img[r,c,1] & 1)) # get LSB of second channel
                chars.append(str(img[r,c,2] & 1)) # get LSB of third channel
                count += 1
            else: 
                break
    
        
    # return string instead of array.
    return chars

def getTextHeaderFromImage(img, height, width, header_size):
    textMetadata = []
    for r in range(height):
        for c in range(width):
            if len(textMetadata) < header_size:
                textMetadata.append(str(img[r,c,0] & 1))
                textMetadata.append(str(img[r,c,1] & 1))
                textMetadata.append(str(img[r,c,2] & 1))
            else:
                break

    textMetadata = ''.join(textMetadata)[0:header_size]

    return binaryToASCII(textMetadata)
    



    """
        Method to try extract header from an image.
    """
def getImageHeaderFromMessage(img, height, width, header_size):
    image_metadata = []
    for r in range(height):
        for c in range(width):
            if len(image_metadata) < header_size:
                image_metadata.append(str(img[r,c,0] & 1))
                image_metadata.append(str(img[r,c,1] & 1))
                image_metadata.append(str(img[r,c,2] & 1))
            else: 
                break
           

    image_metadata = ''.join(image_metadata)[0:header_size]
    height, width = binaryToInt(image_metadata[:header_size//2]), binaryToInt(image_metadata[header_size//2:])

    return height, width    


    """
        Method to extract images
    """
def getImage(img, height, width, hidden_height, hiden_width):
    bit_limit = hidden_height * hiden_width
    count = 0
    for r in range(hidden_height):
        for c in range(hiden_width):
            img[r, c][0] = 0
            img[r, c][1] = img[r, c, 1]
            img[r, c][2] = 128 
                # count += 1

    imageio.imwrite("altered_py.png", img)










    """
        Write the output to file.
    """
def writeToFile(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)

if __name__ == "__main__":
    main()