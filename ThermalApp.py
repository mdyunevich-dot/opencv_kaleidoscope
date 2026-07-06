import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from VisionProcessor import Processor  # Импортируем наш обработчик

class App(tk.Tk):
    """Класс интерфейса приложения с вкладками управления и просмотра."""
    def __init__(self):
        super().__init__()
        self.title("Вариант 25: Калейдоскоп")
        self.geometry("800x600")

        self.processor = Processor()

        # Создание вкладок (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Управление")
        self.notebook.add(self.tab2, text="Просмотр результата")

        self.mirror_mode = tk.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):
        # Панель управления на первой вкладке
        btn_frame = ttk.Frame(self.tab1, padding=20)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Открыть изображение", command=self.open_file).pack(anchor="w", pady=5)

        ttk.Label(btn_frame, text="Режим калейдоскопа:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 5))
        
        ttk.Radiobutton(btn_frame, text="Отразить левую половину направо", variable=self.mirror_mode, value=1, command=self.update_image).pack(anchor="w", pady=2)
        ttk.Radiobutton(btn_frame, text="Отразить верхнюю половину вниз", variable=self.mirror_mode, value=2, command=self.update_image).pack(anchor="w", pady=2)

        ttk.Button(btn_frame, text="Сохранить результат", command=self.save_file).pack(anchor="w", pady=20)

        self.lbl_orig = ttk.Label(self.tab1, text="Изображение не загружено", wraplength=700)
        self.lbl_orig.pack(expand=True)

        # Компонент для вывода картинки на второй вкладке
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
        mode = self.mirror_mode.get()
        res_bgr = self.processor.make_kaleidoscope(mode)

        if res_bgr is not None:
            img_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil.thumbnail((700, 450))
            
            self.img_tk = ImageTk.PhotoImage(img_pil)
            self.lbl_res.config(image=self.img_tk, text="")
            self.lbl_orig.config(text="Изображение загружено! Перейдите на вкладку 'Просмотр результата' для просмотра.")
        else:
            self.lbl_orig.config(text="Сначала откройте корректное изображение.")

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
