import unittest
import numpy.testing as npt
import cv2
# Add one directory up to pull in helpers
import sys
sys.path.append('..')
#from pprint import pprint as var_dump

import src.python.jtm_opencv_helpers as JOH
from src.python.jtm_opencv_helpers import Image_Concatenate as Im_Concat


class LP_Tests(unittest.TestCase):
	def setUp(self):
		# Set to True to save images created during testing
		# to test directory. Helpful for debugging failed tests.
		self.save_images = False

	def test_create_blank_image_bgr(self):
		im = JOH.create_blank_image(100, 200, (50,100,150))

		if self.save_images:
			cv2.imwrite('test_create_blank_image_bgr.jpg', im)

		(h,w,d) = im.shape
		random_value = im[27,47]

		self.assertEqual(w, 100, "Width different than specified.")
		self.assertEqual(h, 200, "Height different than specified.")
		self.assertEqual(d, 3, "Color channels different than specified.")
		npt.assert_array_equal(random_value, (50,100,150),
			"Color different than specified.")

	def test_create_blank_image_grayscale(self):
		im = JOH.create_blank_image(100, 200, 200)

		if self.save_images:
			cv2.imwrite('test_create_blank_image_grayscale.jpg', im)

		(h,w) = im.shape
		random_value = im[27,47]

		self.assertEqual(w, 100, "Width different than specified.")
		self.assertEqual(h, 200, "Height different than specified.")
		self.assertEqual(random_value, 200, "Color different than specified.")

	def test_concat_horizontal_and_cut_larger(self):
		im1 = JOH.create_blank_image(100, 200, 0)
		im2 = JOH.create_blank_image(200, 300, 128)
		im3 = JOH.create_blank_image(300, 400, 255)

		cim = Im_Concat.horizontal_and_cut_larger((im1, im2, im3))

		if self.save_images:
			cv2.imwrite('test_concat_horizontal_and_cut_larger.jpg', cim)

		(h,w) = cim.shape
		im1_val = cim[50,50]
		im2_val = cim[50,150]
		im3_val = cim[50,500]


		self.assertEqual(h, 200, "Height should be equal to smallest height.")
		self.assertEqual(w, 600, "Width should be sum of widths.")
		self.assertEqual(im1_val, 0, "This should be region of image 1.")
		self.assertEqual(im2_val, 128, "This should be region of image 2.")
		self.assertEqual(im3_val, 255, "This should be region of image 3.")

	def test_concat_vertical_and_cut_larger(self):
		im1 = JOH.create_blank_image(200, 100, 0)
		im2 = JOH.create_blank_image(300, 200, 128)
		im3 = JOH.create_blank_image(400, 300, 255)

		cim = Im_Concat.vertical_and_cut_larger((im1, im2, im3))

		if self.save_images:
			cv2.imwrite('test_concat_vertical_and_cut_larger.jpg', cim)

		(h,w) = cim.shape
		im1_val = cim[50,50]
		im2_val = cim[150,50]
		im3_val = cim[500,50]


		self.assertEqual(h, 600, "Height should be sum of heights.")
		self.assertEqual(w, 200, "Width should be equal to smallest width.")
		self.assertEqual(im1_val, 0, "This should be region of image 1.")
		self.assertEqual(im2_val, 128, "This should be region of image 2.")
		self.assertEqual(im3_val, 255, "This should be region of image 3.")

	def test_concat_horizontal_and_fill_empty(self):
		im1 = JOH.create_blank_image(100, 200, (0,0,0))
		im2 = JOH.create_blank_image(200, 300, (128,128,128))
		im3 = JOH.create_blank_image(300, 400, (255,255,255))

		cim = Im_Concat.horizontal_and_fill_empty((im1, im2, im3),
			(255,128,0))

		if self.save_images:
			cv2.imwrite('test_concat_horizontal_and_fill_empty.jpg', cim)

		(h,w,d) = cim.shape
		im1_val = cim[50,50]
		im2_val = cim[50,150]
		im3_val = cim[50,500]
		pad_val = cim[200,50]


		self.assertEqual(h, 400, "Height should be equal to largest.")
		self.assertEqual(w, 600, "Width should be equal to sum of widths.")
		npt.assert_array_equal(im1_val, (0,0,0),
			"This should be region of image 1.")
		npt.assert_array_equal(im2_val, (128,128,128),
			"This should be region of image 2.")
		npt.assert_array_equal(im3_val, (255,255,255),
			"This should be region of image 3.")
		npt.assert_array_equal(pad_val, (255,128,0),
			"This should be padded region of image.")

	def test_concat_vertical_and_fill_empty(self):
		im1 = JOH.create_blank_image(200, 100, (0,0,0))
		im2 = JOH.create_blank_image(300, 200, (128,128,128))
		im3 = JOH.create_blank_image(400, 300, (255,255,255))

		cim = Im_Concat.vertical_and_fill_empty((im1, im2, im3),
			(255,128,0))

		if self.save_images:
			cv2.imwrite('test_concat_vertical_and_fill_empty.jpg', cim)

		(h,w,d) = cim.shape
		im1_val = cim[50,50]
		im2_val = cim[150,50]
		im3_val = cim[400,50]
		pad_val = cim[50,200]


		self.assertEqual(h, 600, "Height should be equal to sum of heights.")
		self.assertEqual(w, 400, "Width should be equal to largest.")
		npt.assert_array_equal(im1_val, (0,0,0),
			"This should be region of image 1.")
		npt.assert_array_equal(im2_val, (128,128,128),
			"This should be region of image 2.")
		npt.assert_array_equal(im3_val, (255,255,255),
			"This should be region of image 3.")
		npt.assert_array_equal(pad_val, (255,128,0),
			"This should be padded region of image.")




# Activate unittests for when this file is run.
if __name__ == "__main__":
    unittest.main()