import tkinter as tk

def update_scale_factor(*args):
    global SCALE_FACTOR
    SCALE_FACTOR = int(*args)
    draw_rectangle()

def draw_rectangle():
    length_text = length_entry.get()
    width_text = width_entry.get()
    rows_text = rows_entry.get()
    cols_text = cols_entry.get()
    spacing_text = spacing_entry.get()

    # 验证输入框的值是否为空字符串
    if length_text == '' or width_text == '' or rows_text == '' or cols_text == '' or spacing_text == '':
        return

    length = float(length_text)
    width = float(width_text)
    rows = int(rows_text)
    cols = int(cols_text)
    spacing = float(spacing_text)

    # 缩放矩形的长度和宽度
    scaled_length = length * SCALE_FACTOR
    scaled_width = width * SCALE_FACTOR
    # 缩放矩形摆放间隔
    scaled_spacing = spacing * SCALE_FACTOR

    canvas.delete("rectangle")
    canvas.delete("arrow")

    for row in range(rows):
        for col in range(cols):
            x1 = 10 + (scaled_length + scaled_spacing) * col
            y1 = 10 + (scaled_width + scaled_spacing) * row
            x2 = x1 + scaled_length
            y2 = y1 + scaled_width
            canvas.create_rectangle(x1, y1, x2, y2, fill="cyan", tags="rectangle")
    
    # 绘制带箭头的直线
    x1, y1 = 10+scaled_length/2, 10+scaled_width/2  # 起点坐标
    x2, y2 = 10+scaled_length/2, 10+scaled_width/2+50  # 终点坐标
    canvas.create_line(x1, y1, x2, y2, arrow="last",tags="arrow")

root = tk.Tk()
root.title("矩形绘制程序")

# 创建输入框和按钮
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

length_label = tk.Label(input_frame, text="长度：")
length_label.grid(row=0, column=0, padx=5)
length_entry = tk.Entry(input_frame)
length_entry.grid(row=0, column=1, padx=5)

width_label = tk.Label(input_frame, text="宽度：")
width_label.grid(row=1, column=0, padx=5)
width_entry = tk.Entry(input_frame)
width_entry.grid(row=1, column=1, padx=5)

rows_label = tk.Label(input_frame, text="行数：")
rows_label.grid(row=2, column=0, padx=5)
rows_entry = tk.Entry(input_frame)
rows_entry.grid(row=2, column=1, padx=5)

cols_label = tk.Label(input_frame, text="列数：")
cols_label.grid(row=3, column=0, padx=5)
cols_entry = tk.Entry(input_frame)
cols_entry.grid(row=3, column=1, padx=5)

spacing_label = tk.Label(input_frame, text="间隔：")
spacing_label.grid(row=4, column=0, padx=5)
spacing_entry = tk.Entry(input_frame)
spacing_entry.grid(row=4, column=1, padx=5)

# 创建滑动条比例尺
scale_label = tk.Label(root, text="比例尺")
scale_label.pack()
scale = tk.Scale(root, from_=1, to=20, orient="horizontal", command=update_scale_factor, sliderlength=10, length=300)
scale.set(10)  # 默认初始值为10
scale.pack(pady=10)

# 创建绘制按钮
draw_button = tk.Button(root, text="绘制矩形", command=draw_rectangle)
draw_button.pack(pady=10)

# 创建画布
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

root.mainloop()
