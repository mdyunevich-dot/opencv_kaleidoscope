import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class Processor:
    """Класс для попиксельной/матричной обработки изображений с помощью OpenCV."""
    def __init__(self):
        self.image = None       # Исходное изображение (BGR)
        self.processed = None   # Результат обработки (BGR)

    def load_image(self, path):
        """Абсолютно безопасная загрузка картинки через встроенный open()."""
        try:
            # Читаем файл как сырые байты штатными средствами Python (им плевать на кракозябры в путях)
            with open(path, "rb") as f:
                file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
            
            # Декодируем байты в матрицу OpenCV
            self.image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if self.image is not None:
                self.processed = self.image.copy()
                print("Отладка: Матрица успешно загружена в память!")
                return True
            print("Отладка: Ошибка декодирования байт.")
            return False
        except Exception as e:
            print(f"Отладка: Ошибка при чтении файла через open(): {e}")
            return False

    def make_kaleidoscope(self, mode):
        """Разрезание матрицы, зеркальный переворот и склеивание."""
        if self.image is None:
            return None

        h, w, c = self.image.shape

        if mode == 1:
            mid_w = w // 2
            left_half = self.image[:, :mid_w]
            right_half = cv2.flip(left_half, 1)
            self.processed = np.hstack((left_half, right_half))
            
        elif mode == 2:
            mid_h = h // 2
            top_half = self.image[:mid_h, :]
            bottom_half = cv2.flip(top_half, 0)
            self.processed = np.vstack((top_half, bottom_half))

        return self.processed

    def save_image(self, path):
        """Безопасное сохранение через open() байтового буфера."""
        if self.processed is not None:
            try:
                ext = path.split('.')[-1]
                is_success, im_buf_arr = cv2.imencode(f".{ext}", self.processed)
                if is_success:
                    with open(path, "wb") as f:
                        f.write(im_buf_arr.tobytes())
                    return True
                return False
            except Exception as e:
                print(f"Отладка: Не удалось сохранить файл: {e}")
                return False
        return False


class App(tk.Tk):
    """Класс интерфейса приложения."""
    def __init__(self):
        super().__init__()
        self.title("Вариант 25: Калейдоскоп")
        self.geometry("800x600")

        self.processor = Processor()

        # Задача №1: Окно с двумя вкладками
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Управление")
        self.notebook.add(self.tab2, text="Просмотр результата")

        self.mirror_mode = tk.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):
        # --- ВКЛАДКА 1: Управление ---
        btn_frame = ttk.Frame(self.tab1, padding=20)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Открыть изображение", command=self.open_file).pack(anchor="w", pady=5)

        ttk.Label(btn_frame, text="Режим калейдоскопа:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 5))
        
        ttk.Radiobutton(btn_frame, text="Отразить левую половину направо", variable=self.mirror_mode, value=1, command=self.update_image).pack(anchor="w", pady=2)
        ttk.Radiobutton(btn_frame, text="Отразить верхнюю половину вниз", variable=self.mirror_mode, value=2, command=self.update_image).pack(anchor="w", pady=2)

        ttk.Button(btn_frame, text="Сохранить результат", command=self.save_file).pack(anchor="w", pady=20)

        self.lbl_orig = ttk.Label(self.tab1, text="Изображение не загружено", wraplength=700)
        self.lbl_orig.pack(expand=True)

        # --- ВКЛАДКА 2: Просмотр результата ---
        self.lbl_res = ttk.Label(self.tab2, text="Здесь будет результат")
        self.lbl_res.pack(expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            if self.processor.load_image(file_path):
                self.update_image()
            else:
                self.lbl_orig.config(text="Ошибка: не удалось прочитать файл изображения.")

    def update_image(self):
        try:
            mode = self.mirror_mode.get()
            res_bgr = self.processor.make_kaleidoscope(mode)

            if res_bgr is not None:
                # Конвертируем OpenCV BGR в RGB для Tkinter
                img_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                
                # Масштабируем под размеры окна
                img_pil.thumbnail((700, 450))
                
                # Создаем и жестко привязываем картинку к объекту
                self.img_tk = ImageTk.PhotoImage(img_pil)

                self.lbl_res.config(image=self.img_tk, text="")
                self.lbl_orig.config(text="Изображение загружено! Перейдите на вкладку 'Просмотр результата' для просмотра.")
                print("Отладка: Отрисовка на вкладке завершена успешно!")
            else:
                self.lbl_orig.config(text="Сначала откройте корректное изображение.")
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА ОБНОВЛЕНИЯ: {e}")

    def save_file(self):
        if self.processor.processed is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            if self.processor.save_image(file_path):
                self.lbl_orig.config(text="Файл успешно сохранен!")


if __name__ == "__main__":
    app = App()
    app.mainloop()