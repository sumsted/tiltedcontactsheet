from PIL import Image
from io import BytesIO
from random import shuffle


SPACING = 10
VCELLS = 10
MARGIN = 20

hcells = 0


def start(image_byte_array):
    original_image = convert_bytes_to_image(image_byte_array)
    working_image = create_working_image(original_image)
    destination_image = create_destination_image(working_image)
    randomize(working_image, destination_image)
    return convert_image_to_bytes(destination_image)


def create_working_image(original_image):
    global hcells
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    width, height = original_image.size
    if width > ((height*3)//2):
        new_width = (3 * height) // 2
        x1 = width//2 - new_width//2
        y1 = 0
        x2 = new_width + x1
        y2 = height
        hcells = new_width//(((height//VCELLS)*3)//2)
    else:
        new_height = (2 * width) // 3
        x1 = 0
        y1 = height//2 - new_height//2
        x2 = width
        y2 = new_height + y1
        hcells = width//(((new_height//VCELLS)*3)//2)
    return original_image.crop((x1, y1, x2, y2))


def create_destination_image(reference_image):
    width = ((VCELLS+1)*SPACING) + reference_image.size[0]
    height = ((hcells+1)*SPACING) + reference_image.size[1]
    return Image.new('RGBA', (width, height), 'black')


def randomize(working_image, destination_image):
    block_width = working_image.size[0] // hcells
    block_height = working_image.size[1] // VCELLS

    cell_coordinates = [ (x, y) for x in range(0, hcells) for y in range(0, VCELLS) ]
    shuffle(cell_coordinates)
    h2 = 0 
    v2 = 0 
    for coor in cell_coordinates:
        # get random block in work image
        wx1 = block_width * coor[0]
        wy1 = block_height * coor[1]
        wx2 = wx1 + block_width
        wy2 = wy1 + block_height
        block = working_image.crop((wx1, wy1, wx2, wy2))
        
        # paste in order to destination_image
        dx1 = block_width * h2 + (SPACING + (h2 * SPACING))
        dy1 = block_height * v2 + (SPACING + (v2 * SPACING))
        destination_image.paste(block, (dx1, dy1))
        v2 += 1
        if v2 >= VCELLS:
            h2 += 1
            v2 = 0 


def convert_image_to_bytes(image):
    fp = BytesIO()
    image.save(fp, 'JPEG')
    image_byte_array = fp.getvalue()
    fp.close()
    return image_byte_array


def convert_bytes_to_image(image_byte_array):
    fp = BytesIO(image_byte_array)
    return Image.open(fp)


if __name__ == '__main__':
    infile = 'mountain_in.jpg'
    outfile = 'mountain_out3.jpg'
    iba = open(infile, 'rb').read()
    oba = start(iba)
    open(outfile, 'wb').write(oba)