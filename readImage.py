import numpy as np
import imageio.v2 as imageio 


def main():
    img = imageio.imread("sampleImages/hide_text.png")
    height, width, _ = img.shape
    print("Height:", height, "Width:", width)
    chars = getTextChars(img, height, width)
    #print chars as a string of 0s and 1s

    # # convert binary to ASCII
    text = binaryToAsciiString(''.join(chars))
    writeToFile(text, "hidden_message.txt")

    # # get hidden image.
    hidingImage = imageio.imread("sampleImages/hide_image.png")
    height_1, width_2, channels = img.shape
    hidden_height, hidden_width = getImageHeaderFromMessage(hidingImage, height_1, width_2, 64)
    print("Hidden Height:", hidden_height, "Hidden Width:", hidden_width)

    # read pixels from hidingImage and write to img.
    chars = readImagePixels(hidingImage, height_1, width_2, hidden_height, hidden_width)
    img = convertBitsIntoImage(chars, hidden_height, hidden_width)
    imageio.imwrite("hidden_image.png", img)




    """
        Read pixels about a hidden image 
    """    
def readImagePixels(img, height, width, hidden_height, hidden_width, header_size=64):
    total_bits = (header_size-1) + (24 * hidden_height * hidden_width)
    # create a new  array to store the pixels.
    chars = []
    for r in range(height):
        for c in range(width): 
            if(len(chars) < total_bits):
                chars.append(str(img[r,c,0] & 1)) # get LSB of first channel
                chars.append(str(img[r,c,1] & 1)) # get LSB of second channel
                chars.append(str(img[r,c,2] & 1)) # get LSB of third channel
            else: 
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


def binaryToASCII(chars):
    # convert binary to ASCII
    # https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
    n = binaryToInt(''.join(chars))
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode() # buggy code

    """
        Given a binary string, return an ascii string
    """
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
def getTextChars(img, height, width):
    chars = []
    count = 0
    numCharsInHiddenText = getTextHeaderFromImage(img, height, width, 32)
    bitSizeOfHeader = len(str(numCharsInHiddenText)) * 8
    bitSizeOfText = (numCharsInHiddenText * 8) + bitSizeOfHeader
    for r in range(height):
        for c in range(width):
            if count < bitSizeOfText: # string ends at char 1526 i think.
                chars.append(str(img[r,c,0] & 1)) # get LSB of first channel 
                chars.append(str(img[r,c,1] & 1)) # get LSB of second channel
                chars.append(str(img[r,c,2] & 1)) # get LSB of third channel
                count = len(chars)
            else: 
                break
    

    # remove the header from our chars
    chars = chars[bitSizeOfHeader:]
        
    # return string instead of array.
    return chars



    """
        Given an image, get metadata about the hidden text
    """
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
    
    return binaryToInt(textMetadata)
    



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
        Write the output to file.
    """
def writeToFile(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)

if __name__ == "__main__":
    main()