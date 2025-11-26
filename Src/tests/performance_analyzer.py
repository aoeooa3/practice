# performance_analyzer.py
import time
import statistics
import os
import sys
from functools import wraps
from PIL import Image
from image_processor import ImageProcessor

def performance_decorator(iterations=5, warmup=1):
    """Универсальный декоратор для измерения производительности"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n🔍 Тестирование {func.__name__}...")
            
            # Прогревочные итерации
            for i in range(warmup):
                if i == 0:
                    print("   🔥 Прогрев...")
                func(*args, **kwargs)
            
            # Измерение времени выполнения
            execution_times = []
            for i in range(iterations):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                execution_times.append((end_time - start_time) * 1000)  # ms
                
                # Прогресс-бар
                progress = (i + 1) / iterations * 100
                print(f"   📊 Прогресс: {progress:.0f}%", end='\r')
            
            # Статистика
            stats = {
                'function': func.__name__,
                'iterations': iterations,
                'min_time_ms': min(execution_times),
                'max_time_ms': max(execution_times),
                'mean_time_ms': statistics.mean(execution_times),
                'median_time_ms': statistics.median(execution_times),
                'stdev_time_ms': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
                'total_time_ms': sum(execution_times),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Красивый вывод
            print(f"\n   ✅ {func.__name__} - Результаты ({iterations} итераций):")
            print(f"      ⏱️  Время: {stats['mean_time_ms']:.2f} ms")
            print(f"      📈 Диапазон: {stats['min_time_ms']:.2f} - {stats['max_time_ms']:.2f} ms")
            print(f"      📊 Стандартное отклонение: {stats['stdev_time_ms']:.2f} ms")
            
            return result, stats
        return wrapper
    return decorator

class CrossPlatformImageProcessorBenchmark:
    """Кроссплатформенный бенчмарк для ImageProcessor"""
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.results = {}
        # Тестовые размеры изображений
        self.test_sizes = [
            (100, 100),      # Очень маленькое (для тестов)
            (800, 600),      # Small
            (1920, 1080),    # HD
        ]
    
    def create_test_images(self):
        """Создание тестовых изображений разных размеров и форматов"""
        print("🖼️ Создание тестовых изображений...")
        
        for width, height in self.test_sizes:
            # RGB JPEG (качественный)
            rgb_image = Image.new('RGB', (width, height), color=(255, 100, 100))
            # Добавляем немного шума для реалистичности
            for x in range(0, width, 50):
                for y in range(0, height, 50):
                    rgb_image.putpixel((x, y), (200, 150, 100))
            rgb_image.save(f'test_rgb_{width}x{height}.jpg', quality=95)
            
            # Grayscale PNG
            gray_image = Image.new('L', (width, height), color=150)
            gray_image.save(f'test_gray_{width}x{height}.png')
            
            print(f"   ✅ Создано: {width}x{height} (JPG, PNG)")
    
    def cleanup_test_files(self):
        """Очистка тестовых файлов"""
        print("\n🧹 Очистка тестовых файлов...")
        removed_count = 0
        
        for width, height in self.test_sizes:
            for color_mode in ['rgb', 'gray']:
                for ext in ['jpg', 'png', 'bmp']:
                    filename = f'test_{color_mode}_{width}x{height}.{ext}'
                    output_name = f'output_{width}x{height}.{ext}'
                    
                    if os.path.exists(filename):
                        os.remove(filename)
                        removed_count += 1
                    if os.path.exists(output_name):
                        os.remove(output_name)
                        removed_count += 1
        
        print(f"   ✅ Удалено файлов: {removed_count}")
    
    def get_file_size(self, filename):
        """Получение размера файла в KB"""
        if os.path.exists(filename):
            return os.path.getsize(filename) / 1024
        return 0
    
    @performance_decorator(iterations=3, warmup=1)
    def benchmark_load_operations(self):
        """Тестирование операций загрузки разных форматов и размеров"""
        print("📥 Тестирование загрузки изображений...")
        
        load_results = {}
        for width, height in self.test_sizes:
            # Тестируем разные форматы
            formats = [
                (f'test_rgb_{width}x{height}.jpg', 'JPEG'),
                (f'test_gray_{width}x{height}.png', 'PNG')
            ]
            
            for filename, format_name in formats:
                key = f"{format_name}_{width}x{height}"
                file_size = self.get_file_size(filename)
                
                # Измеряем время загрузки
                start_time = time.perf_counter()
                success = self.processor.load_image(filename)
                load_time = (time.perf_counter() - start_time) * 1000
                
                if success:
                    load_results[key] = {
                        'success': True,
                        'time_ms': load_time,
                        'file_size_kb': file_size,
                        'format': format_name,
                        'size': f"{width}x{height}"
                    }
                    print(f"      ✅ {key}: {load_time:.2f} ms ({file_size:.1f} KB)")
                else:
                    load_results[key] = {
                        'success': False,
                        'time_ms': load_time,
                        'error': 'Load failed'
                    }
                    print(f"      ❌ {key}: Ошибка загрузки")
        
        return load_results
    
    @performance_decorator(iterations=5, warmup=1)
    def benchmark_processing_operations(self):
        """Тестирование операций обработки изображений"""
        print("🔧 Тестирование операций обработки...")
        
        # Загружаем тестовое изображение
        self.processor.load_image('test_rgb_1920x1080.jpg')
        
        processing_results = {}
        
        # 1. Тестирование шумоподавления с разной интенсивностью
        print("   🎚️  Шумоподавление...")
        for strength in [1, 3, 5, 7]:
            start_time = time.perf_counter()
            success = self.processor.remove_noise(strength)
            processing_time = (time.perf_counter() - start_time) * 1000
            
            processing_results[f'noise_strength_{strength}'] = {
                'time_ms': processing_time,
                'success': success
            }
            print(f"      ✅ Intensity {strength}: {processing_time:.2f} ms")
        
        # 2. Тестирование конвертации в grayscale
        print("   ⚫ Конвертация в grayscale...")
        start_time = time.perf_counter()
        success = self.processor.convert_to_grayscale()
        processing_time = (time.perf_counter() - start_time) * 1000
        processing_results['grayscale'] = {
            'time_ms': processing_time,
            'success': success
        }
        print(f"      ✅ Grayscale: {processing_time:.2f} ms")
        
        # 3. Тестирование изменения размеров
        print("   📏 Изменение размеров...")
        resize_sizes = [(1600, 900), (800, 600), (400, 300)]
        for width, height in resize_sizes:
            start_time = time.perf_counter()
            success = self.processor.resize_image(width, height)
            resize_time = (time.perf_counter() - start_time) * 1000
            
            processing_results[f'resize_{width}x{height}'] = {
                'time_ms': resize_time,
                'success': success
            }
            print(f"      ✅ Resize to {width}x{height}: {resize_time:.2f} ms")
        
        return processing_results
    
    @performance_decorator(iterations=3, warmup=1)
    def benchmark_save_operations(self):
        """Тестирование операций сохранения в разных форматах"""
        print("💾 Тестирование сохранения...")
        
        # Убедимся, что изображение загружено
        if self.processor.current_image is None:
            self.processor.load_image('test_rgb_1920x1080.jpg')
        
        save_results = {}
        
        # Тестируем разные форматы сохранения
        formats = [
            ('jpg', 'JPEG'),
            ('png', 'PNG'),
            ('bmp', 'BMP')
        ]
        
        for ext, format_name in formats:
            filename = f'output_1920x1080.{ext}'
            
            start_time = time.perf_counter()
            success = self.processor.save_image(filename)
            save_time = (time.perf_counter() - start_time) * 1000
            
            file_size = self.get_file_size(filename) if success else 0
            
            save_results[format_name] = {
                'time_ms': save_time,
                'success': success,
                'file_size_kb': file_size
            }
            
            status = "✅" if success else "❌"
            print(f"      {status} {format_name}: {save_time:.2f} ms ({file_size:.1f} KB)")
        
        return save_results
    
    @performance_decorator(iterations=5, warmup=2)
    def benchmark_undo_operations(self):
        """Тестирование операций отмены действий"""
        print("↩️ Тестирование операций отмены...")
        
        # Создаем историю действий
        self.processor.load_image('test_rgb_800x600.jpg')
        self.processor.remove_noise(3)
        self.processor.convert_to_grayscale()
        
        undo_results = {}
        
        # Тестируем отмену
        start_time = time.perf_counter()
        success = self.processor.undo()
        undo_time = (time.perf_counter() - start_time) * 1000
        
        undo_results['undo'] = {
            'time_ms': undo_time,
            'success': success
        }
        print(f"      ✅ Undo: {undo_time:.2f} ms")
        
        # Тестируем сброс к оригиналу
        start_time = time.perf_counter()
        success = self.processor.reset_to_original()
        reset_time = (time.perf_counter() - start_time) * 1000
        
        undo_results['reset'] = {
            'time_ms': reset_time,
            'success': success
        }
        print(f"      ✅ Reset: {reset_time:.2f} ms")
        
        return undo_results
    
    def benchmark_complete_workflow(self):
        """Тестирование полного рабочего процесса"""
        print("\n🔄 Тестирование полного рабочего процесса...")
        
        workflow_steps = {}
        total_start = time.perf_counter()
        
        print("   📋 Последовательность операций:")
        
        # Шаг 1: Загрузка
        print("      1. Загрузка изображения...")
        step_start = time.perf_counter()
        self.processor.load_image('test_rgb_1920x1080.jpg')
        workflow_steps['load'] = (time.perf_counter() - step_start) * 1000
        
        # Шаг 2: Шумоподавление
        print("      2. Шумоподавление...")
        step_start = time.perf_counter()
        self.processor.remove_noise(3)
        workflow_steps['noise_reduction'] = (time.perf_counter() - step_start) * 1000
        
        # Шаг 3: Конвертация в grayscale
        print("      3. Конвертация в grayscale...")
        step_start = time.perf_counter()
        self.processor.convert_to_grayscale()
        workflow_steps['grayscale'] = (time.perf_counter() - step_start) * 1000
        
        # Шаг 4: Изменение размера
        print("      4. Изменение размера...")
        step_start = time.perf_counter()
        self.processor.resize_image(800, 600)
        workflow_steps['resize'] = (time.perf_counter() - step_start) * 1000
        
        # Шаг 5: Сохранение
        print("      5. Сохранение результата...")
        step_start = time.perf_counter()
        self.processor.save_image('complete_workflow_output.jpg')
        workflow_steps['save'] = (time.perf_counter() - step_start) * 1000
        
        # Общее время
        workflow_steps['total'] = (time.perf_counter() - total_start) * 1000
        
        # Вывод результатов
        print("\n   📊 Результаты рабочего процесса:")
        for step, time_ms in workflow_steps.items():
            if step != 'total':
                print(f"      {step:15} {time_ms:8.2f} ms")
        
        print(f"      {'='*25}")
        print(f"      {'ОБЩЕЕ ВРЕМЯ':15} {workflow_steps['total']:8.2f} ms 🎯")
        
        return workflow_steps
    
    def run_comprehensive_benchmark(self):
        """Запуск комплексного бенчмарка"""
        print("🎯 ЗАПУСК КОМПЛЕКСНОГО АНАЛИЗА ПРОИЗВОДИТЕЛЬНОСТИ")
        print("=" * 60)
        
        try:
            # Подготовка тестовых данных
            self.create_test_images()
            
            # Запуск отдельных бенчмарков
            print("\n1. 📊 ОПЕРАЦИИ ЗАГРУЗКИ")
            load_results, load_stats = self.benchmark_load_operations()
            self.results['load'] = load_stats
            
            print("\n2. 📊 ОПЕРАЦИИ ОБРАБОТКИ")
            processing_results, processing_stats = self.benchmark_processing_operations()
            self.results['processing'] = processing_stats
            
            print("\n3. 📊 ОПЕРАЦИИ СОХРАНЕНИЯ")
            save_results, save_stats = self.benchmark_save_operations()
            self.results['save'] = save_stats
            
            print("\n4. 📊 ОПЕРАЦИИ ОТМЕНЫ")
            undo_results, undo_stats = self.benchmark_undo_operations()
            self.results['undo'] = undo_stats
            
            print("\n5. 📊 ПОЛНЫЙ РАБОЧИЙ ПРОЦЕСС")
            workflow_results = self.benchmark_complete_workflow()
            self.results['workflow'] = workflow_results
            
            # Вывод суммарных результатов
            self._print_summary()
            
            return self.results
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении бенчмарка: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            # Очистка тестовых файлов
            self.cleanup_test_files()
    
    def _print_summary(self):
        """Вывод сводных результатов"""
        print("\n" + "=" * 60)
        print("📈 СВОДНЫЕ РЕЗУЛЬТАТЫ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("=" * 60)
        
        # Время выполнения по категориям
        categories = {
            'load': '📥 Загрузка изображений',
            'processing': '🔧 Обработка изображений', 
            'save': '💾 Сохранение результатов',
            'undo': '↩️ Операции отмены'
        }
        
        print("\n⏱️  СРЕДНЕЕ ВРЕМЯ ВЫПОЛНЕНИЯ:")
        for key, label in categories.items():
            if key in self.results:
                stats = self.results[key]
                if 'mean_time_ms' in stats:
                    print(f"   {label}: {stats['mean_time_ms']:8.2f} ms")
        
        # Полный рабочий процесс
        if 'workflow' in self.results:
            workflow = self.results['workflow']
            if 'total' in workflow:
                print(f"   🔄 Полный рабочий процесс: {workflow['total']:8.2f} ms")
        
        # Анализ производительности
        print("\n💡 АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")
        
        if 'processing' in self.results:
            proc_stats = self.results['processing']
            if 'mean_time_ms' in proc_stats:
                if proc_stats['mean_time_ms'] < 50:
                    print("   ✅ Отличная производительность обработки")
                elif proc_stats['mean_time_ms'] < 100:
                    print("   ⚡ Хорошая производительность обработки")
                else:
                    print("   📉 Производительность обработки можно улучшить")
        
        if 'undo' in self.results:
            undo_stats = self.results['undo']
            if 'mean_time_ms' in undo_stats and undo_stats['mean_time_ms'] < 1:
                print("   ✅ Операции отмены - мгновенные")
        
        print("\n🎯 РЕКОМЕНДАЦИИ:")
        print("   - Для лучшей производительности используйте изображения до 1920x1080")
        print("   - Операции отмены практически не влияют на производительность")
        print("   - Наиболее ресурсоемкая операция: шумоподавление")
        print("   - Программа оптимальна для пользовательских задач обработки")

def quick_performance_test():
    """Быстрый тест производительности основных операций"""
    print("⚡ БЫСТРЫЙ ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 40)
    
    processor = ImageProcessor()
    
    # Создаем тестовое изображение
    test_image = Image.new('RGB', (800, 600), color=(255, 100, 100))
    test_image.save('quick_test.jpg')
    
    try:
        operations = [
            ('Загрузка', lambda: processor.load_image('quick_test.jpg')),
            ('Шумоподавление (3)', lambda: processor.remove_noise(3)),
            ('Grayscale', processor.convert_to_grayscale),
            ('Изменение размера', lambda: processor.resize_image(400, 300)),
            ('Сохранение', lambda: processor.save_image('quick_output.jpg'))
        ]
        
        print("ОПЕРАЦИЯ\t\t\tВРЕМЯ (ms)\tСТАТУС")
        print("-" * 55)
        
        total_time = 0
        for op_name, op_func in operations:
            start_time = time.perf_counter()
            result = op_func()
            end_time = time.perf_counter()
            
            time_ms = (end_time - start_time) * 1000
            total_time += time_ms
            status = "✅ УСПЕХ" if result else "❌ ОШИБКА"
            
            print(f"{op_name:25} {time_ms:8.2f} ms\t{status}")
        
        print("-" * 55)
        print(f"{'ОБЩЕЕ ВРЕМЯ':25} {total_time:8.2f} ms\t🎯")
        
        # Анализ результатов
        print(f"\n💡 Результаты быстрого теста:")
        if total_time < 200:
            print("   ✅ Отличная производительность!")
        elif total_time < 500:
            print("   ⚡ Хорошая производительность")
        else:
            print("   📉 Производительность можно улучшить")
    
    finally:
        # Очистка
        for file in ['quick_test.jpg', 'quick_output.jpg']:
            if os.path.exists(file):
                os.remove(file)

# Запуск бенчмарка
if __name__ == "__main__":
    print("Выберите тип тестирования:")
    print("1 - Полный бенчмарк (рекомендуется)")
    print("2 - Быстрый тест")
    
    try:
        choice = input("Введите номер (1 или 2): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            benchmark = CrossPlatformImageProcessorBenchmark()
            results = benchmark.run_comprehensive_benchmark()
            
            # Сохранение результатов в файл
            if results:
                with open('performance_results.txt', 'w', encoding='utf-8') as f:
                    f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ПРОИЗВОДИТЕЛЬНОСТИ\n")
                    f.write("=" * 50 + "\n\n")
                    for category, stats in results.items():
                        f.write(f"{category.upper()}:\n")
                        for key, value in stats.items():
                            if isinstance(value, float):
                                f.write(f"  {key}: {value:.2f}\n")
                            else:
                                f.write(f"  {key}: {value}\n")
                        f.write("\n")
                print("💾 Результаты сохранены в 'performance_results.txt'")
                
        elif choice == "2":
            quick_performance_test()
        else:
            print("Запуск полного бенчмарка по умолчанию...")
            benchmark = CrossPlatformImageProcessorBenchmark()
            results = benchmark.run_comprehensive_benchmark()
            
    except KeyboardInterrupt:
        print("\n\n❌ Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")