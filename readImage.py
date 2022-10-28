import binascii
import numpy as np
import imageio


def main():
    img = imageio.imread("sampleImages/hide_text.png")
    height, width, _ = img.shape
    print("Height:", height, "Width:", width)
    chars = getLSBchannels(img, height, width)
    #assert(len(chars) == 32 * 3)
    # convert binary to ASCII
    chars = binaryToASCII(chars)
    print(chars)

def binaryToASCII(chars):
    # convert binary to ASCII
    # https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
    n = int(''.join(chars), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()



    """
    Method that returns an array with the value of the least significant bit of each pixel channel until it can construct three double-words.
    """
def getLSBchannels(img, height, width):
    chars = []
    count = 0
    for r in range(height):
        for c in range(width):
            if count < 32:
                chars.append(str(img[r,c,0] & 1)) # get LSB of first channel
                chars.append(str(img[r,c,1] & 1)) # get LSB of second channel
                chars.append(str(img[r,c,2] & 1)) # get LSB of third channel
                count += 1
    return chars
    

if __name__ == "__main__":
    main()