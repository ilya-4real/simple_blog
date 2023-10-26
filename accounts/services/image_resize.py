from PIL import Image


def resize_image(image_path: str):
    """
    function that crops an image to a square depending on size of an image
    :param image_path: path to the image that will be cropped
    :return:
    """
    im = Image.open(image_path)
    width, height = im.size  # Get dimensions
    new_size = min(width, height)  # get a minimum side to crop to a square

    left = round((width - new_size) / 2)
    top = round((height - new_size) / 2)
    x_right = round(width - new_size) - left
    x_bottom = round(height - new_size) - top
    right = width - x_right
    bottom = height - x_bottom

    # Crop the center of the image
    cropped_image = im.crop((left, top, right, bottom))
    cropped_image.save(image_path)
    return 'image resized'  # to know that the picture has cropped

