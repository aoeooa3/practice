from PIL import Image, ImageFilter, ImageOps
import logging
import json
import os
from datetime import datetime

class ImageProcessor:
    """
    Модуль обработки и работы с изображениями для Проекта 5
    Использует только PIL (Pillow) - стандартную библиотеку для работы с изображениями
    """
    
    def __init__(self):
        self.current_image = None
        self.previous_image = None
        self.original_image = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Настройка логирования"""
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_image(self, image_path: str) -> bool:
        """Загрузка изображения с проверкой формата"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            # Проверка поддерживаемых форматов
            supported_formats = ('.png', '.jpg', '.jpeg', '.bmp')
            if not image_path.lower().endswith(supported_formats):
                raise ValueError(f"Неподдерживаемый формат: {image_path}")
            
            self.previous_image = self.current_image
            self.current_image = Image.open(image_path)
            self.original_image = self.current_image.copy()
            
            self.logger.info(f"Изображение загружено: {image_path}")
            self._log_user_action("load_image", {"path": image_path})
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка загрузки: {str(e)}")
            return False
    
    def remove_noise(self, strength: int = 3) -> bool:
        """
        Удаление шумов (лёгкое, один режим)
        strength: интенсивность шумоподавления (1-7)
        """
        try:
            if self.current_image is None:
                raise ValueError("Изображение не загружено")
            
            self.previous_image = self.current_image.copy()
            
            # Применение медианного фильтра для удаления шумов
            # Размер фильтра должен быть нечетным
            filter_size = max(1, min(7, strength))  # Ограничение 1-7
            if filter_size % 2 == 0:
                filter_size += 1
                
            self.current_image = self.current_image.filter(ImageFilter.MedianFilter(size=filter_size))
            
            self.logger.info(f"Шумоподавление применено: strength={filter_size}")
            self._log_user_action("remove_noise", {"strength": filter_size})
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка шумоподавления: {str(e)}")
            return False
    
    def convert_to_grayscale(self) -> bool:
        """Перевод в оттенки серого"""
        try:
            if self.current_image is None:
                raise ValueError("Изображение не загружено")
            
            self.previous_image = self.current_image.copy()
            self.current_image = ImageOps.grayscale(self.current_image)
            # Конвертируем обратно в RGB для единообразия
            self.current_image = self.current_image.convert('RGB')
            
            self.logger.info("Изображение преобразовано в оттенки серого")
            self._log_user_action("convert_to_grayscale", {})
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка конвертации: {str(e)}")
            return False
    
    def resize_image(self, width: int, height: int) -> bool:
        """Изменение разрешения изображения"""
        try:
            if self.current_image is None:
                raise ValueError("Изображение не загружено")
            
            if width <= 0 or height <= 0:
                raise ValueError("Размеры должны быть положительными")
            
            self.previous_image = self.current_image.copy()
            self.current_image = self.current_image.resize((width, height), Image.Resampling.LANCZOS)
            
            self.logger.info(f"Размер изменен: {width}x{height}")
            self._log_user_action("resize_image", {"width": width, "height": height})
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка изменения размера: {str(e)}")
            return False
    
    def get_image_info(self) -> dict:
        """Получение информации об изображении"""
        try:
            if self.current_image is None:
                return {}
            
            width, height = self.current_image.size
            
            info = {
                'width': width,
                'height': height,
                'format': self.current_image.format or 'Unknown',
                'mode': self.current_image.mode,
                'size': f"{width}x{height}"
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Ошибка получения информации: {str(e)}")
            return {}
    
    def save_image(self, output_path: str) -> bool:
        """Сохранение изображения в другом формате"""
        try:
            if self.current_image is None:
                raise ValueError("Нет изображения для сохранения")
            
            # Определяем формат из расширения файла
            format_map = {
                '.jpg': 'JPEG',
                '.jpeg': 'JPEG', 
                '.png': 'PNG',
                '.bmp': 'BMP'
            }
            ext = os.path.splitext(output_path)[1].lower()
            format_name = format_map.get(ext, 'JPEG')
            
            self.current_image.save(output_path, format=format_name)
            self.logger.info(f"Изображение сохранено: {output_path} ({format_name})")
            self._log_user_action("save_image", {"path": output_path, "format": format_name})
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка сохранения: {str(e)}")
            return False
    
    def undo(self) -> bool:
        """Отмена последнего действия"""
        if self.previous_image is not None:
            self.current_image = self.previous_image
            self.previous_image = None
            self.logger.info("Отмена последнего действия")
            self._log_user_action("undo", {})
            return True
        return False
    
    def reset_to_original(self) -> bool:
        """Сброс к исходному изображению"""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.previous_image = None
            self.logger.info("Сброс к исходному изображению")
            self._log_user_action("reset_to_original", {})
            return True
        return False
    
    def _log_user_action(self, operation: str, parameters: dict):
        """Логирование действий пользователя в JSON файл"""
        action_log = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "parameters": parameters
        }
        
        log_file = "logs/user_actions.json"
        logs = []
        
        # Чтение существующих логов
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Добавление новой записи
        logs.append(action_log)
        
        # Сохранение
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)