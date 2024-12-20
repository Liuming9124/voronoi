# $LAN=PYTHON$
# M133040015 劉恭銘
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
        self.edges = []     # 繪製的邊 : [[draw1, draw2, point_a, point_b, edge_piont1, edge_point2, id]] -> 畫布上兩點, 源自兩point, 長度延伸的兩點, line_id

        # 讀檔的圖
        self.inputCurrentIndex = 0
        self.inputIndex = 0
        self.inputPoints = []
 
        # store record for step by step
        self.rpoints_id = []
        self.rpoints = []
        self.redges = []
        
        # 輸出用: 兩層列表，第一層存取每個圖的點，第二層存取每個圖的點座標
        self.outputPoints = [] # 繪製的點 : [[(x, y)]]
        self.outputEdges = [] # 繪製的邊 : [[( draw1, draw2, point_a, point_b, edge_piont1, edge_point2)]] -> 畫布上兩點, 源自兩point, 長度延伸的兩點

    # 計算line兩端點的最大邊界
    # return endpoints -> [dx1, dy1, dx2, dy2]
    def calculate_line_endpoints(self, point1, point2, edge_status):
        x1, y1 = point1
        x2, y2 = point2
        
        # 計算斜率 function y = slope * x + b
        slope, b = self.find_line(point1, point2)
        # 計算直線的兩端點
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
        
        # print(f"calculate_line_endpoints: {dx1, dy1, dx2, dy2}")
        return dx1, dy1, dx2, dy2

    # return edge id
    def add_line(self, point1, point2, edge_status, color='blue'): # edge_status = [left, mid, right] -> left=1 : <-1 2, mid=1 : 1-2, right=1 : 1 2-> ; excaption [0,0,0] means perpendicular line 
        dx1, dy1, dx2, dy2 = self.calculate_line_endpoints(point1, point2, edge_status)
        canvasP = self.clip_line((dx1, dy1), (dx2, dy2))
        if (canvasP == None):
            return None
        canvas_x1, canvas_y1 = canvasP[0]
        canvas_x2, canvas_y2 = canvasP[1]

        # 畫線
        eID = self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=color, tags="line")
        self.edges.append([canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2], eID])
        return eID

    # 裁切線段回傳畫布上兩端點 -> return [[x1, y1], [x2, y2]]
    def clip_line(self, point1, point2):

        line_a, line_b = self.find_line(point1, point2)
        x1, y1 = point1
        x2, y2 = point2
        canvas_x1, canvas_y1 = point1
        canvas_x2, canvas_y2 = point2
        # 如果整條線段都在畫布外，則不畫
        if ((x1<0 or x1>self.width) and (x2<0 or x2>self.width) and (y1<0 or y1>self.length) and (y2<0 or y2>self.length)):
            return [[0, 0], [0, 0]]

        if line_a is None:  # 處理垂直線的邊界
            if y1 < 0:
                canvas_y1 = 0
            elif y1 > self.length:
                canvas_y1 = self.length
            if y2 < 0:
                canvas_y2 = 0
            elif y2 > self.length:
                canvas_y2 = self.length
        else:
            if x1 < 0:
                canvas_x1 = 0
                canvas_y1 = line_a * canvas_x1 + line_b
            elif x1 > self.width:
                canvas_x1 = self.width
                canvas_y1 = line_a * canvas_x1 + line_b
            if x2 < 0:
                canvas_x2 = 0
                canvas_y2 = line_a * canvas_x2 + line_b
            elif x2 > self.width:
                canvas_x2 = self.width
                canvas_y2 = line_a * canvas_x2 + line_b

        x1, y1 = canvas_x1, canvas_y1
        x2, y2 = canvas_x2, canvas_y2

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
        # if (test):
        print(f"add point: {point}: {point_id}")
        self.points_id.append(point_id)

    # clear all points and lines
    def clear_all(self):
        """清除畫布上所有物件，並重置點列表。"""
        self.canvas.delete("all")  # 清除畫布上的所有物件
        self.canvas.delete("line")
        self.canvas.delete("point")
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
    
    #clear line by id
    def clear_lineID(self, id):
        print("clear line",end=" ")
        print(id)
        self.canvas.delete(id)

    # clear all lines
    def clear_lines(self):
        # self.edges_id.clear()
        self.edges.clear()
        self.canvas.delete("line")

    # add a perpendicular line #  return draw_edge -> [canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]]
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
            
        canvasP = self.clip_line((canvas_x1, canvas_y1), (canvas_x2, canvas_y2))
        if (canvasP == None):
            return None
        canvas_x1, canvas_y1 = canvasP[0]
        canvas_x2, canvas_y2 = canvasP[1]

        draw_edge = [canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]]
        return draw_edge

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
    def lineOtherPoint(self, point, line_slope, line_b, dir='x'):
        x, y = point
        if (line_slope == None):
            return (x, maxsize)
        elif (line_slope == 0):
            return (maxsize, y)
        else:
            if (dir=='x'):
                new_x = maxsize
                new_y = line_slope * new_x + line_b
                return [new_x, new_y]
            elif (dir=='y'):
                new_y = maxsize
                new_x = (new_y - line_b) / line_slope
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
                print("findLine error", a, b)
            else:
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1
            return [a, b]

    # 透過兩條線找出交點 回傳: 兩條線的交點 TODO bug: check a1, a2 with NoneType
    def find_intersection(self, a1, b1, a2, b2):
        # a1, b1: 第一條線的斜率和截距
        # a2, b2: 第二條線的斜率和截距
        # print(f"find_intersection: {a1, b1, a2, b2}")
        if a1 is None and b1 is None or a2 is None and b2 is None:
            print('find_intersection() error: 兩條線無法找出交點')
            return None

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

    # return [ Point, Center, [0,0,1]]
    def find_line_degreeMoreThan90(self, Center, P_large, P1, P2, mid_L1, mid_L2, mid_12):
        line1 = (self.add_perpendicular_line(P1, P2))[4:6]
        line2 = [mid_L1, mid_L2]
        Point = self.intersectionTwoLineparts(line1, line2)
        if (Point[0]):
            return [ Point[1], Center, [0,0,1]]
        else:
            print("find_line_degreeMoreThan90 error: no intersection")

    # 判斷三角形並找出要畫的線段
    # return 三組欲畫的線段，[(mid, one, status, point1, point2), (mid, two, status, point1, point2), (mid, three, status, point1, point2)]
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
            edges.append([Center, ab, [0,1,1], A, B])
            edges.append([Center, bc, [0,1,1], B, C])
            edges.append([Center, ac, [0,1,1], A, C])
        else:   # 鈍角三角形 or 直角三角形
            print("鈍角三角形")
            if (cos_C <= 0):
                print("cos_C <= 0")
                edges.append([Center, bc, [0,1,1], B, C])
                edges.append([Center, ac, [0,1,1], A, C])
                edgeFind = self.find_line_degreeMoreThan90(Center, C, A, B, bc, ac, ab)
                print(edgeFind)
                edgeFind.append(A)
                edgeFind.append(B)
                edges.append(edgeFind)
            elif (cos_A <= 0):
                print("cos_A <= 0")
                edges.append([Center, ab, [0,1,1], A, B])
                edges.append([Center, ac, [0,1,1], A, C])
                edgeFind = self.find_line_degreeMoreThan90(Center, A, B, C, ab, ac, bc)
                print(edgeFind)
                edgeFind.append(B)
                edgeFind.append(C)
                edges.append(edgeFind)
            elif (cos_B <= 0):
                print("cos_B <= 0")
                edges.append([Center, ab, [0,1,1], A, B])
                edges.append([Center, bc, [0,1,1], B, C])
                edgeFind = self.find_line_degreeMoreThan90(Center, B, A, C, ab, bc, ac)
                print(edgeFind)
                edgeFind.append(A)
                edgeFind.append(C)
                edges.append(edgeFind)

        return edges

    # 計算點是否有在線段上 -> return True or False
    def pointOnLine(self, point, line_point1, line_point2):
        if test and test_index <= 1:
            print(f"------------pointOnLine show------------")
            print(f"point: {point}")
            print(f"line_point1: {line_point1}")
            print(f"line_point2: {line_point2}")
            print(f"------------pointOnLine end------------")

        # 精度問題 -> round 4 位
        if (point == line_point1 or point == line_point2):
            return False
        online_flag = False
        onpart_flag = False
        slope, b = self.find_line(line_point1, line_point2)
        if (slope == None):
            if (round(point[0],4) == round(line_point1[0], 4)):
                online_flag = True
                print(f"online_flag: {online_flag}")
        else:
            if (round(point[1], 4) == round(slope * point[0] + b, 4)):
                online_flag = True
                print(f"online_flag: {online_flag}")
            else:
                online_flag = False
                print(f'{point[1]} != {slope} * {point[0]} + {b} = {slope * point[0] + b}')
        print(f"dbcheck pointOnLine: {online_flag}")
        if (online_flag):
            if ((point[0] >= min(line_point1[0], line_point2[0]) and (point[0] <= max(line_point1[0], line_point2[0]))) and 
                (point[1] >= min(line_point1[1], line_point2[1]) and (point[1] <= max(line_point1[1], line_point2[1])))):
                onpart_flag = True
                print(f"onpart_flag: {onpart_flag}")
        print(f"pointOnLine: {online_flag, onpart_flag}")
        return onpart_flag

    # 計算兩線段是否有交點 -> return [T or F, [x, y]]  TODO check return , ERROR
    def intersectionTwoLineparts(self, line1, line2):
        print("intersection in", line1, line2)
        # line1, line2: 兩條線段的座標 ; 回傳: 是否有交點, 交點座標
        slope1, b1 = self.find_line(line1[0], line1[1])
        slope2, b2 = self.find_line(line2[0], line2[1])
        # 找出交點
        intersection = []
        if (slope1 == slope2): # 例外處理
            if (b1 == b2): # 兩條線平行
                print("intersectionTwoLineparts error: 共線")
            else: # 兩條線垂直
                print("intersectionTwoLineparts error: 平行")
            return [False, []]
        elif (slope1 == None):
            x = line1[0][0]
            y = slope2 * x + b2
            intersection = [x, y]
        elif (slope2 == None):
            x = line2[0][0]
            y = slope1 * x + b1
            intersection = [x, y]
        else:
            intersection = self.find_intersection(slope1, b1, slope2, b2)
        print(f"intersectionTwoLineparts: find-> {intersection}")
        if (intersection == None):
            return [False, []]
        else:
            # print(intersection, line1[0], line1[1], line2[0], line2[1])
            print("---------------------------------------------------------------------------------------------")
            status1 = self.pointOnLine(intersection, line1[0], line1[1])
            status2 = self.pointOnLine(intersection, line2[0], line2[1])
            print("status1, status2", status1, status2)
            if (status1 and status2):
                print(status1, intersection, line1[0], line1[1])
                print(status2, intersection, line2[0], line2[1])
                print("---------------------------------------------------------------------------------------------")
                return [True, intersection]
            else:
                print("---------------------------------------------------------------------------------------------")
                return [False, []]
            # return [False, []]
            # if (self.pointOnLine(intersection, line1[0], line1[1]) and self.pointOnLine(intersection, line2[0], line2[1])):
            #     print("return intersection", intersection)
            #     print("---------------------------------------------------------")
            #     return [True, intersection]
            # else: 
            #     print("---------------------------------------------------------")
            #     return [False, []]
            
# calculate---------------------------------------------------------------------------------------------------------------
class voronoi():
    def __init__(self, canvas, graph, uiapp):
        self.uiapp = uiapp
        self.canvas = canvas
        self.graph = graph

        # store diagram
        self.points = []
        self.chl = []
        self.chr = []
        self.ch  = []
        self.hpedges = []
        self.vedges = []
        # store voronoi diagram
        self.lvor = []
        self.rvor = []
        self.vor = []

    def resetVoronoi(self):
        self.points.clear()
        self.chl.clear()
        self.chr.clear()
        self.ch.clear()
        self.hpedges.clear()
        self.vedges.clear()
        self.lvor.clear()
        self.rvor.clear()
        self.vor.clear()

    def compute_voronoi(self):
        if (len(self.graph.points) <=1):
            return self.graph.points, []
        elif (len(self.graph.points) == 2):
            drawEdge = self.graph.add_perpendicular_line(self.graph.points[0], self.graph.points[1])
            eid = self.graph.add_line(drawEdge[0], drawEdge[1], [0, 1, 0])
            # eID = self.canvas.create_line(drawEdge[0][0], drawEdge[0][1], drawEdge[1][0], drawEdge[1][1], fill="blue", tags="line")
            drawEdge.append(eID)
            self.graph.edges.append(drawEdge)
            return self.graph.points, drawEdge
        elif (len(self.graph.points) == 3):
            ch ,drawEdges = self.compute_voronoi_three(self.graph.points)
            for edge in drawEdges:
                print(edge)
                eID = self.graph.add_line(edge[0], edge[1], [0, 1, 0])
                edge[6] = eID
            return ch ,drawEdges
        else:
            self.voronoi_start(self.graph.points, self.graph.points_id)

    def voronoi_start(self, points, points_id):
        if (len(points) <=1):
            return points, [] # return v_points, v_edges
        elif (len(points) == 2):
            drawEdge = self.graph.add_perpendicular_line(points[0], points[1]) # return [canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]]
            print(drawEdge)
            eID = self.canvas.create_line(drawEdge[0][0], drawEdge[0][1], drawEdge[1][0], drawEdge[1][1], fill="blue", tags="line")
            Edgepoint = [drawEdge[0], drawEdge[1], points[0], points[1], drawEdge[4], drawEdge[5], eID]
            self.graph.edges.append(Edgepoint)
            return self.convex_hull(points), [Edgepoint]
        elif (len(points) == 3):
            ch ,drawEdges = self.compute_voronoi_three(points)
            return ch ,drawEdges
        else:
            left, left_id, right, right_id = self.divide(points, points_id)
            # draw left convex hull
            self.uiapp.stop()
            lpoints, lvor = self.voronoi_start( left,  left_id) # left
            for Bpoint in lpoints:
                self.canvas.create_oval(Bpoint[0] - 3, Bpoint[1] - 3, Bpoint[0] + 3, Bpoint[1] + 3, fill='blue')
            self.lvor = (lvor)

            # draw right convex hull
            self.uiapp.stop()
            rpoints, rvor = self.voronoi_start(right, right_id) # right
            self.rvor = (rvor)
            for Bpoint in rpoints:
                self.canvas.create_oval(Bpoint[0] - 3, Bpoint[1] - 3, Bpoint[0] + 3, Bpoint[1] + 3, fill='blue')

            # merge
            self.uiapp.stop()
            # mpoints, mvor = 
            self.merge(left, right) # merge(left, right)
            return left+right, self.vor
    
    # devide points into left and right -> return [left, left_id, right, right_id]
    def divide(self, points, points_id):
        # 根據x進行排序 並分成左右兩邊 sort points and points_id together
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                if (points[i][0] > points[j][0]):
                    points[i], points[j] = points[j], points[i]
                    points_id[i], points_id[j] = points_id[j], points_id[i]
        mid = len(points) // 2
        left, right = points[:mid], points[mid:]
        left_id, right_id = points_id[:mid], points_id[mid:]
        # if test==True and test_index <= 1:
        #     print("-----devide-----")
        #     print(left, right)
        #     print("-----devideEnd-----")
        return left, left_id, right, right_id

    def merge(self, left, right):
        # merge hull and find lower and upper tangent
        chl = self.convex_hull(left)
        chr = self.convex_hull(right)
        merge_ch, lower, upper = self.merge_hull(chl, chr)
        print("merge_ch", merge_ch)
        print("lower", lower)
        print("upper", upper)
        # draw merge convex hull
        for i in range(len(merge_ch)):
            # if (lower)
            if (i != len(merge_ch)-1):
                self.ch.append(self.graph.add_line(merge_ch[i], merge_ch[i+1], [0, 1, 0], 'gray'))
            else:
                self.ch.append(self.graph.add_line(merge_ch[0], merge_ch[i], [0, 1, 0], 'gray'))
        # draw voronoi left and right
        print("---------------vorstart-------------")
        print('self.lvor', len(self.lvor))
        # for vor in self.lvor:
        #     print(vor)
        for i in range(len(self.lvor)):
            # draw
            # print(self.lvor[i])
            eID = self.graph.add_line(self.lvor[i][0], self.lvor[i][1], [0,1,0], 'purple')
            self.lvor[i][6] = eID
        # for vor in self.rvor:
        #     print(vor)
        for i in range(len(self.rvor)):
            # draw
            # print(self.rvor[i])
            eID = self.graph.add_line(self.rvor[i][0], self.rvor[i][1], [0,1,0], 'green')
            self.rvor[i][6] = eID
        print("--------------end--------------------")
        self.uiapp.stop()
        # delete convex hull
        for id in self.ch:
            self.graph.clear_lineID(id)
        self.ch.clear()


        self.vor = self.lvor + self.rvor
        self.hyper_plane(lower, upper)
        # voronoi
        # self.merge()
        # self.convex_hull(left + right)

    # return ch <- points
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
        # self.uiapp.stop()
        chEdges = []
        for i in range(len(ch)):
            eID = self.graph.add_line(ch[i], ch[(i + 1) % len(ch)], [0, 1, 0], 'gray')  # Connect points in hull
            chEdges.append([ch[i], ch[(i + 1) % len(ch)], [0, 1, 0], eID])

        self.uiapp.stop()
        self.graph.clear_lines()
        return ch #, chEdges
    
    # return angle -> polar angle with respect to the base point
    def angle(self, o, p):  # calculate polar angle with respect to the base point
        return math.atan2(p[1] - o[1], p[0] - o[0])
    
    # return cross product
    def cross(self, o, a, b): # cross product
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    # return True if a is clockwise from b with respect to the origin o
    def compare_angle(self, o, a, b):
        return self.cross(o, a, b) > 0

    # return self.convex_hull(chl+chr), lower_tangent, upper_tangent
    def merge_hull(self, chl, chr):
        # 找出左凸包的最右點和右凸包的最左點
        rightmost_chl = max(chl, key=lambda x: x[0])  # 左凸包最右點
        leftmost_chr = min(chr, key=lambda x: x[0])  # 右凸包最左點
        
        # 找到這些點在各自列表中的索引
        i = chl.index(rightmost_chl)  # 左凸包的起始索引
        j = chr.index(leftmost_chr)  # 右凸包的起始索引

        # 找下公切線
        while True:
            moved = False
            # 固定右側點，移動左側點（順時針旋轉）
            while self.cross(chr[j], chl[i], chl[(i + 1) % len(chl)]) < 0:
                i = (i + 1) % len(chl)  # 順時針移動左側點
                moved = True
            # 固定左側點，移動右側點（逆時針旋轉）
            while self.cross(chl[i], chr[j], chr[(j - 1) % len(chr)]) > 0:
                j = (j - 1) % len(chr)  # 逆時針移動右側點
                moved = True
            # 檢查是否三點共線，且有更近的點需要更新
            if self.cross(chr[j], chl[i], chl[(i + 1) % len(chl)]) == 0:
                if self.graph.distance(chr[j], chl[i]) > self.graph.distance(chr[j], chl[(i + 1) % len(chl)]):
                    i = (i + 1) % len(chl)
                    moved = True
            if self.cross(chl[i], chr[j], chr[(j - 1) % len(chr)]) == 0:
                if self.graph.distance(chl[i], chr[j]) > self.graph.distance(chl[i], chr[(j - 1) % len(chr)]):
                    j = (j - 1) % len(chr)
                    moved = True
            # 如果兩側都不再移動，找到下公切線
            if not moved:
                break

        lower_tangent = [chl[i], chr[j]]  # 下公切線的兩個端點

        # 找上公切線
        i = chl.index(rightmost_chl)  # 重置索引
        j = chr.index(leftmost_chr)
        while True:
            moved = False
            # 固定右側點，移動左側點（逆時針旋轉）
            while self.cross(chr[j], chl[i], chl[(i - 1) % len(chl)]) > 0:
                i = (i - 1) % len(chl)  # 逆時針移動左側點
                moved = True
            # 固定左側點，移動右側點（順時針旋轉）
            while self.cross(chl[i], chr[j], chr[(j + 1) % len(chr)]) < 0:
                j = (j + 1) % len(chr)  # 順時針移動右側點
                moved = True
            # 檢查是否三點共線，且有更近的點需要更新
            if self.cross(chr[j], chl[i], chl[(i - 1) % len(chl)]) == 0:
                if self.graph.distance(chr[j], chl[i]) > self.graph.distance(chr[j], chl[(i - 1) % len(chl)]):
                    i = (i - 1) % len(chl)
                    moved = True
            if self.cross(chl[i], chr[j], chr[(j + 1) % len(chr)]) == 0:
                if self.graph.distance(chl[i], chr[j]) > self.graph.distance(chl[i], chr[(j + 1) % len(chr)]):
                    j = (j + 1) % len(chr)
                    moved = True
            # 如果兩側都不再移動，找到上公切線
            if not moved:
                break

        upper_tangent = [chl[i], chr[j]]  # 上公切線的兩個端點

        # 合併凸包
        # 收集下公切線左側到上公切線左側的點
        merged_hull = []
        idx = chl.index(lower_tangent[0])
        while True:
            merged_hull.append(chl[idx])
            if chl[idx] == upper_tangent[0]:
                break
            idx = (idx + 1) % len(chl)

        # 收集上公切線右側到下公切線右側的點
        idx = chr.index(upper_tangent[1])
        while True:
            merged_hull.append(chr[idx])
            if chr[idx] == lower_tangent[1]:
                break
            idx = (idx + 1) % len(chr)

        # ensure upper is above lower
        if ((lower_tangent[0][1] >= upper_tangent[0][1] and lower_tangent[1][1] >= upper_tangent[1][1]) or (lower_tangent[0][0] <= upper_tangent[0][0] and lower_tangent[1][0] <= upper_tangent[1][0])):
            lower_tangent, upper_tangent = upper_tangent, lower_tangent

        # self.graph.add_line(lower_tangent[0], lower_tangent[1], [0, 1, 0], 'red')
        # self.graph.add_line(upper_tangent[0], upper_tangent[1], [0, 1, 0], 'red')
        
        # print(merged_hull)
        return self.convex_hull(chl+chr), lower_tangent, upper_tangent
    
    def hyper_plane(self, lower, upper):
        # draw lower and upper tangent
        if test and test_index <= 2:
            # self.graph.add_line(lower[0], lower[1], [0, 1, 0], 'red')
            self.graph.add_line(lower[0], lower[1], [0, 1, 0], 'green')
        # use the perpendicular line to find the hyperplane -> use lower
        drawEdge = self.graph.add_perpendicular_line(lower[0], lower[1])
        eID = self.canvas.create_line(drawEdge[0][0], drawEdge[0][1], drawEdge[1][0], drawEdge[1][1], fill="green", tags="line")
        # 第一次會與lower_tangent相交
        if drawEdge[4][1] > drawEdge[5][1]:
            drawEdge[4], drawEdge[5] = drawEdge[5], drawEdge[4]
            drawEdge[0], drawEdge[1] = drawEdge[1], drawEdge[0]
        # store low and up in hpUp and hpLow
        hpLow, hpUp = drawEdge[4], drawEdge[5]
        footl, footr = lower[0], lower[1]
        hpedge = [drawEdge[0], drawEdge[1], footl[0], footr[1], drawEdge[4], drawEdge[5], eID]
        newHpedges = []
        
        # from upper to lower to find the first intersection point and line -> return first intersection point and line
        # 最多交集len(vor)條線段
        end_flag = False
        if test and test_index <= 2:
            print('vor:', len(self.vor))
        skipID = -1
        oldtouchLine = []
        last_intersection = []
        while(not end_flag):
            intersections_flag = False
            intersections = []
            touchLine = []
            for j in range(len(self.vor)):
                if (test and test_index <= 2):
                    self.graph.add_line(self.vor[j][0], self.vor[j][1], [0, 1, 0], 'orange')
                    self.uiapp.stop()
                # use intersectionTwoLineparts to find intersection point
                intersection_flag = False
                intersection_flag, intersection = self.graph.intersectionTwoLineparts( [hpedge[4], hpedge[5]], [self.vor[j][4], self.vor[j][5]]) # 計算兩線段是否有交點 -> return [T or F, [x, y]]
                if (intersection_flag):
                    intersections_flag = True
                    if (test and test_index <= 2):
                        self.canvas.create_oval(intersection[0] - 3, intersection[1] - 3, intersection[0] + 3, intersection[1] + 3, fill='blue')
                        # self.uiapp.stop()
                    intersections.append([intersection, self.vor[j]])
            # 如果有找到交點，則找出最近的交點，由lower往upper找
            if (intersections_flag):
                # sort intersection by y
                # intersections.sort(key=lambda x: x[1])
                intersections.sort(key=lambda x: x[0][1])
                intersection = intersections[0][0]
                touchLine = intersections[0][1]
                if skipID == intersections[0][1][6]:
                    if len(intersections) > 1:
                        intersection = intersections[1][0]
                        touchLine = intersections[1][1]
                # intersection = intersections[0]
                if test and test_index <= 2:
                    self.canvas.create_oval(intersection[0] - 3, intersection[1] - 3, intersection[0] + 3, intersection[1] + 3, fill='yellow')
                    # self.uiapp.stop()
            else:
                # the last hyperplane
                end_flag = True
                # draw last hyperplane
                drawEdge = self.graph.add_perpendicular_line(upper[0], upper[1])
                # sort drawEdge, y1 < y2
                if drawEdge[4][1] > drawEdge[5][1]:
                    drawEdge[4], drawEdge[5] = drawEdge[5], drawEdge[4]
                    drawEdge[0], drawEdge[1] = drawEdge[1], drawEdge[0]
                drawEdge[1] = drawEdge[5] = last_intersection
                
                eID = self.canvas.create_line(drawEdge[0][0], drawEdge[0][1], drawEdge[1][0], drawEdge[1][1], fill="green", tags="line")
                drawEdge.append(eID)
                newHpedges.append(drawEdge)

                print('-------------------end_flag-------------------')
                # self.uiapp.stop()
                break
            # 先處理前一個hyperplane  # TYPE -> hpedge = [low_drawEdge[0], Up_drawEdge[1], footl[0], footr[1], low_drawEdge[4], Up_drawEdge[5], eID]
            self.graph.clear_lineID(hpedge[6])
            self.uiapp.stop()

            hpUp = intersection
            drawLow, drawUp = self.graph.clip_line(hpLow, hpUp)

            # print('drawLow, drawUp, hpLow, hpUp')
            # print(drawLow, drawUp, hpLow, hpUp)
            # self.uiapp.stop()
            # clip, store and draw hyperplane TODO add line after
            eID = self.graph.add_line(drawLow, drawUp, [0,1,0], "orange")
            Cal_HpEdge = [drawLow, drawUp, hpedge[2], hpedge[3], hpLow, hpUp, eID]
            newHpedges.append(Cal_HpEdge)
            # self.uiapp.stop()

            # define new footl and footr
            newFoot = []
            newFootCandidate = [touchLine[2], touchLine[3]]
            if ((newFootCandidate[0] == footl) or (newFootCandidate[1] == footl)):
                newFoot.append(footr)
                if (newFootCandidate[0] == footl):
                    newFoot.append(newFootCandidate[1])
                else:
                    newFoot.append(newFootCandidate[0])
            elif ((newFootCandidate[0] == footr) or (newFootCandidate[1] == footr)):
                newFoot.append(footl)
                if (newFootCandidate[0] == footr):
                    newFoot.append(newFootCandidate[1])
                else:
                    newFoot.append(newFootCandidate[0])
            print('oldFoot', footl, footr)
            print('newFoot', newFoot)
            footl, footr = newFoot[0], newFoot[1]
            if test and test_index <= 3:
                self.graph.add_line(footl, footr, [0, 1, 0], 'black')
            # self.uiapp.stop()
            # define new lower and upper
            slope, b = self.graph.find_perpendicular_line(footl, footr)
            print('-----------------------------')
            print('slope, b', slope, b)
            print(intersection)
            # self.uiapp.stop()
            
            point = self.graph.lineOtherPoint(intersection, slope, b, 'y')
            print('intersection', intersection)
            print('point', point)
            # self.uiapp.stop()
            if slope == 0:
                point[0] = intersection[0]
                point[1] = maxsize
            if test and test_index <= 2:
                self.graph.add_line(intersection, point, [0, 1, 1], 'purple')
                self.uiapp.stop()
            print('point', intersection, point)
            
            # self.uiapp.stop()

            px1, py1, px2, py2 = self.graph.calculate_line_endpoints(intersection, point, [0, 1, 1])
            newpoint = [[px1, py1], [px2, py2]]

            print('newpoint', newpoint)
            # self.uiapp.stop()
            hpLow, hpUp = newpoint[0], newpoint[1]
            drawLow, drawUp = self.graph.clip_line(hpLow, hpUp)
            hpedge = [drawLow, drawUp, footl, footr, newpoint[0], newpoint[1], eID]
            # newHpedges.append(hpedge)

            # TYPE -> hpedge = [low_drawEdge[0], Up_drawEdge[1], lower[0], lower[1], low_drawEdge[4], Up_drawEdge[5], eID]

            # 由intersection向下畫線
                      # Wipe : 找出碰到的第一條voronoi線段 並 擦除不要的部分: 遠離非共線的點
            if (intersection==[]):
                last_intersection = intersection
                oldtouchLine = touchLine
            else:
                delFlagDir = 0
                self.graph.clear_lineID(touchLine[6])
                po = intersection
                pa = touchLine[2]
                pl = touchLine[4]
                pr = touchLine[5]
                if test and test_index <= 2:
                    a = self.canvas.create_oval(pa[0] - 5, pa[1] - 5, pa[0] + 5, pa[1] + 5, fill='yellow')
                    b = self.canvas.create_oval(po[0] - 5, po[1] - 5, po[0] + 5, po[1] + 5, fill='black')
                    c = self.canvas.create_oval(touchLine[0][0] - 5, touchLine[0][1] - 5, touchLine[0][0] + 5, touchLine[0][1] + 5, fill='green')
                    d = self.canvas.create_oval(touchLine[1][0] - 5, touchLine[1][1] - 5, touchLine[1][0] + 5, touchLine[1][1] + 5, fill='red')
                    self.uiapp.stop()
                    self.canvas.delete(a)
                    self.canvas.delete(b)
                    self.canvas.delete(c)
                    self.canvas.delete(d)
                OA = [pa[0] - po[0], pa[1] - po[1]]
                OL = [pl[0] - po[0], pl[1] - po[1]]
                OR = [pr[0] - po[0], pr[1] - po[1]]
                # find the cos of OA, OL and OA, OR
                cosL = (OA[0] * OL[0] + OA[1] * OL[1]) / (math.hypot(*OA) * math.hypot(*OL))
                cosR = (OA[0] * OR[0] + OA[1] * OR[1]) / (math.hypot(*OA) * math.hypot(*OR))

                # 找出 hpLow to hpUp 的向量
                hpVec = [hpUp[0] - hpLow[0], hpUp[1] - hpLow[1]]
                # 找出 前一個hpedge的向量
                lastVec = [newHpedges[-1][4][0] - newHpedges[-1][5][0], newHpedges[-1][4][1] - newHpedges[-1][5][1]]
                # 找出 hpVec 及 lastVec 的cos
                cosHpVecLastVec = (hpVec[0] * lastVec[0] + hpVec[1] * lastVec[1]) / (math.hypot(*hpVec) * math.hypot(*lastVec))

                if test:
                    print('cosL, cosR', cosL, cosR)

                if (cosL * cosHpVecLastVec > 0): # delete left part # 一正一負 負的要刪除
                    delFlagDir = 1
                elif(cosR * cosHpVecLastVec > 0): # delete right part
                    delFlagDir = -1
                # delete the part of the line and delete from data structure, TODO delete from (vor:already delete from voronoi) ... and so on
                afterWipeUp = intersection
                afterWipeLow = []
                if (delFlagDir == 1):
                    afterWipeLow = pr
                else:
                    afterWipeLow = pl
                oldID = touchLine[6]
                afterWipeDrawLow, afterWipeDrawUp = self.graph.clip_line(afterWipeLow, afterWipeUp)
                # self.uiapp.stop()
                eID = self.graph.add_line(afterWipeDrawLow, afterWipeDrawUp, [0,1,0], "blue")
                skipID = eID
                NewTouchLine = [afterWipeDrawLow, afterWipeDrawUp, touchLine[2], touchLine[3], afterWipeLow, afterWipeUp, eID]
                self.canvas.create_line(afterWipeDrawLow[0], afterWipeDrawLow[1], afterWipeDrawUp[0], afterWipeDrawUp[1], fill="blue", tags="line")
                print('--------------------------------------------------------------')
                print('oldID', oldID)
                for i in range(len(self.vor)):
                    print(self.vor[i])
                    if self.vor[i][6] == oldID:
                        self.vor[i] = NewTouchLine
                print('--------------------------------------------------------------')
                for edge in self.vor:
                    print(edge)
                print('--------------------------------------------------------------')
                print(self.vor)
                self.uiapp.stop()
                last_intersection = intersection
                oldtouchLine = touchLine

        
        
        # 遍歷所有voronoi線段，找出Orphan Edge並刪除，orphan edge: 兩端點皆沒有和voronoi的兩端點相同相交
        allVertex = []
        for i in range(len(self.vor)):
            allVertex.append(self.vor[i][4])
            allVertex.append(self.vor[i][5])
        for i in range(len(newHpedges)):
            allVertex.append(newHpedges[i][4])
            allVertex.append(newHpedges[i][5])
        matchEdges = []
        orphanID = []
        print('allVertex')
        for vertex in allVertex:
            print(vertex)
        # self.uiapp.stop()
        for i in range(len(self.vor)):
            connect = 0
            for j in range(len(allVertex)):
                if ((round(self.vor[i][4][0], 4) == round(allVertex[j][0], 4)) and (round(self.vor[i][4][1], 4) == round(allVertex[j][1], 4))):
                    connect += 1
                if ((round(self.vor[i][5][0], 4) == round(allVertex[j][0], 4)) and (round(self.vor[i][5][1], 4) == round(allVertex[j][1], 4))):
                    connect += 1
            if (connect <= 2):
                orphanID.append(self.vor[i][6])
        # self.uiapp.stop()

        if test and test_index <= 2:
            print('vorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvor')
            for i in range(len(self.vor)):
                print(self.vor[i])
            self.uiapp.stop()
            print('vorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvorvor')

        for id in orphanID:
            for j in range(len(self.vor)):
                print('self.vor[j]', self.vor[j])
                self.uiapp.stop()
                if (self.vor[j][6] == id):
                    self.vor.pop(j)
                    self.graph.clear_lineID(id)
                    break


        self.hpedges.append(newHpedges)
        print('out of looop 936')
        self.graph.clear_lines()
        for i in range(len(self.vor)):
            self.graph.clear_lineID(self.vor[i][6])
            eID = self.canvas.create_line(self.vor[i][0][0], self.vor[i][0][1], self.vor[i][1][0], self.vor[i][1][1], fill="green", tags="line")
            self.vor[i][6] = eID
            self.graph.edges.append(self.vor[i])
        for i in range(len(newHpedges)):
            self.graph.clear_lineID(newHpedges[i][6])
            eID = self.canvas.create_line(newHpedges[i][0][0], newHpedges[i][0][1], newHpedges[i][1][0], newHpedges[i][1][1], fill="red", tags="line")
            newHpedges[i][6] = eID
            self.graph.edges.append(newHpedges[i])
        # self.uiapp.stop()
        for edge in newHpedges:
            self.vor.append(edge)
        # print('self.vor', len(self.vor))
        # print(self.vor)
        # self.uiapp.stop()
        print('self.hpedges', len(self.hpedges))
        print(self.hpedges)
        # self.uiapp.stop()
        self.hpedges.clear()

        if test and test_index <= 3:
            for edge in self.vor:
                print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                print(edge)
                self.uiapp.stop()
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        # self.uiapp.stop()



    # return self.convex_hull(points), EdgePoints
    def compute_voronoi_three(self, points):
        # store edges return
        EdgePoints = []
        # 找出三點共線
        a, b = self.graph.find_line(points[0], points[1])
        a1, b1 = self.graph.find_line(points[0], points[2])
        if (test and test_index <= 1):
            print(f'compute_voronoi: y = {a} x + {b}; y = {a1} x + {b1}')
        # 三點共線 TODO change save structure
        if (a == None and a1 == None):
            if (test and test_index <= 1):
                print("三點共線")
            if ((points[0][1] < points[1][1] and points[1][1] < points[2][1]) or (points[0][0] > points[1][0] and points[1][0] > points[2][0])):
                print(f'{points[0][1]} < {points[1][1]} < {points[2][1]} or {points[0][0]} > {points[1][0]} > {points[2][0]}')
                center = 1
            elif ((points[1][1] < points[0][1] and points[0][1] < points[2][1]) or (points[1][0] > points[0][0] and points[0][0] > points[2][0])):
                print(f'{points[1][1]} < {points[0][1]} < {points[2][1]} or {points[1][0]} > {points[0][0]} > {points[2][0]}')
                center = 0
            else:
                print(f'{points[2][1]} < {points[0][1]} < {points[1][1]} or {points[2][0]} > {points[0][0]} > {points[1][0]}')
                center = 2
            # 畫出中垂線
            for i in range(3):
                if (i != center):
                    drawEdge = self.graph.add_perpendicular_line(points[center], points[i]) # return [canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]]
                    eID = self.canvas.create_line(drawEdge[0][0], drawEdge[0][1], drawEdge[1][0], drawEdge[1][1], fill="blue", tags="line")
                    drawEdge.append(eID)
                    EdgePoints.append(drawEdge)
                    self.graph.edges.append(drawEdge)
            
        elif (a == a1):
            if (test and test_index <= 1):
                print("三點共線-非垂直")
            if ((points[0][1] < points[1][1] and points[1][1] < points[2][1]) or 
                (points[0][1] > points[1][1] and points[1][1] > points[2][1]) or 
                (points[0][0] > points[1][0] and points[1][0] > points[2][0]) or
                (points[0][0] < points[1][0] and points[1][0] < points[2][0])):
                # print(f'case1: {points[0][1]} < {points[1][1]} < {points[2][1]} or {points[0][0]} > {points[1][0]} > {points[2][0]}')
                center = 1
            elif ((points[1][1] < points[0][1] and points[0][1] < points[2][1]) or 
                    (points[1][1] > points[0][1] and points[0][1] > points[2][1]) or
                    (points[1][0] > points[0][0] and points[0][0] > points[2][0]) or
                    (points[1][0] < points[0][0] and points[0][0] < points[2][0])):
                # print(f'case2: {points[1][1]} < {points[0][1]} < {points[2][1]} or {points[1][0]} > {points[0][0]} > {points[2][0]}')
                center = 0
            elif ((points[2][1] < points[0][1] and points[0][1] < points[1][1]) or 
                    (points[2][1] > points[0][1] and points[0][1] > points[1][1]) or
                    (points[2][0] > points[0][0] and points[0][0] > points[1][0]) or
                    (points[2][0] < points[0][0] and points[0][0] < points[1][0])):
                # print(f'case3: {points[2][1]} < {points[0][1]} < {points[1][1]} or {points[2][0]} > {points[0][0]} > {points[1][0]}')
                center = 2
            else:
                print('compute_voronoi 三點共線: error')
                print(points)
                
            # 畫出中垂線
            for i in range(3):
                if (i != center):
                    drawEdge = self.graph.add_perpendicular_line(points[center], points[i]) # return [canvasP[0], canvasP[1], point1, point2, [dx1, dy1], [dx2, dy2]]
                    eID = self.canvas.create_line(drawEdge[0][0], drawEdge[0][1], drawEdge[1][0], drawEdge[1][1], fill="blue", tags="line")
                    drawEdge.append(eID)
                    EdgePoints.append(drawEdge)
                    self.graph.edges.append(drawEdge)
        # 三點不共線
        else:
            center_x, center_y = self.graph.circumcenter(points[0], points[1], points[2])
            # 找出三邊的中點
            x1, y1 = self.graph.midpoint(points[0], points[1])
            x2, y2 = self.graph.midpoint(points[1], points[2])
            x3, y3 = self.graph.midpoint(points[0], points[2])

            # 找出三條要畫的線段
            drawEdges = self.graph.cal_triangle_line((center_x, center_y), points[0], points[1], points[2], (x1, y1), (x2, y2), (x3, y3))
            for edge in drawEdges: # edge =  (mid, one, status, point1, point2)
                EdgePoint = []
                dx1, dy1, dx2, dy2 = self.graph.calculate_line_endpoints(edge[0], edge[1], edge[2]) # [dx1, dy1, dx2, dy2]
                Point1 = [dx1, dy1]
                Point2 = [dx2, dy2]
                # [draw1, draw2, point_a, point_b, edge_piont1, edge_point2, id]
                # clip edge
                draw1, draw2 = self.graph.clip_line(Point1, Point2)
                eID = self.graph.add_line(draw1, draw2, [0, 1, 0])
                if eID==None:
                    print('error')
                EdgePoint.extend([draw1, draw2, edge[3], edge[4], Point1, Point2, eID])
                EdgePoints.append(EdgePoint)
                if test and test_index <= 1:
                    print(f"EdgePoint: {EdgePoint}")
                # print(EdgePoint)
                # self.uiapp.stop()
                self.graph.edges.append(EdgePoint)

        return self.convex_hull(points), EdgePoints

# gui---------------------------------------------------------------------------------------------------------------------
class UiApp:
    def __init__(self, master, Length, Width):
        self.master = master
        self.master.title("Voronoi")
        self.file_path = None
        self.length = Length
        self.width = Width
        self.stepbystep_flag = False
        self.pause_flag = False

        # 建立「Run」按鈕
        self.run_button = tk.Button(master, text="Run", command=self.run)
        self.run_button.pack(side="top")

        # 建立「NextGraph」按鈕
        self.next_button = tk.Button(master, text="NextGraph", command=self.nextGraph)
        self.next_button.pack(side="top")

        # 建立「Step by Step」按鈕
        self.stepbystep_button = tk.Button(master, text="Step by Step", command=self.stepbystep)
        self.stepbystep_button.pack(side="top")
        
        # 建立「Step by Step continue」按鈕
        self.interrupt_button = tk.Button(master, text="Continue", command=self.interrupt)
        self.interrupt_button.pack(side="top")

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
        self.voronoi_diagram = voronoi(self.canvas, self.graph, self)

    def get_voronoi_diagram(self):
        return self.voronoi_diagram

    def run(self, stop=False):
        """當點擊 Run 按鈕時，繪製連線。"""
        if stop:
            self.stepbystep_flag = True
            self.pause_flag = True
        else:
            self.stepbystep_flag = False
            self.pause_flag = False
        self.graph.clear_lines()
        self.master.update() # 更新畫布
        self.voronoi_diagram.compute_voronoi()
        self.master.update() # 更新畫布

    def clear(self):
        """當點擊 Clear 按鈕時，清除畫布。"""
        self.graph.clear_all()
        self.voronoi_diagram.resetVoronoi()
    
    def record_point(self, event):
        """紀錄點擊的 x, y 座標，並在畫布上繪製紅色小圓點。"""
        x, y = event.x, event.y
        self.graph.add_point((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
        if (test and test_index == 0):
            print(f"點紀錄於: ({x}, {y})")


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
        # delete the edge in self.graph.edges with edge[0] == edge[1] 
        cleanEdges = []
        for edge in self.graph.edges:
            if (edge[0] != edge[1]):
                # check cleanEdges and clip line again
                clipedge = self.graph.clip_line(edge[0], edge[1])
                cleanEdges.append(clipedge)
        
        
        for edge in cleanEdges:
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

    def stepbystep(self):
        self.voronoi_diagram.resetVoronoi()
        self.stepbystep_flag = True
        self.pause_flag = True
        self.run(stop=True)
        self.stepbystep_flag = False

    def interrupt(self):
        self.pause_flag = False
    
    def stop(self): # 等待使用者按下按鈕
        if (self.stepbystep_flag):
            self.pause_flag = True
            while self.pause_flag:  # 等待直到使用者按下按鈕
                self.master.update()  # 更新 GUI，避免卡住
                self.master.after(10)

# main---------------------------------------------------------------------------------------------------------------
test = False
test_index = 3

if __name__ == "__main__":
    # 設定長寬
    length = 600
    width = 600
    root = tk.Tk()
    app = UiApp(root, length, width)
    root.mainloop()