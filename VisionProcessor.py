import cv2
import numpy as np

class Processor:
    """Класс для попиксельной и матричной обработки изображений с помощью OpenCV."""
    def __init__(self):
        self.image = None       # Исходное изображение (матрица BGR)
        self.processed = None   # Результат обработки (матрица BGR)

    def load_image(self, path):
        """Безопасная загрузка картинки через байтовый поток Python."""
        try:
            with open(path, "rb") as f:
                file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
            self.image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            if self.image is not None:
                self.processed = self.image.copy()
                return True
            return False
        except Exception:
            return False

    def make_kaleidoscope(self, mode):
        """Разрезание матрицы, зеркальный переворот через cv2.flip и склеивание."""
        if self.image is None:
            return None

        h, w, c = self.image.shape

        if mode == 1:
            # Отразить левую половину направо
            mid_w = w // 2
            left_half = self.image[:, :mid_w]
            right_half = cv2.flip(left_half, 1)
            self.processed = np.hstack((left_half, right_half))
            
        elif mode == 2:
            # Отразить верхнюю половину вниз
            mid_h = h // 2
            top_half = self.image[:mid_h, :]
            bottom_half = cv2.flip(top_half, 0)
            self.processed = np.vstack((top_half, bottom_half))

        return self.processed

    def save_image(self, path):
        """Безопасное сохранение готового изображения."""
        if self.processed is not None:
            try:
                ext = path.split('.')[-1]
                is_success, im_buf_arr = cv2.imencode(f".{ext}", self.processed)
                if is_success:
                    with open(path, "wb") as f:
                        f.write(im_buf_arr.tobytes())
                    return True
                return False
            except Exception:
                return False
        return False
