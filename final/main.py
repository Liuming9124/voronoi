# $LAN=PYTHON$
# TODO change tuple to list
import tkinter as tk
from tkinter import filedialog
import math
maxsize = 1000000000

# variable----------------------------------------------------------------------------------------------------------------
class Graph():
    def __init__(self, canvas, Width, Length):
        self.canvas = canvas
        self.width = Width
        self.length = Length

        # 當前情況的圖
        self.points_id = []  # 存取每個圖的點的 id : [id]
        self.points = []    # 存取每個圖的點 : [(x, y)]
        self.edges_id = []   # 存取每個圖的邊的 id : [id]
        self.edges = []     # 繪製的邊 : [[draw1, draw2, point_a, point_b, edge_piont1, edge_point2]] -> 畫布上兩點, 源自兩point, 長度延伸的兩點

        # 讀檔的圖
        self.inputCurrentIndex = 0
        self.inputIndex = 0
        self.inputPoints = []
 
        # store record for step by step
        self.rpoints_id = []
        self.rpoints = []
        self.redges_id = []
        self.redges = []
        


        # 輸出用: 兩層列表，第一層存取每個圖的點，第二層存取每個圖的點座標
        self.outputPoints = [] # 繪製的點 : [[(x, y)]]
        self.outputEdges = [] # 繪製的邊 : [[( draw1, draw2, point_a, point_b, edge_piont1, edge_point2)]] -> 畫布上兩點, 源自兩point, 長度延伸的兩點

    # add a line to the graph
    def calculate_line_endpoints(self, point1, point2, edge_status):
        x1, y1 = point1
        x2, y2 = point2
        # 計算斜率 function y = slope * x + b
        slope, b = self.find_line(point1, point2)
        
        #計算直線的兩端點
        if (slope == None): # 畫出垂直線
            dx1 = dx2 = x1
            if   (edge_status==[0,0,1]):
                dy1 = y2
                if (y1 < y2):
                    dy2 = maxsize
                else:
                    dy2 = -maxsize
            elif (edge_status==[0,1,0]):
                dy1 = y1
                dy2 = y2
            elif (edge_status==[0,1,1]):
                dy1 = y1
                if (y1 < y2):
                    dy2 = maxsize
                else:
                    dy2 = -maxsize
            elif (edge_status==[1,0,0]):
                dy1 = y1
                if (y1 < y2):
                    dy2 = -maxsize
                else:
                    dy2 = maxsize
            elif (edge_status==[1,1,0]):
                dy1 = y2
                if (y1 < y2):
                    dy2 = -maxsize
                else:
                    dy2 = maxsize
            elif (edge_status==[1,1,1]):
                dy1 = maxsize
                dy2 = -maxsize
        else:
            if   (edge_status==[0,0,1]):
                dx1 = x2
                dy1 = y2
                if (x1 < x2):
                    dx2 = maxsize
                else:
                    dx2 = -maxsize
                dy2 = slope * dx2 + b
            elif (edge_status==[0,1,0]):
                dx1 = x1
                dy1 = y1
                dx2 = x2
                dy2 = y2
            elif (edge_status==[0,1,1]):
                dx1 = x1
                dy1 = y1
                if (x1 < x2):
                    dx2 = maxsize
                else:
                    dx2 = -maxsize
                dy2 = slope * dx2 + b
            elif (edge_status==[1,0,0]):
                dx1 = x1
                dy1 = y1
                if (x1 < x2):
                    dx2 = -maxsize
                else:
                    dx2 = maxsize
                dy2 = slope * dx2 + b
            elif (edge_status==[1,1,0]):
                dx1 = x2
                dy1 = y2
                if (x1 < x2):
                    dx2 = -maxsize
                else:
                    dx2 = maxsize
                dy2 = slope * dx2 + b
            elif (edge_status==[1,1,1]):
                dx1 = maxsize
                dy1 = slope * dx1 + b
                dx2 = -maxsize
                dy2 = slope * dx2 + b
        return dx1, dy1, dx2, dy2, slope, b
        
    def add_line(self, point1, point2, edge_status): # edge_status = [left, mid, right] -> left=1 : <-1 2, mid=1 : 1-2, right=1 : 1 2-> ; excaption [0,0,0] means perpendicular line 
        dx1, dy1, dx2, dy2, slope, b = self.calculate_line_endpoints(point1, point2, edge_status)
        # 檢查線是否在畫布上，若有則裁切成畫布範圍，若無則不畫
        canvas_x1 = dx1
        canvas_y1 = dy1
        canvas_x2 = dx2
        canvas_y2 = dy2

        if slope is None:  # 處理垂直線的邊界
            if dy1 < 0:
                canvas_y1 = 0
            elif dy1 > self.length:
                canvas_y1 = self.length
            if dy2 < 0:
                canvas_y2 = 0
            elif dy2 > self.length:
                canvas_y2 = self.length
        else:
            if dx1 < 0:
                canvas_x1 = 0
                canvas_y1 = slope * canvas_x1 + b
            elif dx1 > self.width:
                canvas_x1 = self.width
                canvas_y1 = slope * canvas_x1 + b
            if dx2 < 0:
                canvas_x2 = 0
                canvas_y2 = slope * canvas_x2 + b
            elif dx2 > self.width:
                canvas_x2 = self.width
                canvas_y2 = slope * canvas_x2 + b

        canvasP = self.clip_line((canvas_x1, canvas_y1), (canvas_x2, canvas_y2), slope, b)
        canvas_x1, canvas_y1 = canvasP[0]
        canvas_x2, canvas_y2 = canvasP[1]

        # 畫線
        eID = self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue", tags="line")
        self.edges_id.append(eID)
        self.edges.append([canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]])
        
        if test and test_index >= 1:
            print(f"({canvas_x1}, {canvas_y1}), ({canvas_x2}, {canvas_y2})")
            print(f"({point1[0]}, {point1[1]}), ({point2[0]}, {point2[1]})")
            print(edge_status)
            print()

    # add a point to the graph
    def add_point(self, point, color='red', checkindex = -1):
        if (checkindex == -1):
            checkindex = len(self.points)
        # find the same point and delete in canvas
        for i in range(0, checkindex):
            if (point == self.points[i]):
                # delete the point in the canvas
                print(f'delete point: {point}: {self.points_id[i]}')
                self.canvas.delete(self.points_id[i])
                self.points.pop(i)
                self.points_id.pop(i)
                
        # add the point in the canvas
        point_id = self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill=color)
        self.points.append((point[0], point[1]))
        if (test):
            print(f"add point: {point}: {point_id}")
        self.points_id.append(point_id)

    # clear all points and lines
    def clear_all(self):
        """清除畫布上所有物件，並重置點列表。"""
        self.canvas.delete("all")  # 清除畫布上的所有物件
        self.points_id = []  # 清空點 id 列表
        self.points = []
        self.edges = []   # 清空邊列表
        
    # clear a line
    def clear_line(self, point1, point2, c_oneToTwo, c_twoToOne):
        # find the line index in edges
        for i in range(len(self.edges)):
            if (point1 == self.edges[i][2] and point2 == self.edges[i][3]):
                last_edge = self.edges.pop(i)
                # delete the line in the canvas
                if (c_oneToTwo):
                    # delete part of line
                    x, y = point1
                    slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
                    if (slope == None):
                        pass
                    else:
                        x_edge1, y_edge1 = self.edges[i]
                        x_edge2, y_edge2 = self.edges[i + 1]
                        # find out same slope and add the line
                        if (slope == (y_edge2 - y_edge1) / (x_edge2 - x_edge1)):
                            # self.edges.append()
                            pass
                        elif (slope == (y_edge1 - y) / (x_edge1 - x)):
                            # self.canvas.delete(c_oneToTwo)
                            pass

                if (c_twoToOne):
                    x, y = point2
                    # self.canvas.delete(c_twoToOne)

    # clear all lines
    def clear_lines(self):
        self.edges_id.clear()
        self.edges.clear()
        self.canvas.delete("line")

    # 裁切線段回傳畫布上兩端點
    def clip_line(self, point1, point2, line_a, line_b):
        x1, y1 = point1
        x2, y2 = point2
        
        if (x1 > self.length):
            ty1 = line_a * self.length + line_b
            if (ty1 >= 0 and ty1 <= self.width):
                x1 = self.length
                y1 = ty1
        elif (x1 < 0):
            ty1 = line_a * 0 + line_b
            if (ty1 >= 0 and ty1 <= self.width):
                x1 = 0
                y1 = ty1
        
        if (y1 > self.width):
            tx1 = (self.width - line_b) / line_a
            if (tx1 >= 0 and tx1 <= self.length):
                x1 = tx1
                y1 = self.width
        elif (y1 < 0):
            tx1 = (-line_b) / line_a
            if (tx1 >= 0 and tx1 <= self.length):
                x1 = tx1
                y1 = 0
        
        if (x2 > self.length):
            ty2 = line_a * self.length + line_b
            if (ty2 >= 0 and ty2 <= self.width):
                x2 = self.length
                y2 = ty2
        elif (x2 < 0):
            ty2 = line_a * 0 + line_b
            if (ty2 >= 0 and ty2 <= self.width):
                x2 = 0
                y2 = ty2
        
        if (y2 > self.width):
            tx2 = (self.width - line_b) / line_a
            if (tx2 >= 0 and tx2 <= self.length):
                x2 = tx2
                y2 = self.width
        elif (y2 < 0):
            tx2 = (-line_b) / line_a
            if (tx2 >= 0 and tx2 <= self.length):
                x2 = tx2
                y2 = 0
            
        return ([[x1, y1], [x2, y2]])


    # add a perpendicular line
    def add_perpendicular_line(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        mid_x, mid_y = self.midpoint(point1, point2)

        perp_slope, b = self.find_perpendicular_line(point1, point2)
        if (perp_slope == None):
            dx1 = mid_x
            dy1 = maxsize
            dx2 = mid_x
            dy2 = -maxsize

            canvas_x1 = canvas_x2 = mid_x
            canvas_y1 = 0
            canvas_y2 = self.length
        else:
            b = mid_y - perp_slope * mid_x

            dx1 = maxsize
            dy1 = perp_slope * dx1 + b
            dx2 = -maxsize
            dy2 = perp_slope * dx2 + b

            canvas_x1 = 0
            canvas_y1 = perp_slope * canvas_x1 + b
            canvas_x2 = self.length
            canvas_y2 = perp_slope * canvas_x2 + b
            
        canvasP = self.clip_line((canvas_x1, canvas_y1), (canvas_x2, canvas_y2), perp_slope, b)
        canvas_x1, canvas_y1 = canvasP[0]
        canvas_x2, canvas_y2 = canvasP[1]

        draw_edge = [canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]] 
        return draw_edge
        # eID = self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue", tags="line")
        # self.edges_id.append(eID)
        # self.edges.append(((canvas_x1, canvas_y1), (canvas_x2, canvas_y2), point1, point2, (dx1, dy1), (dx2, dy2)))
        
    # find the perpendicular line
    def find_perpendicular_line(self, point1, point2):
        # return slope and b
        x1, y1 = point1
        x2, y2 = point2
        # calculate the slope
        if (y1 == y2):
            slope = None
        else:
            slope = -(x2 - x1) / (y2 - y1)
        # calculate the middle point
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        # calculate the perpendicular slope
        if (slope == None):
            b = mid_x
        else:
            b = mid_y - slope * mid_x
        return [slope, b]
    
    # use slope and point to find another point
    def lineOtherPoint(self, point, line_slope, line_b):
        x, y = point
        if (line_slope == None):
            return (x+1, 0)
        elif (line_slope == 0):
            return (0, y+1)
        else:
            new_x = x+1
            new_y = line_slope * new_x + line_b
            return [new_x, new_y]

    
    # 找三角形的外心 : a, b, c: 三角形的三個頂點 ; 回傳: 外心的座標
    def circumcenter(self, a, b, c):
        # 找出ab及bc的中垂線
        a_ab, b_ab = self.find_perpendicular_line(a, b)
        a_bc, b_bc = self.find_perpendicular_line(b, c)
        # 透過中垂線找出外心
        x, y = self.find_intersection(a_ab, b_ab, a_bc, b_bc)
        return [x, y]

    # 找兩點的中點
    def midpoint(self, a, b):
        # a, b: 兩個點的座標 ; 回傳: 中點的座標
        x1, y1 = a
        x2, y2 = b
        return [(x1 + x2) / 2, (y1 + y2) / 2]

    # 計算兩點距離
    def distance(self, a, b):
        # a, b: 兩個點的座標 ; 回傳: 兩點的距離
        x1, y1 = a
        x2, y2 = b
        return math.hypot(x2 - x1, y2 - y1)

    # 透過兩點找出 function y = ax+b
    def find_line(self, a, b):
        # a, b: 兩個點的座標 ; 回傳: 直線的斜率 a 和截距 b
        x1, y1 = a
        x2, y2 = b
        if (a == b):
            print('find_line() error: a == b, cannot find line')
            return None, None
        else:
            if (x1 == x2):
                a = None
                b = None
            else:
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1
            return [a, b]

    # 透過兩條線找出交點 回傳: 兩條線的交點
    def find_intersection(self, a1, b1, a2, b2):
        # a1, b1: 第一條線的斜率和截距
        # a2, b2: 第二條線的斜率和截距

        if (a1 == a2):
            if (b1 == b2):
                print('find_intersection() error: 兩條線重合')
                return None
            else:
                print('find_intersection() error: 兩條線平行')
                return None
        if (a1 == None):
            x = b1
            y = a2 * x + b2
        elif (a2 == None):
            x = b2
            y = a1 * x + b1
        else:
            x = (b2 - b1) / (a1 - a2)
            y = a1 * x + b1
        return [x, y]

    def find_line_degreeMoreThan90(self, Center, P_large, P1, P2, mid_L1, mid_L2, mid_12):
        xm, ym = mid_12
        x1, y1 = P1
        x2, y2 = P2
        
        # line 1 create from other two mid points
        a1, b1 = self.find_line(mid_L1, mid_L2)
        # 找出 Mid 投影到線 y = a1x + b1 的點
        # 找出 p1, p2 的中垂線 TODO : 有兩點垂直或水平的情況 , ondo
        if (y1 == y2):
            a2 = None
            b2 = ym
        else:
            a2 = -(x1 - x2) / (y1 - y2)
            b2 = ym - a2 * xm
        Point = self.find_intersection(a1, b1, a2, b2)

        if (self.distance(Point, P_large) < self.distance(mid_12, P_large)):
            return [ Point, Center, [0,0,1]]
        else:
            return [ Center, Point, [0,1,1]]
    
    # 判斷三角形並找出要畫的線段
    def cal_triangle_line(self, Center, A, B, C, ab, bc, ac): # 中點 Mid; 頂點A, B, C ; 三邊中點 ab, bc, ac => return 三組欲畫的線段，[(mid, one, status), (mid, two, status), (mid, three, status)]
        # 定義點 A, B, C 的坐標
        x1, y1 = A
        x2, y2 = B
        x3, y3 = C

        # 計算向量 AB 和 AC 的餘弦值 (對應角 A)
        AB = ((x2 - x1), (y2 - y1))
        AC = ((x3 - x1), (y3 - y1))
        cos_A = (AB[0] * AC[0] + AB[1] * AC[1]) / (math.hypot(*AB) * math.hypot(*AC))
        
        # 計算向量 BA 和 BC 的餘弦值 (對應角 B)
        BA = ((x1 - x2), (y1 - y2))
        BC = ((x3 - x2), (y3 - y2))
        cos_B = (BA[0] * BC[0] + BA[1] * BC[1]) / (math.hypot(*BA) * math.hypot(*BC))
        
        # 計算向量 CA 和 CB 的餘弦值 (對應角 C)
        CA = ((x1 - x3), (y1 - y3))
        CB = ((x2 - x3), (y2 - y3))
        cos_C = (CA[0] * CB[0] + CA[1] * CB[1]) / (math.hypot(*CA) * math.hypot(*CB))
        
        # 計算不同三角形下該畫的線段
        edges = []
        if (cos_A > 0 and cos_B > 0 and cos_C > 0): # 銳角三角形
            edges.append([Center, ab, [0,1,1]])
            edges.append([Center, bc, [0,1,1]])
            edges.append([Center, ac, [0,1,1]])
        else:   # 鈍角三角形 or 直角三角形
            print("鈍角三角形")
            if (cos_C <= 0):
                print("cos_C <= 0")
                edges.append([Center, bc, [0,1,1]])
                edges.append([Center, ac, [0,1,1]])
                edgeFind = self.find_line_degreeMoreThan90(Center, C, A, B, bc, ac, ab)
                edges.append(edgeFind)
            elif (cos_A <= 0):
                print("cos_A <= 0")
                edges.append([Center, ab, [0,1,1]])
                edges.append([Center, ac, [0,1,1]])
                edgeFind = self.find_line_degreeMoreThan90(Center, A, B, C, ab, ac, bc)
                edges.append(edgeFind)
            elif (cos_B <= 0):
                print("cos_B <= 0")
                edges.append([Center, ab, [0,1,1]])
                edges.append([Center, bc, [0,1,1]])
                edgeFind = self.find_line_degreeMoreThan90(Center, B, A, C, ab, bc, ac)
                edges.append(edgeFind)

        return edges


# calculate---------------------------------------------------------------------------------------------------------------
class voronoi():
    def __init__(self, canvas, graph):
        self.canvas = canvas
        self.graph = graph
        # store voronoi diagram
        self.points = []
        self.hpedges = []
        self.vedges = []

        
    def compute_voronoi(self):
        self.voronoi_start(self.graph.points, self.graph.points_id)

    def voronoi_start(self, points, points_id):
        if (len(points) <=1):
            return
        elif (len(points) == 2):
            drawEdge = self.graph.add_perpendicular_line(points[0], points[1]) # return [canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]]
            eID = self.canvas.create_line(drawEdge[0][0], drawEdge[0][1], drawEdge[1][0], drawEdge[1][1], fill="blue", tags="line")
            self.graph.edges_id.append(eID)
            self.graph.edges.append(drawEdge)
        elif (len(points) == 3):
            self.compute_voronoi_three()
        else:
            left, left_id, right, right_id = self.devide(points, points_id)
            self.voronoi_start( left,  left_id) # left
            self.voronoi_start(right, right_id) # right
            self.merge(left, right) # merge(left, right)
    
    def devide(self, points, points_id):
        # 根據x進行排序 並分成左右兩邊 sort points and points_id together
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                if (points[i][0] > points[j][0]):
                    points[i], points[j] = points[j], points[i]
                    points_id[i], points_id[j] = points_id[j], points_id[i]
        mid = len(points) // 2
        left, right = points[:mid], points[mid:]
        left_id, right_id = points_id[:mid], points_id[mid:]
        return left, left_id, right, right_id

    def merge(self, left, right):
        chl = self.convex_hull(left)
        chr = self.convex_hull(right)
        merge_chr = self.merge_hull(chl, chr)

        self.hyper_plane(left, right)
        self.wipe_line()
        # voronoi
        # self.merge()
        self.convex_hull(left + right)

    def convex_hull(self, points): # use graham's scan
        # Step 1: Find the base point (lowest and left-most point)
        points.sort(key=lambda x: (x[1], x[0]))  # Sort by y, then by x
        base = points[0]

        # Step 2: Sort remaining points by polar angle and distance from the base
        points = [base] + sorted(points[1:], key=lambda p: (
            self.angle(base, p), 
            (p[0] - base[0]) ** 2 + (p[1] - base[1]) ** 2
        ))

        # Step 3: Build the convex hull
        ch = []
        for p in points:
            while len(ch) >= 2 and self.cross(ch[-2], ch[-1], p) <= 0:
                ch.pop()  # Remove points that form a clockwise or collinear turn
            ch.append(p)

        # Step 4: Draw the convex hull
        # for i in range(len(ch)):
        #     self.graph.add_line(ch[i], ch[(i + 1) % len(ch)], [0, 1, 0])  # Connect points in hull
        return ch
    
    def angle(self, o, p):  # calculate polar angle with respect to the base point
        return math.atan2(p[1] - o[1], p[0] - o[0])
    
    def cross(self, o, a, b): # cross product
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def compare_angle(self, o, a, b):
        return self.cross(o, a, b) > 0

    def merge_hull(self, chl, chr):
        pass
    
    def hyper_plane(self, left, right):
        print("hyper")
        pass

    def wipe_line(self):
        print("wipe")
        pass
    
    def compute_voronoi_three(self):
            # 找出三點共線
            a, b = self.graph.find_line(self.graph.points[0], self.graph.points[1])
            a1, b1 = self.graph.find_line(self.graph.points[0], self.graph.points[2])
            if (test and test_index <= 1):
                print(f'compute_voronoi: y = {a} x + {b}; y = {a1} x + {b1}')
            # 三點共線
            if (a == None and a1 == None):
                if (test and test_index <= 1):
                    print("三點共線")
                if ((self.graph.points[0][1] < self.graph.points[1][1] and self.graph.points[1][1] < self.graph.points[2][1]) or (self.graph.points[0][0] > self.graph.points[1][0] and self.graph.points[1][0] > self.graph.points[2][0])):
                    print(f'{self.graph.points[0][1]} < {self.graph.points[1][1]} < {self.graph.points[2][1]} or {self.graph.points[0][0]} > {self.graph.points[1][0]} > {self.graph.points[2][0]}')
                    center = 1
                elif ((self.graph.points[1][1] < self.graph.points[0][1] and self.graph.points[0][1] < self.graph.points[2][1]) or (self.graph.points[1][0] > self.graph.points[0][0] and self.graph.points[0][0] > self.graph.points[2][0])):
                    print(f'{self.graph.points[1][1]} < {self.graph.points[0][1]} < {self.graph.points[2][1]} or {self.graph.points[1][0]} > {self.graph.points[0][0]} > {self.graph.points[2][0]}')
                    center = 0
                else:
                    print(f'{self.graph.points[2][1]} < {self.graph.points[0][1]} < {self.graph.points[1][1]} or {self.graph.points[2][0]} > {self.graph.points[0][0]} > {self.graph.points[1][0]}')
                    center = 2
                # 畫出中垂線
                for i in range(3):
                    if (i != center):
                        self.graph.add_perpendicular_line(self.graph.points[center], self.graph.points[i])
            elif (a == a1):
                if (test and test_index <= 1):
                    print("三點共線-非垂直")
                if ((self.graph.points[0][1] < self.graph.points[1][1] and self.graph.points[1][1] < self.graph.points[2][1]) or 
                    (self.graph.points[0][1] > self.graph.points[1][1] and self.graph.points[1][1] > self.graph.points[2][1]) or 
                    (self.graph.points[0][0] > self.graph.points[1][0] and self.graph.points[1][0] > self.graph.points[2][0]) or
                    (self.graph.points[0][0] < self.graph.points[1][0] and self.graph.points[1][0] < self.graph.points[2][0])):
                    # print(f'case1: {self.graph.points[0][1]} < {self.graph.points[1][1]} < {self.graph.points[2][1]} or {self.graph.points[0][0]} > {self.graph.points[1][0]} > {self.graph.points[2][0]}')
                    center = 1
                elif ((self.graph.points[1][1] < self.graph.points[0][1] and self.graph.points[0][1] < self.graph.points[2][1]) or 
                      (self.graph.points[1][1] > self.graph.points[0][1] and self.graph.points[0][1] > self.graph.points[2][1]) or
                      (self.graph.points[1][0] > self.graph.points[0][0] and self.graph.points[0][0] > self.graph.points[2][0]) or
                      (self.graph.points[1][0] < self.graph.points[0][0] and self.graph.points[0][0] < self.graph.points[2][0])):
                    
                    print(f'case2: {self.graph.points[1][1]} < {self.graph.points[0][1]} < {self.graph.points[2][1]} or {self.graph.points[1][0]} > {self.graph.points[0][0]} > {self.graph.points[2][0]}')
                    center = 0
                elif ((self.graph.points[2][1] < self.graph.points[0][1] and self.graph.points[0][1] < self.graph.points[1][1]) or 
                      (self.graph.points[2][1] > self.graph.points[0][1] and self.graph.points[0][1] > self.graph.points[1][1]) or
                      (self.graph.points[2][0] > self.graph.points[0][0] and self.graph.points[0][0] > self.graph.points[1][0]) or
                      (self.graph.points[2][0] < self.graph.points[0][0] and self.graph.points[0][0] < self.graph.points[1][0])):
                    
                    print(f'case3: {self.graph.points[2][1]} < {self.graph.points[0][1]} < {self.graph.points[1][1]} or {self.graph.points[2][0]} > {self.graph.points[0][0]} > {self.graph.points[1][0]}')
                    center = 2
                else:
                    print('compute_voronoi 三點共線: error')
                    print(self.graph.points)
                    
                # 畫出中垂線
                for i in range(3):
                    if (i != center):
                        self.graph.add_perpendicular_line(self.graph.points[center], self.graph.points[i])
            # 三點不共線
            else:
                center_x, center_y = self.graph.circumcenter(self.graph.points[0], self.graph.points[1], self.graph.points[2])
                if (test and test_index >= 1):
                    self.graph.add_point((center_x, center_y), 'blue')
                # 找出三邊的中點
                x1, y1 = self.graph.midpoint(self.graph.points[0], self.graph.points[1])
                x2, y2 = self.graph.midpoint(self.graph.points[1], self.graph.points[2])
                x3, y3 = self.graph.midpoint(self.graph.points[0], self.graph.points[2])

                # 找出三條要畫的線段
                drawEdges = self.graph.cal_triangle_line((center_x, center_y), self.graph.points[0], self.graph.points[1], self.graph.points[2], (x1, y1), (x2, y2), (x3, y3))
                for edge in drawEdges:
                    self.graph.add_line(edge[0], edge[1], edge[2])

# gui---------------------------------------------------------------------------------------------------------------------
class UiApp:
    def __init__(self, master, Length, Width):
        self.master = master
        self.master.title("Voronoi")
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

        # 建立「Read OutputFile」按鈕
        self.readoutputfile_button = tk.Button(master, text="Read OutputFile", command=self.readGraph)
        self.readoutputfile_button.pack(side="top")

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

    def get_voronoi_diagram(self):
        return self.voronoi_diagram

    def run(self):
        """當點擊 Run 按鈕時，繪製連線。"""
        self.graph.clear_lines()
        self.master.update() # 更新畫布
        self.voronoi_diagram.compute_voronoi()
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
        pass

    def readFile(self):
        self.graph.inputCurrentIndex = 0
        self.graph.inputIndex = 0
        self.graph.inputPoints = []

        file_path = filedialog.askopenfilename(
            title="選擇文件",
            filetypes=(("文本文件", "*.txt"), ("所有文件", "*.*"))  # 設定文件類型過濾
        )
        if file_path:
            self.operate_file(file_path)

    def writeFile(self):
        """write file to windows"""
        # Sorting
        tmpPoints = self.graph.points
        for i in range(0, len(tmpPoints)):
            # 先排序x, 再排序y
            for j in range(i+1, len(tmpPoints)):
                if (tmpPoints[i][0] > tmpPoints[j][0]):
                    tmpPoints[i], tmpPoints[j] = tmpPoints[j], tmpPoints[i]
                elif (tmpPoints[i][0] == tmpPoints[ j][0] and tmpPoints[i][1] > tmpPoints[j][1]):
                    tmpPoints[i], tmpPoints[j] = tmpPoints[j], tmpPoints[i]
        tmpEdges = []

        for edge in self.graph.edges:
            tmpEdges.append([edge[0][0], edge[0][1], edge[1][0], edge[1][1]])

        for i in tmpEdges:
            x1, y1, x2, y2 = i

            if (x1 > x2) or (x1 == x2 and y1 > y2):
                i[0], i[1], i[2], i[3] = i[2], i[3], i[0], i[1]

        tmpEdges.sort(key=lambda x: (x[0]))

        # Write to file
        with open('./result.txt', "w") as file:
            for point in tmpPoints:
                file.write('P ')
                file.write(f"{int(point[0])} {int(point[1])}\n")
            for edge in tmpEdges:
                file.write('E ')
                file.write(f"{int(edge[0])} {int(edge[1])} {int(edge[2])} {int(edge[3])}\n")

    def readGraph(self):
        self.graph.clear_all()
        file_path = filedialog.askopenfilename(
            title="選擇文件",
            filetypes=(("文本文件", "*.txt"), ("所有文件", "*.*"))  # 設定文件類型過濾
        )
        if file_path:
            self.operate_output(file_path)
            self.master.update()
    
    def nextGraph(self):
        self.graph.clear_all()
        if (self.graph.inputCurrentIndex >= self.graph.inputIndex):
            self.graph.inputCurrentIndex = 0
        points = self.graph.inputPoints[self.graph.inputCurrentIndex]
        for i in range(0, len(points)):
            if (test and test_index <= 0):
                print(points[i][0], points[i][1])
            self.graph.add_point((points[i][0], points[i][1]), 'red', len(self.graph.points))
        if (test and test_index >= 0):
            print()

        self.graph.inputCurrentIndex += 1
        

    def operate_file(self, file_path):
        endFlag = False
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
                num_points = int(line.strip())
                if (num_points == 0):
                    endFlag = True
                    break
                
                self.graph.inputIndex += 1
                
                # 讀取指定數量的點
                currentIndex = 0
                points = []
                while currentIndex < num_points:
                    line = file.readline()
                    while ( line and (line.strip() == "" or line.strip().startswith("#"))):
                        line = file.readline()  # 跳到下一行
                    x, y = map(float, line.split())
                    points.append((x, y))
                    if (test and test_index == 0):
                        print(f"({x}, {y})")
                    currentIndex += 1
                    
                # 將該組的點資料加入到 all_points
                all_points += [points]
                
        # 依序將每個圖的點資料加入到 self.graph.points
        self.graph.inputPoints = all_points
        print(all_points)
        if (test and test_index == 0):
            print("讀檔結果：")
            for points in self.graph.inputPoints:
                for x, y in points:
                    print(f"({x}, {y})")
                print()

    def operate_output(self, file_path):
        # operate upper line and store in points and edges
        self.graph.clear_all()
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                if (line.startswith("P")):
                    x, y = map(float, line[2:].split())
                    self.graph.add_point((x, y), 'red', len(self.graph.points))
                elif (line.startswith("E")):
                    x1, y1, x2, y2 = map(float, line[2:].split())
                    self.graph.add_line((x1, y1), (x2, y2), [0,1,0])
                else:
                    print("operate_output error")
                    break

# main---------------------------------------------------------------------------------------------------------------
test = False
test_index = 1

if __name__ == "__main__":
    # 設定長寬
    length = 600
    width = 600
    root = tk.Tk()
    app = UiApp(root, length, width)
    root.mainloop()