__author__ = 'scottumsted'

from PIL import Image
from io import BytesIO

class TiltedContactSheet:

    def __init__(self):
        self._spacing = 10
        self._hcells = 0
        self._vcells = 10
        self._hrotate = (2, 10)
        self._vrotate = (3, 17)
        self._rotate_angle = 3

    def start(self, image_byte_array):
        original_image = self._convert_bytes_to_image(image_byte_array)
        working_image = self._create_working_image(original_image)
        destination_image = self._create_destination_image(working_image)
        self._transform(working_image, destination_image)
        return self._convert_image_to_bytes(destination_image)

    def _create_working_image(self, original_image):
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
            self._hcells = new_width//(((height//self._vcells)*3)//2)
        else:
            new_height = (2 * width) // 3
            x1 = 0
            y1 = height//2 - new_height//2
            x2 = width
            y2 = new_height + y1
            self._hcells = width//(((new_height//self._vcells)*3)//2)
        return original_image.crop((x1, y1, x2, y2))

    def _create_destination_image(self, reference_image):
        width = ((self._vcells+1)*self._spacing) + reference_image.size[0]
        height = ((self._hcells+1)*self._spacing) + reference_image.size[1]
        return Image.new('RGBA', (width, height), 'black')

    def _transform(self, working_image, destination_image):
        block_width = working_image.size[0] // self._hcells
        block_height = working_image.size[1] // self._vcells
        rotate_count = 0
        for h in range(0, int(self._hcells)):
            for v in range(0, self._vcells):
                # calculate working and destination coordinates
                wx1 = block_width * h
                wy1 = block_height * v
                wx2 = wx1 + block_width
                wy2 = wy1 + block_height
                dx1 = block_width * h + (self._spacing + (h * self._spacing))
                dy1 = block_height * v + (self._spacing + (v * self._spacing))
                if self._vrotate[0] <= v <= self._vrotate[1] and self._hrotate[0] <= h <= self._hrotate[1]:
                    margin = 20
                    large_block = working_image.crop((wx1-margin, wy1-margin, wx2+margin, wy2+margin))
                    angle = self._rotate_angle if rotate_count % 2 == 0 else (-1 * self._rotate_angle)
                    block = large_block.rotate(angle).crop((margin, margin,
                                                            large_block.size[0]-margin, large_block.size[1]-margin))
                    rotate_count += 1
                else:
                    block = working_image.crop((wx1, wy1, wx2, wy2))
                destination_image.paste(block, (dx1, dy1))

    def _convert_image_to_bytes(self, image):
        fp = BytesIO()
        image.save(fp, 'JPEG')
        image_byte_array = fp.getvalue()
        fp.close()
        return image_byte_array

    def _convert_bytes_to_image(self, image_byte_array):
        fp = BytesIO(image_byte_array)
        return Image.open(fp)


if __name__ == '__main__':
    infile = 'mountain_in.jpg'
    outfile = 'mountain_out2.jpg'
    iba = open(infile, 'rb').read()
    tcs = TiltedContactSheet()
    oba = tcs.start(iba)
    open(outfile, 'wb').write(oba)