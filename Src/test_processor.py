import unittest
import os
from PIL import Image
from image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    """Тесты для модуля обработки изображений"""
    
    def setUp(self):
        self.processor = ImageProcessor()
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.test_image.save('test_image.jpg')
    
    def tearDown(self):
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')
        if os.path.exists('test_output.jpg'):
            os.remove('test_output.jpg')
    
    def test_load_image(self):
        result = self.processor.load_image('test_image.jpg')
        self.assertTrue(result)
        self.assertIsNotNone(self.processor.current_image)
    
    def test_remove_noise(self):
        self.processor.load_image('test_image.jpg')
        result = self.processor.remove_noise(3)
        self.assertTrue(result)
    
    def test_convert_to_grayscale(self):
        self.processor.load_image('test_image.jpg')
        result = self.processor.convert_to_grayscale()
        self.assertTrue(result)
    
    def test_resize_image(self):
        self.processor.load_image('test_image.jpg')
        result = self.processor.resize_image(50, 50)
        self.assertTrue(result)
        info = self.processor.get_image_info()
        self.assertEqual(info['width'], 50)
    
    def test_save_image(self):
        self.processor.load_image('test_image.jpg')
        result = self.processor.save_image('test_output.jpg')
        self.assertTrue(result)
        self.assertTrue(os.path.exists('test_output.jpg'))

if __name__ == '__main__':
    unittest.main()