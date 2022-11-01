We use numpy version number
WE use imageio version number

Run code with python3 readImage.python3

Code has the following functions:

readImagePixels : Given a height and a width, returns a binary string that we think will form an image representation
convertBitsIntoImage: Given an array of chars, it returns an image
binaryToAsciiString : Given a string of binary, it returns an ascii string.
binaryToInt: Given a string of binary, it returns an integer 
getLSBchannels : Gets the least significant bit from the channels
getTextHeaderFromImage : Given an image, and a header size, it returns text metadata. In this case, it's an int 
getImageHeaderFromMessage : Given an image and a header size, it returns an the height and width of hidden image.
writeToFile : Given a string and a file name, it writes and saves to a file with the given file name.