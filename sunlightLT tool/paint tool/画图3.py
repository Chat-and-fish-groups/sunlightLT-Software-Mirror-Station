import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("增强画板程序")

        # 初始化画布大小
        self.canvas_width = 800
        self.canvas_height = 600

        # 创建一个画布
        self.canvas = tk.Canvas(self.root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # 创建工具栏
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack()

        # 创建颜色选择按钮
        self.color_button = tk.Button(self.toolbar, text="选择颜色", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        # 创建橡皮擦按钮
        self.eraser_button = tk.Button(self.toolbar, text="橡皮擦", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        # 创建清除按钮
        self.clear_button = tk.Button(self.toolbar, text="清除画布", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        # 创建保存按钮
        self.save_button = tk.Button(self.toolbar, text="保存", command=self.save_canvas)
        self.save_button.pack(side=tk.LEFT)

        # 创建加载按钮
        self.load_button = tk.Button(self.toolbar, text="加载", command=self.load_canvas)
        self.load_button.pack(side=tk.LEFT)

        # 创建撤销按钮
        self.undo_button = tk.Button(self.toolbar, text="撤销", command=self.undo)
        self.undo_button.pack(side=tk.LEFT)

        # 创建画笔大小选择
        self.brush_size = tk.IntVar(value=2)
        self.brush_size_slider = tk.Scale(self.toolbar, from_=1, to=10, orient=tk.HORIZONTAL, label="画笔大小", variable=self.brush_size)
        self.brush_size_slider.pack(side=tk.LEFT)

        self.paint_color = "black"
        self.eraser_on = False
        self.history = []

        # 绑定鼠标事件
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # 初始化画笔位置和画布图像
        self.old_x = None
        self.old_y = None
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.paint_color = askcolor(color=self.paint_color)[1]

    def use_eraser(self):
        self.eraser_on = not self.eraser_on

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.history.clear()

    def paint(self, event):
        brush_size = self.brush_size.get()
        color = "white" if self.eraser_on else self.paint_color
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, fill=color, width=brush_size)
            self.draw.line([self.old_x, self.old_y, event.x, event.y], fill=color, width=brush_size)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None
        self.history.append(self.image.copy())

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image = Image.open(file_path)
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def undo(self):
        if self.history:
            self.image = self.history.pop()
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()