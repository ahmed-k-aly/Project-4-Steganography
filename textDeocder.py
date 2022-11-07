"""
Program that detects steganography in images, particularly hidden text 
"""
from readImage import getTextHeaderFromImage
import imageio

def decodeTextInImage(image, height, width, headerSize=32):
    # step1: read the header of the image to get the size of the hidden image
    # step2: read each pixel and get the LSB of each pixel channel until we have read the number of characters in the hidden text
    # step3: convert the binary string to a string of characters
    # step4: return the string of characters

    # step1: read the header of the image to get the size of the hidden image
    numCharsInHiddenText = getTextHeaderFromImage(image, height, width, headerSize)
    print("text has ", numCharsInHiddenText, " characters")
    bitSizeOfHeader = len(str(numCharsInHiddenText)) * 8
    bitSizeOfText = (numCharsInHiddenText * 8) + bitSizeOfHeader

    # step2: read each pixel and get the LSB of each pixel channel until we have read the number of characters in the hidden text
    chars = []
    count = 0
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if count < bitSizeOfText: # string ends at char 1526 i think.
                chars.append(str(image[r,c,0] & 1)) # get LSB of first channel 
                chars.append(str(image[r,c,1] & 1)) # get LSB of second channel
                chars.append(str(image[r,c,2] & 1)) # get LSB of third channel
                count = len(chars)
            else: 
                break_out_flag = True
                break
        if break_out_flag:
            break

    # step3: convert the binary string to a string of characters
    # remove the header from our chars
    chars = chars[bitSizeOfHeader:]
    # return string instead of array.
    return chars


def main():
    print("hello world")
    img = imageio.imread("hidden_images.png")
    height, width, _ = img.shape
    text = decodeTextInImage(img, height, width)
    # print text 
    text = ''.join(text)
    text = ''.join(chr(int(text[i*8:i*8+8], 2)) for i in range(len(text)//8))
    print(text)
    
if __name__ == '__main__':
    main()