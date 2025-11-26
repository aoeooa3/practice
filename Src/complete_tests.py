import unittest
import time
import os
import sys
import statistics
from PIL import Image

# Добавляем путь к модулю обработки изображений
sys.path.append(os.path.dirname(__file__))
from image_processor import ImageProcessor

# =============================================================================
# БАЗОВЫЕ ФУНКЦИИ ДЛЯ ТЕСТИРОВАНИЯ
# =============================================================================

def create_test_image(width=100, height=100, color='red', filename=None):
    """Создание тестового изображения"""
    if filename is None:
        filename = f'test_image_{width}x{height}.jpg'
    
    test_image = Image.new('RGB', (width, height), color=color)
    test_image.save(filename)
    return filename

def cleanup_files():
    """Очистка тестовых файлов"""
    files_to_remove = []
    for file in os.listdir('.'):
        if (file.startswith('test_') and 
            (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.bmp'))):
            files_to_remove.append(file)
    
    for file in files_to_remove:
        try:
            os.remove(file)
        except:
            pass

def measure_time(func, *args, iterations=5):
    """Измерение времени выполнения функции"""
    times = []
    
    for i in range(iterations):
        start_time = time.time()
        result = func(*args)
        end_time = time.time()
        
        if result:  # Если функция выполнилась успешно
            execution_time = (end_time - start_time) * 1000  # в миллисекундах
            times.append(execution_time)
    
    if times:
        return {
            'min': min(times),
            'max': max(times),
            'avg': statistics.mean(times),
            'median': statistics.median(times),
            'all_times': times
        }
    else:
        return None

# =============================================================================
# 5 ОСНОВНЫХ МОДУЛЬНЫХ ТЕСТОВ (требование задания)
# =============================================================================

def test1_load_image():
    """Тест 1: Загрузка изображения"""
    print("=== Тест 1: Загрузка изображения ===")
    
    image_path = create_test_image(100, 100, 'red')
    processor = ImageProcessor()
    result = processor.load_image(image_path)
    
    # Проверяем результаты
    assert result == True, "Ошибка загрузки изображения"
    assert processor.current_image is not None, "Изображение не загружено"
    assert processor.original_image is not None, "Оригинальное изображение не сохранено"
    
    print("✓ Тест пройден: изображение успешно загружено")
    return True

def test2_remove_noise():
    """Тест 2: Удаление шумов"""
    print("\n=== Тест 2: Удаление шумов ===")
    
    image_path = create_test_image(100, 100, 'red')
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    # Сохраняем исходное состояние
    original_size = processor.current_image.size
    
    # Применяем шумоподавление
    result = processor.remove_noise(3)
    
    # Проверяем результаты
    assert result == True, "Ошибка шумоподавления"
    assert processor.current_image is not None, "Изображение потеряно после шумоподавления"
    assert processor.current_image.size == original_size, "Размер изображения изменился после шумоподавления"
    
    print("✓ Тест пройден: шумоподавление работает корректно")
    return True

def test3_convert_to_grayscale():
    """Тест 3: Конвертация в оттенки серого"""
    print("\n=== Тест 3: Конвертация в оттенки серого ===")
    
    image_path = create_test_image(100, 100, 'red')
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    # Применяем конвертацию
    result = processor.convert_to_grayscale()
    
    # Проверяем результаты
    assert result == True, "Ошибка конвертации в оттенки серого"
    assert processor.current_image is not None, "Изображение потеряно после конвертации"
    assert processor.current_image.mode == 'RGB', "Режим изображения не корректен после конвертации"
    
    print("✓ Тест пройден: конвертация в оттенки серого работает корректно")
    return True

def test4_resize_image():
    """Тест 4: Изменение размера изображения"""
    print("\n=== Тест 4: Изменение размера изображения ===")
    
    image_path = create_test_image(100, 100, 'red')
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    # Изменяем размер
    new_width, new_height = 50, 50
    result = processor.resize_image(new_width, new_height)
    
    # Проверяем результаты
    assert result == True, "Ошибка изменения размера"
    assert processor.current_image is not None, "Изображение потеряно после изменения размера"
    assert processor.current_image.size == (new_width, new_height), f"Размер не соответствует ожидаемому: {processor.current_image.size}"
    
    print("✓ Тест пройден: изменение размера работает корректно")
    return True

def test5_save_image():
    """Тест 5: Сохранение изображения"""
    print("\n=== Тест 5: Сохранение изображения ===")
    
    image_path = create_test_image(100, 100, 'red')
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    # Сохраняем изображение
    output_path = 'test_output.jpg'
    result = processor.save_image(output_path)
    
    # Проверяем результаты
    assert result == True, "Ошибка сохранения изображения"
    assert os.path.exists(output_path), "Файл не создан"
    
    # Проверяем что файл можно загрузить
    saved_image = Image.open(output_path)
    assert saved_image is not None, "Сохраненный файл поврежден"
    
    print("✓ Тест пройден: сохранение изображения работает корректно")
    return True

# =============================================================================
# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ
# =============================================================================

def test6_get_image_info():
    """Тест 6: Получение информации об изображении"""
    print("\n=== Тест 6: Получение информации об изображении ===")
    
    image_path = create_test_image(150, 200, 'blue')
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    # Получаем информацию
    info = processor.get_image_info()
    
    # Проверяем результаты
    assert info is not None, "Информация не получена"
    assert 'width' in info, "Отсутствует информация о ширине"
    assert 'height' in info, "Отсутствует информация о высоте"
    assert info['width'] == 150, f"Неверная ширина: {info['width']}"
    assert info['height'] == 200, f"Неверная высота: {info['height']}"
    
    print("✓ Тест пройден: получение информации работает корректно")
    return True

def test7_undo_action():
    """Тест 7: Отмена действия"""
    print("\n=== Тест 7: Отмена действия ===")
    
    image_path = create_test_image(100, 100, 'green')
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    # Запоминаем исходное состояние
    original_size = processor.current_image.size
    
    # Выполняем действие (изменяем размер)
    processor.resize_image(50, 50)
    
    # Проверяем что размер изменился
    assert processor.current_image.size == (50, 50), "Размер не изменился"
    
    # Отменяем действие
    result = processor.undo()
    
    # Проверяем что действие отменено
    assert result == True, "Ошибка отмены действия"
    assert processor.current_image.size == original_size, "Размер не вернулся к исходному"
    
    print("✓ Тест пройден: отмена действия работает корректно")
    return True

def test8_error_handling():
    """Тест 8: Обработка ошибок"""
    print("\n=== Тест 8: Обработка ошибок ===")
    
    processor = ImageProcessor()
    
    # Пытаемся загрузить несуществующий файл
    result = processor.load_image('non_existent_file.jpg')
    assert result == False, "Должна быть ошибка при загрузке несуществующего файла"
    
    # Пытаемся загрузить файл неподдерживаемого формата
    with open('test_file.txt', 'w') as f:
        f.write('not an image')
    
    result = processor.load_image('test_file.txt')
    assert result == False, "Должна быть ошибка при загрузке неподдерживаемого формата"
    
    # Очистка
    if os.path.exists('test_file.txt'):
        os.remove('test_file.txt')
    
    print("✓ Тест пройден: обработка ошибок работает корректно")
    return True

# =============================================================================
# ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ (СКОРОСТИ)
# =============================================================================

def speed_test_load():
    """Тест скорости загрузки изображений разных размеров"""
    print("\n=== ТЕСТ СКОРОСТИ ЗАГРУЗКИ ИЗОБРАЖЕНИЙ ===")
    
    image_sizes = [
        (640, 480),    # VGA
        (1280, 720),   # HD
        (1920, 1080),  # Full HD
    ]
    
    results = {}
    
    for width, height in image_sizes:
        image_path = create_test_image(width, height)
        processor = ImageProcessor()
        
        # Измеряем время загрузки
        time_info = measure_time(processor.load_image, image_path, iterations=3)
        
        if time_info:
            results[f"{width}x{height}"] = time_info
            print(f"{width}x{height}: {time_info['avg']:.2f} мс "
                  f"(min: {time_info['min']:.2f}, max: {time_info['max']:.2f})")
    
    return results

def speed_test_noise_removal():
    """Тест скорости шумоподавления"""
    print("\n=== ТЕСТ СКОРОСТИ ШУМОПОДАВЛЕНИЯ ===")
    
    image_path = create_test_image(1280, 720)
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    noise_levels = [1, 3, 5]
    results = {}
    
    for strength in noise_levels:
        time_info = measure_time(processor.remove_noise, strength, iterations=3)
        
        if time_info:
            results[f"strength_{strength}"] = time_info
            print(f"Шумоподавление {strength}: {time_info['avg']:.2f} мс "
                  f"(min: {time_info['min']:.2f}, max: {time_info['max']:.2f})")
    
    return results

def speed_test_grayscale():
    """Тест скорости конвертации в оттенки серого"""
    print("\n=== ТЕСТ СКОРОСТИ КОНВЕРТАЦИИ В ОТТЕНКИ СЕРОГО ===")
    
    image_sizes = [
        (640, 480),
        (1280, 720), 
    ]
    
    results = {}
    
    for width, height in image_sizes:
        image_path = create_test_image(width, height)
        processor = ImageProcessor()
        processor.load_image(image_path)
        
        time_info = measure_time(processor.convert_to_grayscale, iterations=3)
        
        if time_info:
            results[f"grayscale_{width}x{height}"] = time_info
            print(f"Серый {width}x{height}: {time_info['avg']:.2f} мс "
                  f"(min: {time_info['min']:.2f}, max: {time_info['max']:.2f})")
    
    return results

def speed_test_resize():
    """Тест скорости изменения размера"""
    print("\n=== ТЕСТ СКОРОСТИ ИЗМЕНЕНИЯ РАЗМЕРА ===")
    
    image_path = create_test_image(1280, 720)
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    target_sizes = [
        (800, 600),
        (1920, 1080),
    ]
    
    results = {}
    
    for width, height in target_sizes:
        time_info = measure_time(processor.resize_image, width, height, iterations=3)
        
        if time_info:
            results[f"resize_to_{width}x{height}"] = time_info
            print(f"Размер -> {width}x{height}: {time_info['avg']:.2f} мс "
                  f"(min: {time_info['min']:.2f}, max: {time_info['max']:.2f})")
    
    return results

def speed_test_save():
    """Тест скорости сохранения"""
    print("\n=== ТЕСТ СКОРОСТИ СОХРАНЕНИЯ ===")
    
    image_path = create_test_image(1280, 720)
    processor = ImageProcessor()
    processor.load_image(image_path)
    
    formats = [
        ('test_output.jpg', 'JPEG'),
        ('test_output.png', 'PNG'),
    ]
    
    results = {}
    
    for filename, format_name in formats:
        time_info = measure_time(processor.save_image, filename, iterations=3)
        
        if time_info:
            results[format_name] = time_info
            print(f"Сохранение {format_name}: {time_info['avg']:.2f} мс "
                  f"(min: {time_info['min']:.2f}, max: {time_info['max']:.2f})")
    
    return results

def speed_test_complete_workflow():
    """Тест скорости полного рабочего процесса"""
    print("\n=== ТЕСТ СКОРОСТИ ПОЛНОГО РАБОЧЕГО ПРОЦЕССА ===")
    
    def complete_workflow():
        processor = ImageProcessor()
        processor.load_image('test_workflow.jpg')
        processor.remove_noise(3)
        processor.convert_to_grayscale()
        processor.resize_image(800, 600)
        processor.save_image('test_workflow_output.jpg')
    
    # Создаем тестовое изображение
    create_test_image(1280, 720, 'blue', 'test_workflow.jpg')
    
    time_info = measure_time(complete_workflow, iterations=3)
    
    if time_info:
        print(f"Полный рабочий процесс: {time_info['avg']:.2f} мс "
              f"(min: {time_info['min']:.2f}, max: {time_info['max']:.2f})")
    
    # Очистка
    for file in ['test_workflow.jpg', 'test_workflow_output.jpg']:
        if os.path.exists(file):
            os.remove(file)
    
    return time_info

# =============================================================================
# ФУНКЦИИ ЗАПУСКА ТЕСТОВ
# =============================================================================

def run_basic_tests():
    """Запуск 5 основных тестов (требование задания)"""
    print("🧪 ЗАПУСК 5 ОСНОВНЫХ МОДУЛЬНЫХ ТЕСТОВ")
    print("=" * 50)
    
    basic_tests = [
        test1_load_image,
        test2_remove_noise,
        test3_convert_to_grayscale,
        test4_resize_image,
        test5_save_image
    ]
    
    passed = 0
    failed = 0
    
    for test in basic_tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Тест {test.__name__} упал с ошибкой: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ОСНОВНЫХ ТЕСТОВ:")
    print(f"Пройдено: {passed}/5")
    print(f"Не пройдено: {failed}/5")
    
    return passed == 5

def run_additional_tests():
    """Запуск дополнительных тестов"""
    print("\n🔧 ЗАПУСК ДОПОЛНИТЕЛЬНЫХ ТЕСТОВ")
    print("=" * 50)
    
    additional_tests = [
        test6_get_image_info,
        test7_undo_action,
        test8_error_handling
    ]
    
    passed = 0
    total = len(additional_tests)
    
    for test in additional_tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Тест {test.__name__} упал с ошибкой: {e}")
    
    print(f"\nДополнительные тесты: {passed}/{total} пройдено")
    return passed

def run_speed_tests():
    """Запуск тестов производительности"""
    print("\n⚡ ЗАПУСК ТЕСТОВ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 50)
    
    speed_tests = [
        speed_test_load,
        speed_test_noise_removal,
        speed_test_grayscale,
        speed_test_resize,
        speed_test_save,
        speed_test_complete_workflow
    ]
    
    results = {}
    
    for test in speed_tests:
        try:
            test_name = test.__name__.replace('speed_test_', '')
            results[test_name] = test()
        except Exception as e:
            print(f"Ошибка в тесте {test.__name__}: {e}")
    
    return results

def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 ПОЛНОЕ ТЕСТИРОВАНИЕ МОДУЛЯ ОБРАБОТКИ ИЗОБРАЖЕНИЙ")
    print("=" * 60)
    
    # Запускаем основные тесты
    basic_success = run_basic_tests()
    
    # Запускаем дополнительные тесты
    additional_passed = run_additional_tests()
    
    # Запускаем тесты производительности
    speed_results = run_speed_tests()
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    if basic_success:
        print("✅ 5 ОСНОВНЫХ ТЕСТОВ: ПРОЙДЕНЫ")
    else:
        print("❌ 5 ОСНОВНЫХ ТЕСТОВ: НЕ ПРОЙДЕНЫ")
    
    print(f"📈 ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ: {additional_passed}/3 пройдено")
    print("⚡ ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ: ВЫПОЛНЕНЫ")
    
    # Рекомендации по производительности
    print("\n💡 РЕКОМЕНДАЦИИ:")
    if speed_results.get('noise_removal'):
        avg_time = list(speed_results['noise_removal'].values())[0]['avg']
        if avg_time > 100:
            print("- Шумоподавление занимает много времени, используйте меньшую интенсивность")
    
    if speed_results.get('complete_workflow'):
        workflow_time = speed_results['complete_workflow']['avg']
        print(f"- Полный рабочий процесс занимает {workflow_time:.2f} мс")
    
    # Очистка
    cleanup_files()
    
    return basic_success

def run_quick_test():
    """Быстрый тест (только основные 5 тестов)"""
    print("⚡ БЫСТРОЕ ТЕСТИРОВАНИЕ - 5 ОСНОВНЫХ ТЕСТОВ")
    print("=" * 50)
    
    tests = [
        test1_load_image,
        test2_remove_noise,
        test3_convert_to_grayscale,
        test4_resize_image,
        test5_save_image
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Ошибка в тесте: {e}")
    
    print(f"\nРезультат: {passed}/5 тестов пройдено")
    cleanup_files()
    return passed == 5

# =============================================================================
# UNITTEST КЛАССЫ (для совместимости)
# =============================================================================

class TestImageProcessorUnittest(unittest.TestCase):
    """Тесты в стиле unittest для совместимости"""
    
    def setUp(self):
        self.image_path = create_test_image(100, 100, 'red')
        self.processor = ImageProcessor()
    
    def tearDown(self):
        cleanup_files()
    
    def test_load_image(self):
        result = self.processor.load_image(self.image_path)
        self.assertTrue(result)
        self.assertIsNotNone(self.processor.current_image)
    
    def test_remove_noise(self):
        self.processor.load_image(self.image_path)
        result = self.processor.remove_noise(3)
        self.assertTrue(result)
    
    def test_convert_to_grayscale(self):
        self.processor.load_image(self.image_path)
        result = self.processor.convert_to_grayscale()
        self.assertTrue(result)
    
    def test_resize_image(self):
        self.processor.load_image(self.image_path)
        result = self.processor.resize_image(50, 50)
        self.assertTrue(result)
        self.assertEqual(self.processor.current_image.size, (50, 50))
    
    def test_save_image(self):
        self.processor.load_image(self.image_path)
        result = self.processor.save_image('test_unittest_output.jpg')
        self.assertTrue(result)
        self.assertTrue(os.path.exists('test_unittest_output.jpg'))

# =============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# =============================================================================

def main():
    """Главная функция для запуска тестов"""
    print("ТЕСТИРОВАНИЕ МОДУЛЯ ОБРАБОТКИ ИЗОБРАЖЕНИЙ")
    print("=" * 50)
    print("Выберите тип тестирования:")
    print("1 - Полное тестирование (все тесты)")
    print("2 - Только 5 основных тестов")
    print("3 - Только тесты производительности") 
    print("4 - Unittest стиль")
    print("5 - Быстрый тест")
    
    try:
        choice = input("Введите номер (1-5): ").strip()
    except:
        choice = "1"  # По умолчанию полное тестирование
    
    if choice == "1":
        success = run_all_tests()
        exit(0 if success else 1)
    elif choice == "2":
        success = run_basic_tests()
        cleanup_files()
        exit(0 if success else 1)
    elif choice == "3":
        run_speed_tests()
        cleanup_files()
    elif choice == "4":
        print("\nЗапуск тестов в стиле unittest...")
        unittest.main(argv=[''], exit=False)
        cleanup_files()
    elif choice == "5":
        success = run_quick_test()
        exit(0 if success else 1)
    else:
        print("Неверный выбор. Запуск полного тестирования...")
        success = run_all_tests()
        exit(0 if success else 1)

if __name__ == "__main__":
    main()