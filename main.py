import tkinter as tk
from tkinter import filedialog

# variable---------------------------------------------------------------------------------------------------------------

# calculate---------------------------------------------------------------------------------------------------------------


# gui---------------------------------------------------------------------------------------------------------------

def draw_lines(canvas, points):
    """在畫布上依序連接所有點，並繪製線段。"""
    canvas.delete("line")  # 清除現有連線
    if len(points) > 1:
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill="blue", tags="line")

def clear_canvas(canvas, points):
    """清除畫布上所有物件，並重置點列表。"""
    canvas.delete("all")  # 清除畫布上的所有物件
    points.clear()  # 清空點列表


def operate_file(file_path):
    endFlag = False
    all_points = []  # 用來儲存所有組的點資料

    with open(file_path, "r", encoding="utf-8") as file:
        while not endFlag:
            # 跳過註解行並尋找點的數量
            line = file.readline()
            while line and (line.strip() == "" or line.strip().startswith("#")):
                line = file.readline()  # 跳到下一行

            # 如果文件結尾，退出循環
            if not line:
                break

            # 將第一個非註解行視為點的數量
            try:
                num_points = int(line.strip())
            except ValueError:
                break

            if (endFlag):
                break

            # 讀取指定數量的點
            points = []
            for _ in range(num_points):
                line = file.readline().strip()
                if line:
                    try:
                        x, y = map(int, line.split())
                        points.append((x, y))
                    except ValueError:
                        print(f"無效的點座標：{line}")
                        continue  # 跳過無效的座標行
            
            # 將該組的點資料加入到 all_points
            all_points.append(points)
    if (test):
        for points in all_points:
            for x, y in points:
                print(f"({x}, {y})")
            print()

    return all_points



class PointConnectorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Point Connector")
        self.file_path = None

        # 建立「Run」按鈕
        self.run_button = tk.Button(master, text="Run", command=self.run)
        self.run_button.pack(side="top")

        # 建立「NextGraph」按鈕
        self.next_button = tk.Button(master, text="NextGraph", command=self.nextGraph)
        self.next_button.pack(side="top")

        # 建立「Step by Step」按鈕
        self.stepbystep_button = tk.Button(master, text="Step by Step", command=self.stepbystep)
        self.stepbystep_button.pack(side="top")

        # 建立「Read File」按鈕
        self.readfile_button = tk.Button(master, text="Read File", command=self.readFile)
        self.readfile_button.pack(side="top")

        # 建立「Write File」按鈕
        self.writefile_button = tk.Button(master, text="Write File", command=self.writeFile)
        self.writefile_button.pack(side="top")

        # 建立「Clear」按鈕
        self.clear_button = tk.Button(master, text="Clear", command=self.clear)
        self.clear_button.pack(side="top")

        
        # 設定畫布大小
        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()

        # 初始化點座標列表
        self.points = []

        # 綁定點擊事件到畫布
        self.canvas.bind("<Button-1>", self.record_point)



    def record_point(self, event):
        """紀錄點擊的 x, y 座標，並在畫布上繪製紅色小圓點。"""
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
        print(f"點紀錄於: ({x}, {y})")

    def run(self):
        """當點擊 Run 按鈕時，繪製連線。"""
        draw_lines(self.canvas, self.points)

    def clear(self):
        """當點擊 Clear 按鈕時，清除畫布。"""
        clear_canvas(self.canvas, self.points)
    
    def stepbystep(self):
        draw_lines(self.canvas, self.points)
        self.master.update()
        self.master.after(1000)

    def readFile(self):
        file_path = filedialog.askopenfilename(
            title="選擇文件",
            filetypes=(("文本文件", "*.txt"), ("所有文件", "*.*"))  # 設定文件類型過濾
        )
        if file_path:
            operate_file(file_path)


    def writeFile(self):
        """write file to windows"""
        pass
    
    def nextGraph(self):
        """next graph"""
        pass


# main---------------------------------------------------------------------------------------------------------------


test = True


if __name__ == "__main__":
    root = tk.Tk()
    app = PointConnectorApp(root)
    root.mainloop()
