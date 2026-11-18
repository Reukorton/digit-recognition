
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

from processing import find_contours


class Application:

    def __init__(self, root):
        self.root = root
        self.root.title("Распознавание изображений")
        self.root.resizable(False, False)

        self.width = 600
        self.height = 500

        self.last_x = None
        self.last_y = None

        self.brush_size = tk.IntVar(value=10)
        self.status = tk.StringVar(value="Готов к работе")

        self.image = Image.new(
            "RGB", (self.width, self.height), "white"
        )

        self.draw = ImageDraw.Draw(self.image)

        self.create_interface()
        self.show_image(self.image)

    def create_interface(self):

        # Левая панель
        left_panel = tk.Frame(self.root)
        left_panel.pack(side=tk.LEFT, padx=10, pady=10)

        # Холст для рисования
        self.canvas = tk.Canvas(
            left_panel,
            width=self.width,
            height=self.height,
            bg="white",
            highlightthickness=1,
            highlightbackground="gray"
        )

        self.canvas.pack()

        # События мыши
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Строка состояния
        tk.Label(
            left_panel,
            textvariable=self.status,
            anchor="w"
        ).pack(fill=tk.X, pady=5)

        # Правая панель
        right_panel = tk.Frame(self.root)
        right_panel.pack(
            side=tk.RIGHT,
            fill=tk.Y,
            padx=10,
            pady=10
        )

        tk.Label(
            right_panel,
            text="Управление",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            right_panel,
            text="Загрузить изображение",
            command=self.load_image,
            width=24
        ).pack(pady=5)

        tk.Button(
            right_panel,
            text="Найти контуры",
            command=self.process_image,
            width=24
        ).pack(pady=5)

        tk.Button(
            right_panel,
            text="Исходное изображение",
            command=self.restore_image,
            width=24
        ).pack(pady=5)

        tk.Button(
            right_panel,
            text="Очистить холст",
            command=self.clear_canvas,
            width=24
        ).pack(pady=5)

        tk.Label(
            right_panel,
            text="Толщина кисти"
        ).pack(pady=(20, 0))

        tk.Scale(
            right_panel,
            from_=1,
            to=40,
            orient=tk.HORIZONTAL,
            variable=self.brush_size
        ).pack(fill=tk.X)

    # Отображение изображения
    def show_image(self, image):
        self.photo = ImageTk.PhotoImage(image)

        self.canvas.delete("all")
        self.canvas.create_image(
            0, 0,
            anchor=tk.NW,
            image=self.photo
        )

    # Начало рисования
    def start_drawing(self, event):
        self.last_x = event.x
        self.last_y = event.y

        radius = self.brush_size.get() / 2

        self.draw.ellipse(
            (
                event.x - radius,
                event.y - radius,
                event.x + radius,
                event.y + radius
            ),
            fill="black"
        )

        self.show_image(self.image)

    # Рисование мышью
    def paint(self, event):
        if self.last_x is not None:

            self.draw.line(
                (
                    self.last_x,
                    self.last_y,
                    event.x,
                    event.y
                ),
                fill="black",
                width=self.brush_size.get()
            )

            radius = self.brush_size.get() / 2

            self.draw.ellipse(
                (
                    event.x - radius,
                    event.y - radius,
                    event.x + radius,
                    event.y + radius
                ),
                fill="black"
            )

        self.last_x = event.x
        self.last_y = event.y

        self.show_image(self.image)
        self.status.set("Рисование")

    # Завершение рисования
    def stop_drawing(self, event):
        self.last_x = None
        self.last_y = None

    # Загрузка изображения
    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp"),
                ("Все файлы", "*.*")
            ]
        )

        if not path:
            return

        try:
            loaded = Image.open(path).convert("RGBA")

            loaded.thumbnail(
                (self.width, self.height),
                Image.Resampling.LANCZOS
            )

            self.image = Image.new(
                "RGB",
                (self.width, self.height),
                "white"
            )

            x = (self.width - loaded.width) // 2
            y = (self.height - loaded.height) // 2

            self.image.paste(loaded, (x, y), loaded)

            self.draw = ImageDraw.Draw(self.image)

            self.show_image(self.image)
            self.status.set("Изображение загружено")

        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # Очистка холста
    def clear_canvas(self):
        self.image = Image.new(
            "RGB",
            (self.width, self.height),
            "white"
        )

        self.draw = ImageDraw.Draw(self.image)

        self.show_image(self.image)
        self.status.set("Холст очищен")

    # Поиск контуров
    def process_image(self):
        result = find_contours(self.image)

        self.show_image(result)
        self.status.set("Контуры выделены")

    # Возврат исходного изображения
    def restore_image(self):
        self.show_image(self.image)
        self.status.set("Исходное изображение")
