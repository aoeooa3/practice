import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from PIL import Image, ImageTk
from image_processor import ImageProcessor

class ImageProcessorUI:
    """
    Модуль взаимодействия с пользователем (UI)
    Графический интерфейс для Проекта 5
    """
    
    def __init__(self, root):
        self.root = root
        self.processor = ImageProcessor()
        self.setup_ui()
        self.load_settings()
        self.create_directories()
    
    def create_directories(self):
        """Автоматическое создание служебных папок при первом запуске"""
        for folder in ['logs', 'config', 'output']:
            os.makedirs(folder, exist_ok=True)
    
    def setup_ui(self):
        """Настройка графического интерфейса"""
        self.root.title("Image Processor - Проект 5")
        self.root.geometry("1000x700")
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Обработчик изображений - Проект 5", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Основная область контента
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель - изображения
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Исходное изображение
        original_frame = ttk.LabelFrame(left_frame, text="Исходное изображение", padding="5")
        original_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.original_label = ttk.Label(original_frame, 
                                       text="Загрузите изображение\n\nНажмите кнопку 'Загрузить изображение'",
                                       background='white', 
                                       anchor='center',
                                       justify='center')
        self.original_label.pack(fill=tk.BOTH, expand=True)
        
        # Обработанное изображение
        processed_frame = ttk.LabelFrame(left_frame, text="Обработанное изображение", padding="5")
        processed_frame.pack(fill=tk.BOTH, expand=True)
        
        self.processed_label = ttk.Label(processed_frame, 
                                        text="Здесь будет отображаться результат обработки",
                                        background='white', 
                                        anchor='center',
                                        justify='center')
        self.processed_label.pack(fill=tk.BOTH, expand=True)
        
        # Правая панель - управление и информация
        right_frame = ttk.Frame(content_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Панель управления
        control_frame = ttk.LabelFrame(right_frame, text="Управление", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(control_frame, text="Загрузить изображение", 
                  command=self.load_image_dialog).pack(fill=tk.X, pady=2)
        
        ttk.Button(control_frame, text="Сохранить результат", 
                  command=self.save_image_dialog).pack(fill=tk.X, pady=2)
        
        ttk.Button(control_frame, text="Отменить действие", 
                  command=self.undo_action).pack(fill=tk.X, pady=2)
        
        ttk.Button(control_frame, text="Сбросить к исходному", 
                  command=self.reset_to_original).pack(fill=tk.X, pady=2)
        
        # Настройка шумоподавления
        noise_frame = ttk.LabelFrame(right_frame, text="Настройка шумоподавления", padding="10")
        noise_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(noise_frame, text="Интенсивность:").pack(anchor=tk.W)
        
        self.noise_var = tk.IntVar(value=3)
        noise_scale = ttk.Scale(noise_frame, from_=1, to=7, 
                               variable=self.noise_var, orient=tk.HORIZONTAL)
        noise_scale.pack(fill=tk.X, pady=5)
        
        noise_value_frame = ttk.Frame(noise_frame)
        noise_value_frame.pack(fill=tk.X)
        
        ttk.Label(noise_value_frame, text="Текущее значение:").pack(side=tk.LEFT)
        self.noise_value_label = ttk.Label(noise_value_frame, text="3")
        self.noise_value_label.pack(side=tk.RIGHT)
        
        ttk.Button(noise_frame, text="Применить шумоподавление", 
                  command=self.apply_noise_reduction).pack(fill=tk.X, pady=5)
        
        # Преобразования изображения
        transform_frame = ttk.LabelFrame(right_frame, text="Преобразования", padding="10")
        transform_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(transform_frame, text="Перевести в оттенки серого", 
                  command=self.apply_grayscale).pack(fill=tk.X, pady=2)
        
        # Изменение размера
        resize_frame = ttk.LabelFrame(transform_frame, text="Изменение размера", padding="5")
        resize_frame.pack(fill=tk.X, pady=5)
        
        # Ширина
        width_frame = ttk.Frame(resize_frame)
        width_frame.pack(fill=tk.X, pady=2)
        ttk.Label(width_frame, text="Ширина:").pack(side=tk.LEFT)
        self.width_var = tk.StringVar(value="800")
        width_entry = ttk.Entry(width_frame, textvariable=self.width_var, width=8)
        width_entry.pack(side=tk.RIGHT)
        
        # Высота
        height_frame = ttk.Frame(resize_frame)
        height_frame.pack(fill=tk.X, pady=2)
        ttk.Label(height_frame, text="Высота:").pack(side=tk.LEFT)
        self.height_var = tk.StringVar(value="600")
        height_entry = ttk.Entry(height_frame, textvariable=self.height_var, width=8)
        height_entry.pack(side=tk.RIGHT)
        
        ttk.Button(resize_frame, text="Изменить размер", 
                  command=self.apply_resize).pack(fill=tk.X, pady=5)
        
        # Информация об изображении
        info_frame = ttk.LabelFrame(right_frame, text="Информация об изображении", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(info_frame, height=8, wrap=tk.WORD, font=('Arial', 9))
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Начальный текст информации
        self.info_text.insert(1.0, "Загрузите изображение для просмотра информации")
        
        # Привязка событий
        self.noise_var.trace('w', self.on_noise_change)
    
    def on_noise_change(self, *args):
        """Обновление значения шумоподавления"""
        self.noise_value_label.config(text=str(self.noise_var.get()))
    
    def load_image_dialog(self):
        """Диалог загрузки изображения"""
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Все поддерживаемые", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """Загрузка и отображение изображения"""
        if self.processor.load_image(file_path):
            self.display_images()
            self.update_info()
            self.save_settings()
            messagebox.showinfo("Успех", "Изображение успешно загружено!")
        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение!\nПроверьте формат файла.")
    
    def display_images(self):
        """Отображение исходного и обработанного изображений"""
        # Отображение исходного изображения
        if self.processor.original_image is not None:
            img = self.processor.original_image.copy()
            img.thumbnail((400, 300))
            img_tk = ImageTk.PhotoImage(img)
            
            self.original_label.configure(image=img_tk, text="")
            self.original_label.image = img_tk
        
        # Отображение обработанного изображения
        if self.processor.current_image is not None:
            img = self.processor.current_image.copy()
            img.thumbnail((400, 300))
            img_tk = ImageTk.PhotoImage(img)
            
            self.processed_label.configure(image=img_tk, text="")
            self.processed_label.image = img_tk
    
    def apply_noise_reduction(self):
        """Применение шумоподавления"""
        if self.processor.current_image is not None:
            strength = self.noise_var.get()
            if self.processor.remove_noise(strength):
                self.display_images()
                self.update_info()
                messagebox.showinfo("Успех", "Шумоподавление применено!")
            else:
                messagebox.showerror("Ошибка", "Не удалось применить шумоподавление")
        else:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
    
    def apply_grayscale(self):
        """Применение преобразования в оттенки серого"""
        if self.processor.current_image is not None:
            if self.processor.convert_to_grayscale():
                self.display_images()
                self.update_info()
                messagebox.showinfo("Успех", "Изображение преобразовано в оттенки серого!")
            else:
                messagebox.showerror("Ошибка", "Не удалось преобразовать изображение")
        else:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
    
    def apply_resize(self):
        """Изменение размера изображения"""
        if self.processor.current_image is not None:
            try:
                width = int(self.width_var.get())
                height = int(self.height_var.get())
                
                if width <= 0 or height <= 0:
                    messagebox.showerror("Ошибка", "Размеры должны быть положительными числами")
                    return
                
                if self.processor.resize_image(width, height):
                    self.display_images()
                    self.update_info()
                    messagebox.showinfo("Успех", f"Размер изменен на {width}x{height}")
                else:
                    messagebox.showerror("Ошибка", "Не удалось изменить размер изображения")
                    
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные числовые значения для размеров")
        else:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
    
    def save_image_dialog(self):
        """Диалог сохранения изображения"""
        if self.processor.current_image is not None:
            file_path = filedialog.asksaveasfilename(
                title="Сохранить изображение",
                defaultextension=".jpg",
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("PNG", "*.png"),
                    ("BMP", "*.bmp"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if file_path:
                self.save_image(file_path)
        else:
            messagebox.showwarning("Предупреждение", "Нет изображения для сохранения")
    
    def save_image(self, file_path):
        """Сохранение обработанного изображения"""
        if self.processor.save_image(file_path):
            messagebox.showinfo("Успех", f"Изображение сохранено:\n{file_path}")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить изображение")
    
    def undo_action(self):
        """Отмена последнего действия"""
        if self.processor.undo():
            self.display_images()
            self.update_info()
            messagebox.showinfo("Успех", "Последнее действие отменено")
        else:
            messagebox.showinfo("Информация", "Нечего отменять")
    
    def reset_to_original(self):
        """Сброс к исходному изображению"""
        if self.processor.reset_to_original():
            self.display_images()
            self.update_info()
            messagebox.showinfo("Успех", "Изображение сброшено к исходному")
        else:
            messagebox.showinfo("Информация", "Нет исходного изображения")
    
    def update_info(self):
        """Обновление информации об изображении"""
        info = self.processor.get_image_info()
        if info:
            text = f"=== ИНФОРМАЦИЯ ОБ ИЗОБРАЖЕНИИ ===\n\n"
            text += f"Ширина: {info['width']} px\n"
            text += f"Высота: {info['height']} px\n"
            text += f"Размер: {info['size']}\n"
            text += f"Формат: {info['format']}\n"
            text += f"Цветовой режим: {info['mode']}\n"
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, text)
    
    def load_settings(self):
        """Загрузка пользовательских настроек"""
        try:
            if os.path.exists('config/settings.json'):
                with open('config/settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.width_var.set(settings.get('width', '800'))
                    self.height_var.set(settings.get('height', '600'))
                    self.noise_var.set(settings.get('noise_strength', 3))
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
    
    def save_settings(self):
        """Сохранение пользовательских настроек"""
        try:
            settings = {
                'width': self.width_var.get(),
                'height': self.height_var.get(),
                'noise_strength': self.noise_var.get()
            }
            
            with open('config/settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    app = ImageProcessorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()