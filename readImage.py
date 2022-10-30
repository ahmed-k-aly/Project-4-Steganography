import binascii
import numpy as np
import imageio.v2 as imageio 


def main():
    img = imageio.imread("sampleImages/hide_text.png")
    height, width, _ = img.shape
    print("Height:", height, "Width:", width)
    chars = getLSBchannels(img, height, width)
    #assert(len(chars) == 32 * 3)
    # get header.
    int_output = binaryToInt(chars[0:32])
    print(int_output)

    # convert binary to ASCII
    #chars = decode_binary_string(''.join(chars))
    # writeToFile(chars, "message.txt")

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
    for r in range(height):
        for c in range(width):
            if count < 15: # string ends at char 1526 i think.
                chars.append(str(img[r,c,0] & 1)) # get LSB of first channel
                chars.append(str(img[r,c,1] & 1)) # get LSB of second channel
                chars.append(str(img[r,c,2] & 1)) # get LSB of third channel
                count += 1
        
    # return string instead of array.
    return chars

    """
        Write the output to file.
    """
def writeToFile(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)

if __name__ == "__main__":
    main()