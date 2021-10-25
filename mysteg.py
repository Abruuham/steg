from PIL import Image


# Convert the text to its binary representation
def text_to_binary(message):
    binary = []

    for i in message:
        binary.append(format(ord(i), '08b'))

    return binary


# Modify the pixels for the new image
def modified_pixels(pixel, message):
    binary_message = text_to_binary(message)
    image_iter = iter(pixel)
    for i in range(len(binary_message)):
        pix = [value for value in image_iter.__next__()[:3] +
               image_iter.__next__()[:3] +
               image_iter.__next__()[:3]]

        for j in range(0, 8):
            if binary_message[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif binary_message[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if i == len(binary_message) - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


# helper method for encoding image
def encode_helper(image_copy, message):
    width = image_copy.size[0]
    (x, y) = (0, 0)

    for pixel in modified_pixels(image_copy.getData(), message):

        image_copy.putpixel((x, y), pixel)
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1


# function to encode our message
def encode():
    file_name = input('Enter the name of the image with extension: ')
    image = Image.open(file_name, 'r')

    message = input('Enter the message to be encoded')
    if len(message) == 0:
        raise Exception('Message cannot be empty')

    image_copy = image.copy()
    encode_helper(image_copy, message)

    new_file_name = input('Please enter a name for the encoded image: ')
    if len(new_file_name) == 0:
        raise ValueError('New image filename cannot be empty')
    else:
        new_file_name.save(new_file_name+'.png')


if __name__ == '__main__':
    welcome_message = int(input('1. Encode\n2. Decode\n'))

    if welcome_message == 1:
        encode()
    elif welcome_message == 2:
        print('Decoded message: ' + decode())
    else:
        raise Exception('Invalid input')
