# test_basic.py - только 5 обязательных тестов
import os
import sys
from PIL import Image

sys.path.append(os.path.dirname(__file__))
from image_processor import ImageProcessor

def create_test_image():
    """Создание тестового изображения"""
    test_image = Image.new('RGB', (100, 100), color='red')
    test_image.save('test_image.jpg')
    return 'test_image.jpg'

def cleanup():
    """Очистка тестовых файлов"""
    for file in ['test_image.jpg', 'test_output.jpg']:
        if os.path.exists(file):
            os.remove(file)

# Тест 1: Загрузка изображения
def test1_load_image():
    image_path = create_test_image()
    processor = ImageProcessor()
    result = processor.load_image(image_path)
    assert result == True
    assert processor.current_image is not None
    print("✓ Тест 1: Загрузка изображения - ПРОЙДЕН")

# Тест 2: Удаление шумов  
def test2_remove_noise():
    image_path = create_test_image()
    processor = ImageProcessor()
    processor.load_image(image_path)
    result = processor.remove_noise(3)
    assert result == True
    print("✓ Тест 2: Удаление шумов - ПРОЙДЕН")

# Тест 3: Конвертация в оттенки серого
def test3_convert_to_grayscale():
    image_path = create_test_image()
    processor = ImageProcessor()
    processor.load_image(image_path)
    result = processor.convert_to_grayscale()
    assert result == True
    print("✓ Тест 3: Конвертация в оттенки серого - ПРОЙДЕН")

# Тест 4: Изменение размера
def test4_resize_image():
    image_path = create_test_image()
    processor = ImageProcessor()
    processor.load_image(image_path)
    result = processor.resize_image(50, 50)
    assert result == True
    assert processor.current_image.size == (50, 50)
    print("✓ Тест 4: Изменение размера - ПРОЙДЕН")

# Тест 5: Сохранение изображения
def test5_save_image():
    image_path = create_test_image()
    processor = ImageProcessor()
    processor.load_image(image_path)
    result = processor.save_image('test_output.jpg')
    assert result == True
    assert os.path.exists('test_output.jpg')
    print("✓ Тест 5: Сохранение изображения - ПРОЙДЕН")

# Запуск всех тестов
def main():
    print("ЗАПУСК 5 ОБЯЗАТЕЛЬНЫХ ТЕСТОВ")
    print("=" * 40)
    
    tests = [
        test1_load_image,
        test2_remove_noise, 
        test3_convert_to_grayscale,
        test4_resize_image,
        test5_save_image
    ]
    
    try:
        for test in tests:
            test()
        
        print("=" * 40)
        print("✅ ВСЕ 5 ТЕСТОВ УСПЕШНО ПРОЙДЕНЫ!")
        
    except Exception as e:
        print(f"❌ Тест не пройден: {e}")
    finally:
        cleanup()

if __name__ == "__main__":
    main()