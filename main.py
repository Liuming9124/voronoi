import tkinter as tk
from tkinter import filedialog

# variable---------------------------------------------------------------------------------------------------------------
class Graph():
    def __init__(self, canvas, Width, Length):
        self.canvas = canvas
        self.width = Width
        self.length = Length

        # 讀檔時的變數
        self.graph_index = 0 # 讀檔時的圖索引
        self.graph_points = [] # 存取每個圖的點 : [(x, y)]
        self.graph_edges = [] # 存取每個圖的邊 : [(x1, y1, x2, y2, 斜率)]

        # 輸出用: 兩層列表，第一層存取每個圖的點，第二層存取每個圖的點座標
        self.drawPoints = [] # 繪製的點 : [[(x, y)]],
        self.drawEdges = [] # 繪製的邊 : [[(x1, y1, x2, y2, 斜率)]]

    # add a line to the graph
    def add_line(self, point1, point2):
        self.canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill="blue", tags="line")
    
    def add_lines(self, points):
        """在畫布上依序連接所有點，並繪製線段。"""
        self.canvas.delete("line")  # Corrected to use self.canvas
        if len(points) > 1:
            for i in range(len(points) - 1):
                # add_line(points[i], points[i + 1])
                print(points[i][0])
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", tags="line")


    # add a point to the graph
    def add_point(self, point):
        self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill="red")
        self.graph_points.append(point)

    def add_points(self, points):
        for point in points:
            self.add_point(point)
        # test index 1
        if (test and test_index >= 1):
            for x, y in self.graph_points:
                print(f"({x}, {y})")
            print()

    # clear all points and lines
    def clear_all(self):
        """清除畫布上所有物件，並重置點列表。"""
        self.canvas.delete("all")  # 清除畫布上的所有物件
        self.graph_points.clear()  # 清空點列表
        self.graph_edges.clear()   # 清空邊列表
        
    # clear a line
    def clear_line():
        pass
    # clear all lines
    def clear_lines():
        pass
    # find a line by two points
    def find_line():
        pass
    # add a perpendicular line
    def add_perpendicular_line(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        # calculate the slope
        if (x1 == x2):
            slope = None
        else:
            slope = (y2 - y1) / (x2 - x1)
        # calculate the middle point
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        # calculate the perpendicular slope
        if (slope == None):
            perp_slope = 0
        elif (slope == 0):
            perp_slope = None
        else:
            perp_slope = -1 / slope
        # calculate the perpendicular line and make the line longer to touch the border of the canvas
        if (perp_slope == None):
            self.canvas.create_line(mid_x, 0, mid_x, self.length, fill="blue", tags="line")
        elif (perp_slope == 0):
            self.canvas.create_line(0, mid_y, self.width, mid_y, fill="blue", tags="line")
        else:
            b = mid_y - perp_slope * mid_x
            x1 = 0
            y1 = perp_slope * x1 + b
            x2 = self.width
            y2 = perp_slope * x2 + b
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", tags="line")

    # calculate the intersection of two lines
    def intersection(self, line1, line2):
        # x1, y1, x2, y2, slope1 = line1
        # x3, y3, x4, y4, slope2 = line2
        # if (slope1 == None):
        #     x = x1
        #     y = slope2 * x + y3 - slope2 * x3
        # elif (slope2 == None):
        #     x = x3
        #     y = slope1 * x + y1 - slope1 * x1
        # elif (slope1 == 0):
        #     y = y1
        #     x = (y - y3) / slope2 + x3
        # elif (slope2 == 0):
        #     y = y3
        #     x = (y - y1) / slope1 + x1
        # else:
        #     x = (slope1 * x1 - slope2 * x3 + y3 - y1) / (slope1 - slope2)
        #     y = slope1 * x + y1 - slope1 * x1
        # return (x, y)
        pass


# calculate---------------------------------------------------------------------------------------------------------------
class voronoi():
    def __init__(self, canvas, graph):
        self.canvas = canvas
        self.graph = graph

    def compute_voronoi_first(self):
        if (len(self.graph.graph_points) <=1):
            return
        elif (len(self.graph.graph_points) == 2):
            self.graph.add_perpendicular_line(self.graph.graph_points[0], self.graph.graph_points[1])
        elif (len(self.graph.graph_points) == 3):
            center_x, center_y = self.circumcenter(self.graph.graph_points[0], self.graph.graph_points[1], self.graph.graph_points[2])
            # 將三角形的三個點連接起來，找出三條線的中點及斜率
            for i in range(3):
                x1, y1 = self.graph.graph_points[i]
                x2, y2 = self.graph.graph_points[(i + 1) % 3]
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                if (x1 == x2):
                    slope = None
                else:
                    slope = (y2 - y1) / (x2 - x1)
                self.graph.graph_edges.append((x1, y1, x2, y2, slope))

            # 劃出三條線的中垂線並且碰到外心之後就不繼續畫
            # for i in range(3):
            #     self.graph.add_perpendicular_line(self.graph.graph_points[i], (center_x, center_y))

        

    # 找三角形的外心
    def circumcenter(self, a, b, c):
        # 三角形的外心
        # a, b, c: 三角形的三個頂點
        # 回傳: 外心的座標
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c
        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        x = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (y1 - y2)) / d
        y = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (x2 - x1)) / d
        return (x, y)


    def compute_voronoi(self):
        # Get points from the graph
        points = np.array(self.graph.graph_points)
        if len(points) < 3:
            return  # Need at least 3 points to create a Voronoi diagram

        # Compute Voronoi diagram
        vor = Voronoi(points)

        # Draw Voronoi edges
        for (start, end) in vor.ridge_vertices:
            if start != -1 and end != -1:  # Valid vertices
                self.graph.add_line(vor.vertices[start], vor.vertices[end])


# gui---------------------------------------------------------------------------------------------------------------

class UiApp:
    def __init__(self, master, Length, Width):
        self.master = master
        self.master.title("Point Connector")
        self.file_path = None
        self.length = Length
        self.width = Width

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
        self.canvas = tk.Canvas(master, width=Width, height=Length, bg="white")
        self.canvas.pack()

        # 綁定點擊事件到畫布
        self.canvas.bind("<Button-1>", self.record_point)

        # Create instances of Graph and VoronoiDiagram
        self.graph = Graph(self.canvas, self.width, self.length)
        self.voronoi_diagram = voronoi(self.canvas, self.graph)


    def run(self):
        """當點擊 Run 按鈕時，繪製連線。"""
        self.voronoi_diagram.compute_voronoi_first()
        self.master.update() # 更新畫布
        

    def clear(self):
        """當點擊 Clear 按鈕時，清除畫布。"""
        self.graph.clear_all()
    
    def record_point(self, event):
        """紀錄點擊的 x, y 座標，並在畫布上繪製紅色小圓點。"""
        x, y = event.x, event.y
        self.graph.add_point((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
        if (test and test_index == 0):
            print(f"點紀錄於: ({x}, {y})")

    def stepbystep(self):
        # self.graph.add_lines(self.points)
        # self.master.update()
        # self.master.after(1000)
        pass
    def readFile(self):
        file_path = filedialog.askopenfilename(
            title="選擇文件",
            filetypes=(("文本文件", "*.txt"), ("所有文件", "*.*"))  # 設定文件類型過濾
        )
        if file_path:
            self.operate_file(file_path)


    def writeFile(self):
        """write file to windows"""
        pass
    
    def nextGraph(self):
        """next graph"""
        pass

    def operate_file(self, file_path):
        endFlag = False
        point_index = [] # 存取每個圖的點數
        all_points = []  # 儲存所有組的點資料

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
                    point_index.append(num_points)
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
                            print(f"({x}, {y})")

                            points.append((x, y))
                        except ValueError:
                            print(f"無效的點座標：{line}")
                            continue  # 跳過無效的座標行
                
                # 將該組的點資料加入到 all_points
                for x, y in points:
                    all_points.append((x, y))

        # 依序將每個圖的點資料加入到 self.graph.graph_points
        for i in range(len(point_index)):
            for j in range(point_index[i]):
                self.graph.graph_points.append(all_points[j])
            # 每個圖的點資料加入完後，繪製連線
            # 每個圖畫完之後，清空 self.graph.graph_points
            self.graph.graph_points.clear()
        
        if (test and test_index == 0):
            for points in self.graph.graph_points:
                for x, y in points:
                    print(f"({x}, {y})")
                print()




# main---------------------------------------------------------------------------------------------------------------


test = True
test_index = 1

if __name__ == "__main__":
    # 設定長寬
    length = 600
    width = 600
    root = tk.Tk()
    app = UiApp(root, length, width)
    root.mainloop()
