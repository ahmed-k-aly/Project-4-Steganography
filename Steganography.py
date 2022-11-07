import numpy as np
import imageio.v2 as imageio
import glob

# looking at 1 channels
#

channels = ["Red", "Green", "Blue", "All"]


def main():
    img = imageio.imread("projectImages/Boyos.png")
    file_title = "Boyos.png"
    innerHeight, innerWidth = innerHeight, innerWidth = getImageHeaderFromSingleChannel(img, 0)
    chars = readBitsFromSingleChannel(img, innerHeight, innerWidth, 0, 64)
    new_image = convertBitsIntoImage(chars, innerHeight, innerWidth)
    name = "hidden-images/ABEL_" + str(0) + file_title
    imageio.imwrite(name, new_image)

    flippedImage = flipChannelBits(imageio.imread(name))
    new_name = "hidden-images/ABEL_flipped_" + str(0) + file_title
    imageio.imwrite(new_name, flippedImage)
    
    # file_name = "projectImages/AlbumCover.png"
    # file_title = file_name.split("/")[1]
    # img = imageio.imread(file_name)
    # innerHeight, innerWidth = getImageHeaderFromSingleChannel(img,1)
    # chars = readBitsFromSingleChannel(img, innerHeight, innerWidth, 1)
    # new_image = convertBitsIntoImage(chars, innerHeight, innerWidth)
    # name = "hidden-images/" + channels[1] + file_title
    # imageio.imwrite(name, new_image)
    # flippedImage = flipChannelBits(imageio.imread(name))
    # new_name = "hidden-images/flipped_" + channels[1] + "_" + file_title
    # imageio.imwrite(new_name, flippedImage)

    # exposeImg = imageio.imread(new_name)
    # for y in range(3):
    #     innerHeight, innerWidth = getImageHeaderFromSingleChannel(new_image,y)
    #     print(innerHeight, innerWidth, " on channel ", channels[y])
    # exposed_name = "exposed_ALL_" + file_title
    # exposed_dark_name = "exposed_DARK_" + file_title
    # exposed_light_name = "exposed_LIGHT_" + file_title

    # exposePatterns(exposeImg, exposed_name)
    # exposeDarkPatterns(exposeImg, exposed_dark_name)
    # exposeLightPatterns(exposeImg, exposed_light_name)
    

    


        


def readFilesAsUseful():
    files = ["projectImages/StetchyYawnyBois.png", 
    "projectImages/FlyAway.png", 
    "projectImages/AlbumCover.png",
    "projectImages/FlossyBoi.png",
    "projectImages/Boyos.png",
    "projectImages/Boyos.png",
    "projectImages/Boyos.png",
    "projectImages/Knight.png",
    "projectImages/OhHai.png",
    "projectImages/Drone_Footage_Frame001.png", 
    "projectImages/Drone_Footage_Frame001.png", 
    "projectImages/Drone_Footage_Frame001.png"
    ]
    
    for file_name in files:
        
        img = imageio.imread(file_name)
        for y in range(4):
            try:
                # if we get hidden image, read each channel of the hidden image.
                chars = readTextFromSingleChannel(img, y)
                new_text = binaryToAsciiString(''.join(chars))
                file_title = "hidden-texts/" + str(channels[y]) + "_channel_" + file_name.split("/")[1].replace(".png", ".txt")
                writeToFile(new_text, file_title )
            except Exception as err:
                print(err)

            


def headerHunter():
    
    usefulImageNotification = []
    files = [file for file in glob.glob("projectImages/*.png")]
    for file_name in files:
        try:
            img = imageio.imread(file_name)
            # read them in sequential order
            innerHeight, innerWidth = getImageHeaderFromMessage(img)
            text = notifyOfUsefulBasicHeaders(innerHeight, innerWidth, 3, file_name)
            for x in range(3):
                innerHeight, innerWidth = getImageHeaderFromSingleChannel(img, x)
                text = notifyOfUsefulBasicHeaders(innerHeight, innerWidth, x, file_name)    
                usefulImageNotification.append(text)
        except Exception as err:
            print(err)
        

    writeToFile(''.join(usefulImageNotification), "hidden-texts/images-metadata.txt")

def notifyOfUsefulBasicHeaders(innerHeight, innerWidth, channel_num, file_name):
    text = ""
    if innerHeight < 9000 or innerWidth < 9000:
        text = "Image " + file_name + " potentially has useful TEXT" + \
            " in " + channels[channel_num] + " channel "+ \
            "first 32 chars : " + str(innerHeight) + " inner width: " + str(innerWidth) + "\n"

        if innerHeight < 9000 and innerWidth < 9000:
            text = "Image " + file_name + " potentially has a useful IMAGE" + \
            " in " + channels[channel_num] + " channel "+ \
            "first 32 chars : " + str(innerHeight) + " inner width: " + str(innerWidth) + "\n"


    return text
    

                


def exposeDarkPatterns(img, image_name):
    height, width, _ = img.shape
    # make everything a one, make everything a zero.
    for r in range(height):
        for c in range(width):
            img[r, c][0] = ((img[r, c][0] & 1) * (img[r, c][0]))
            img[r, c][1] = ((img[r, c][1] & 1) * (img[r, c][1]))
            img[r, c][2] = ((img[r, c][2] & 1) * (img[r, c][2]))

    file_name = "exposedImages/dark-exposed/dark_exposed_image_"+image_name

    imageio.imwrite(file_name, img)


def exposeLightPatterns(img, image_name):
    height, width, _ = img.shape
    # make everything a one, make everything a zero.
    for r in range(height):
        for c in range(width):
            img[r, c][0] = (~(img[r, c][0] & 1) * (img[r, c][0]))
            img[r, c][1] = (~(img[r, c][1] & 1) * (img[r, c][1]))
            img[r, c][2] = (~(img[r, c][2] & 1) * (img[r, c][2]))

    file_name = "exposedImages/light-exposed/light_exposed_image_"+image_name

    imageio.imwrite(file_name, img)


def readImagesLikeLurkingColorBalanced(file_name="projectImages/Lurking_Color_Balanced.png"):
    img = imageio.imread(file_name)
    file_title = file_name.split("/")[1]
    height, width = getImageHeaderFromMessage(img)
    imageChars = readImagePixels(img, height, width)
    img = flipChannelBits(convertBitsIntoImage(imageChars, height, width))
    file_name = "hidden-images/" + file_title
    imageio.imwrite(file_name, img)

    imgwithText = imageio.imread(file_name)
    # numChars = getTextHeaderFromImage(imgwithText)
    # print(numChars)

    for x in range(3):
        # reading each channel
        innerHeight, innerWidth = getImageHeaderFromSingleChannel(
            imgwithText, x)
        # exposePatterns(imgWithText, expose_name)
        for y in range(3):
            # if we get hidden image, read each channel of the hidden image.
            chars = readTextFromSingleChannel(imgwithText, y)
            new_text = binaryToAsciiString(''.join(chars))
            bit_file_name = "hidden-texts/flipped_" + \
                str(x) + file_title.replace(".png", "") + str(y) + ".txt"
            writeToFile(new_text, bit_file_name)


def readImagesLikeBoyos(file_name="projectImages/Boyos.png"):
    img = imageio.imread(file_name)
    for x in range(3):
        try:
            file_title = file_name.split('/')[1]
            innerHeight, innerWidth = getImageHeaderFromSingleChannel(img, x)
            chars = readBitsFromSingleChannel(img, innerHeight, innerWidth, x, 64)
            new_image = convertBitsIntoImage(chars, innerHeight, innerWidth)
            name = "hidden-images/" + str(x) + file_title
            imageio.imwrite(name, new_image)

            flippedImage = flipChannelBits(imageio.imread(name))
            new_name = "hidden-images/flipped_" + str(x) + file_title
            imageio.imwrite(new_name, flippedImage)

            imgWithText = imageio.imread(new_name)
            allChannelsChars = readTextFromAllChannels(imgWithText)
            allChannelsText = binaryToAsciiString(''.join(allChannelsChars))
            allChannelsName = "hidden-texts/flipped_" + \
                str(x) + "channel_all" + file_title.replace(".png", '.txt')
            writeToFile(allChannelsText, allChannelsName)

            # exposePatterns(imgWithText, expose_name)
            for y in range(3):
                chars = readTextFromSingleChannel(imgWithText, y)
                new_text = binaryToAsciiString(''.join(chars))
                bit_file_name = "hidden-texts/flipped_" + \
                    str(x) + file_title.replace('.png', '') + \
                    "_channel" + str(y) + ".txt"
                writeToFile(new_text, bit_file_name)
        except Exception as err:
            print(err)

def flipChannelBits(img):
    counter = 0
    height, width, _ = img.shape
    for r in range(height):
        for c in range(width):
            img[r, c, 0] = int(format(img[r, c, 0], '08b')[::-1], 2)
            img[r, c, 1] = int(format(img[r, c, 1], '08b')[::-1], 2)
            img[r, c, 2] = int(format(img[r, c, 2], '08b')[::-1], 2)

            if counter < 10:
                print([img[r, c, 0], img[r, c, 1], img[r, c, 2]])
                counter += 1

    return img

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


def getImageHeaderFromSingleChannel(img, channel_num, header_size=64):
    height, width, _ = img.shape
    image_metadata = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(image_metadata) < header_size:
                image_metadata.append(str(img[r, c, channel_num] & 1))

    image_metadata = ''.join(image_metadata)[0:header_size]
    height, width = binaryToInt(
        image_metadata[:header_size//2]), binaryToInt(image_metadata[header_size//2:])

    return height, width


"""
        Given an image, get metadata about the hidden text
    """


def getTextHeaderFromImage(img, header_size=32):
    height, width, _ = img.shape
    textMetadata = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(textMetadata) < header_size:
                textMetadata.append(str(img[r, c, 0] & 1))
                textMetadata.append(str(img[r, c, 1] & 1))
                textMetadata.append(str(img[r, c, 2] & 1))
            else:
                break_out_flag = True
                break

        if break_out_flag:
            break

    textMetadata = ''.join(textMetadata)[0:header_size]

    return binaryToInt(textMetadata)

    """
        Method that returns an array with the value of the least significant bit of each pixel channel until it can construct three double-words.
    """


def getTextWithHeader(img):
    height, width, _ = img.shape
    chars = []
    count = 0
    numCharsInHiddenText = getTextHeaderFromImage(img)
    print("text has ", numCharsInHiddenText, " characters")
    bitSizeOfHeader = len(str(numCharsInHiddenText)) * 8
    bitSizeOfText = (numCharsInHiddenText * 8) + bitSizeOfHeader
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if count < bitSizeOfText:  # string ends at char 1526 i think.
                chars.append(str(img[r, c, 0] & 1))  # get LSB of first channel
                # get LSB of second channel
                chars.append(str(img[r, c, 1] & 1))
                chars.append(str(img[r, c, 2] & 1))  # get LSB of third channel
                count = len(chars)
            else:
                break_out_flag = True
                break

        if break_out_flag:
            break

    # remove the header from our chars
    chars = chars[bitSizeOfHeader:]
    return chars


def readTextFromAllChannels(img):
    height, width, _ = img.shape
    chars = []
    for r in range(height):
        for c in range(width):
            chars.append(str(img[r, c, 0] & 1))
            chars.append(str(img[r, c, 1] & 1))
            chars.append(str(img[r, c, 2] & 1))

    return chars


def readTextFromSingleChannel(img, channel):
    height, width, _ = img.shape
    chars = []
    for r in range(height):
        for c in range(width):
            chars.append(str(img[r, c, channel] & 1))

    return chars


def readBitsFromSingleChannel(img, hidden_height, hidden_width, channel_num, header_size=0):
    height, width, _ = img.shape
    total_bits = (header_size-1) + (24 * hidden_height * hidden_width)
    # create a new  array to store the pixels.
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if (len(chars) < total_bits):
                # get LSB of first channel
                chars.append(str(img[r, c, channel_num] & 1))
            else:
                break_out_flag = True
                break

        if break_out_flag:
            break

    return chars[header_size:]

    """
        Read pixels about a hidden image 
    """


def readImagePixels(img, hidden_height, hidden_width, header_size=64):
    height, width, _ = img.shape
    total_bits = (header_size-1) + (24 * hidden_height * hidden_width)
    # create a new  array to store the pixels.
    chars = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if (len(chars) < total_bits):
                chars.append(str(img[r, c, 0] & 1))  # get LSB of first channel
                # get LSB of second channel
                chars.append(str(img[r, c, 1] & 1))
                chars.append(str(img[r, c, 2] & 1))  # get LSB of third channel
            else:
                break_out_flag = True
                break

        if break_out_flag:
            break

    return chars[header_size:]

    """
        Given a binary string, return an int
    """


def binaryToInt(binaryArray):
    return int(''.join(binaryArray), 2)


def readImageFromOneChannel(img, channel):
    mask = (2**1) - 1
    height, width, _ = img.shape
    chars = []
    for r in range(height):
        for c in range(width):
            chars.append(format((img[r, c, channel] & mask), 'b'))

    """
        Method to try extract header from an image.
    """


def getImageHeaderFromMessage(img, header_size=64):
    height, width, _ = img.shape
    image_metadata = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(image_metadata) < header_size:
                image_metadata.append(str(img[r, c, 0] & 1))
                image_metadata.append(str(img[r, c, 1] & 1))
                image_metadata.append(str(img[r, c, 2] & 1))
            else:
                break_out_flag = True
                break
        if break_out_flag:
            break

    image_metadata = ''.join(image_metadata)[0:header_size]
    height, width = binaryToInt(
        image_metadata[:header_size//2]), binaryToInt(image_metadata[header_size//2:])

    return height, width


def decodeFirstFiveBitsOfAllImages():
    files = [file for file in glob.glob("projectImages/*.png")]
    for file_name in files:
        img = imageio.imread(file_name)
        for x in range(1, 6):
            print("reading ", file_name, "round: ", x)
            chars = getTextChars(img, x)
            text = binaryToAsciiString(''.join(chars))
            reverse_string = ''.join(chars)[::1]
            reverseText = binaryToAsciiString(reverse_string)
            matches = ["implement", "read", "invest", "lemons",
                       "joke", "knock", "watching", "pots", "list", "shopping"]
            if any(x in text for x in matches) or any(x in reverseText for x in matches):
                print(file_name, "has a potential match")

            name = "increasingBits/" + \
                file_name.split('/')[1] + str(x) + "_LSB.txt"
            reversedName = "increasingBits/" + \
                file_name.split('/')[1] + str(x) + "_LSB_reversed.txt"
            writeToFile(text, name)
            writeToFile(reverseText, reversedName)
            print("finished.... \n")

    """
        Given an image and x num bits find the least significant x bits
    """


def getTextChars(img, numLSB):
    mask = (2**numLSB) - 1
    height, width, _ = img.shape
    chars = []
    for r in range(height):
        for c in range(width):
            chars.append(format((img[r, c, 0] & mask), 'b'))
            chars.append(format((img[r, c, 1] & mask), 'b'))
            chars.append(format((img[r, c, 2] & mask), 'b'))

    return chars


def exposePatterns(img, image_name):
    height, width, _ = img.shape
    # make everything a one, make everything a zero.
    for r in range(height):
        for c in range(width):
            img[r, c][0] = ((img[r, c][0] & 1) * 255)
            img[r, c][1] = ((img[r, c][1] & 1) * 255)
            img[r, c][2] = ((img[r, c][2] & 1) * 255)

    file_name = "exposedImages/exposed_image_"+image_name

    imageio.imwrite(file_name, img)

    """
        Given a binary string, return an ascii string
    """


def binaryToAsciiString(s):
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(len(s)//8))

    """
        Write the output to file.
    """


def writeToFile(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    main()
