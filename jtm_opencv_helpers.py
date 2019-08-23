import numpy as np
import cv2
import imutils

def create_blank_image(width: int, height: int, color = (255,255,255)):
	"""Return a width x height image with color specified.

	Returns an OpenCV compatible NumPy array of the given width and
	height with the 3rd color dimension initialized to color. For a
	grayscale image, color is simply an integer. For another format
	(e.g. BGR or HSV), color is a 3 element tuple.

	Args:
		width (int):	The matrix width (1st dimension)
		height (int):	The matrxi height (2nd dimension)
		color (int or tuple):	The value to initialize the color to.

	Returns:
		numpy.ndarray:	The image.

	Examples:
		>>> create_blank_image(3, 2, 255)
		array([[255, 255, 255],
       	       [255, 255, 255]], dtype=uint8)
		>>> create_blank_image(3, 2, (255, 255, 255))
		array([[[255, 255, 255],
			[255, 255, 255],
			[255, 255, 255]],

			[[255, 255, 255],
			[255, 255, 255],
			[255, 255, 255]]], dtype=uint8)
	"""
	try:
		depth = len(color)
		image = np.zeros((height, width, depth), np.uint8)
	except TypeError:
		image = np.zeros((height, width), np.uint8)

	image[:] = color
	return image

class Image_Concatenate:
	@classmethod
	def horizontal_and_cut_larger(cls, images_list: list):
		"""
		Combines all images horizontally, with a max height of the
		smallest image height. Excess of larger images will be cut
		off, starting from the bottom up.
		"""

		h_min = min(cls.matrix_height(im) for im in images_list)
		chopped_list = [im[:, :h_min] for im in images_list]
		return cls.horizontal_and_resize_down(chopped_list)

	@classmethod
	def vertical_and_cut_larger(cls, images_list: list):
		"""
		Combines all images vertically, with a max width of the
		smallest image height. Excess of larger images will be cut
		off, starting from the right side, moving left.
		"""

		w_min = min(cls.matrix_width(im) for im in images_list)
		chopped_list = [im[:w_min, :] for im in images_list]
		return cls.vertical_and_resize_down(chopped_list)

	@classmethod
	def horizontal_and_fill_empty(cls, images_list: list,
		empty_color: (255, 255, 255)):
		"""
		Combines all images horizontally, filling voids underneath
		smaller height images with a solid color.

		empty_color should be a color representation, in corresponding
		color space to the images. E.g. a BGR image should have a
		3 element tuple, with each element an integer ranging from 0
		to 255 representing blue, green, and red intensities,
		respectively.
		"""

		h_max = max(cls.matrix_height(im) for im in images_list)
		padded = list()
		for im in images_list:
			blank = create_blank_image(cls.matrix_width(im), h_max,
			            empty_color)
			blank[0:im.shape[0], 0:im.shape[1]] = im
			padded.append(blank)
		return padded

	@classmethod
	def vertical_and_fill_empty(cls, images_list: list,
		empty_color: (255, 255, 255)):
		"""
		Combines all images vertically, filling voids to the right of
		smaller width images with a solid color.

		empty_color should be a color representation, in corresponding
		color space to the images. E.g. a BGR image should have a
		3 element tuple, with each element an integer ranging from 0
		to 255 representing blue, green, and red intensities,
		respectively.
		"""

		w_max = max(cls.matrix_width(im) for im in images_list)
		padded = list()
		for im in images_list:
			blank = create_blank_image(w_max, cls.matrix_height(im),
			            empty_color)
			blank[0:im.shape[0], 0:im.shape[1]] = im
			padded.append(blank)
		return padded

	@classmethod
	def horizontal_and_resize_down(cls, images_list: list):
		"""
		Combines all images horizontally, resizing photos to match the
		smallest height image's height. Aspect ratio maintained.
		"""

		h_min = min(cls.matrix_height(im) for im in images_list)
		resized_list = [imutils.resize(im, None, h_min) for im in images_list]
		return cv2.hconcat(resized_list)

	@classmethod
	def vertical_and_resize_down(cls, images_list: list):
		"""
		Combines all images vertically, resizing photos to match the
		smallest width image's width. Aspect ratio maintained.
		"""

		w_min = min(cls.matrix_width(im) for im in images_list)
		resized_list = [imutils.resize(im, w_min) for im in images_list]
		return cv2.vconcat(resized_list)

	@classmethod
	def horizontal_and_resize_up(cls, images_list: list):
		"""
		Combines all images horizontally, resizing photos to match the
		largest height image's height. Aspect ratio maintained.
		"""

		h_max = max(cls.matrix_height(im) for im in images_list)
		resized_list = [imutils.resize(im, None, h_max) for im in images_list]
		return cv2.hconcat(resized_list)

	@classmethod
	def vertical_and_resize_up(cls, images_list: list):
		"""
		Combines all images vertically, resizing photos to match the
		largest width image's width. Aspect ratio maintained.
		"""

		w_max = max(cls.matrix_width(im) for im in images_list)
		resized_list = [imutils.resize(im, w_max) for im in images_list]
		return cv2.vconcat(resized_list)


	@staticmethod
	def matrix_width(matrix: np.ndarray):
		"""Return width of a NumPy array (matrix).

		Returns the width element of the shape property of a
		numpy.ndarray.

		Args:
			matrix (ndarray):	The matrix to size.

		Returns:
			int:	The width.

		Examples:
			>>> Image_Concatenate.matrix_width(np.array([1,2,3,4]))
			4
			>>> Image_Concatenate.matrix_width(np.zeros((3,8,4)))
			3
			>>> Image_Concatenate.matrix_width(np.zeros((1,1)))
			1
		"""

		try:
			return matrix.shape[0]
		except IndexError:
			return 0

	@staticmethod
	def matrix_height(matrix):
		"""Return height of a NumPy array (matrix).

		Returns the height element of the shape property of a
		numpy.ndarray.

		Args:
			matrix (ndarray):	The matrix to size.

		Returns:
			int:	The height.

		Examples:
			>>> Image_Concatenate.matrix_height(np.array([1,2,3,4]))
			1
			>>> Image_Concatenate.matrix_height(np.zeros((3,8,4)))
			8
			>>> Image_Concatenate.matrix_height(np.zeros((1,1)))
			1
		"""
		try:
			return matrix.shape[1]
		except IndexError:
			return 1

	@staticmethod
	def matrix_depth(matrix):
		"""Return depth (3rd dimension) of a NumPy array (matrix).

		Returns the size of the 3rd dimension of a numpy.ndarray, as
		determined by its shape property.

		Args:
			matrix (ndarray):	The matrix to size.

		Returns:
			int:	The height.

		Examples:
			>>> Image_Concatenate.matrix_depth(np.array([1,2,3,4]))
			0
			>>> Image_Concatenate.matrix_depth(np.zeros((3,8,4)))
			4
			>>> Image_Concatenate.matrix_depth(np.zeros((1,1)))
			0
		"""
		try:
			return matrix.shape[2]
		except IndexError:
			return 0



# Activate doctests for when this file is run.
if __name__ == "__main__":
    import doctest
    doctest.testmod()