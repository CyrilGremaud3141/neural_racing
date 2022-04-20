import math
import cv2 as cv
import numpy as np

class NetRender:
    def __init__(self, res_x, res_y):
        self.resolution = res_y, res_x, 3
        self.bg_img = np.zeros(self.resolution)
        self.img = self.bg_img.copy()
        self.border = 20

    def drawNet(self, net):
        self.img = self.bg_img.copy()
        nodes = net.nodes
        connections = net.connections

        pos_dic = {}

        count_pos_x_dic = {}
        pos_x_dic = {}
        pos_list = []

        for no in nodes:
            pos_x = int((no.pos * (self.resolution[1] - (2 * self.border))) + self.border)
            pos_list.append(pos_x)

        max_count = 0
        for x in pos_list:
            count = pos_list.count(x)
            count_pos_x_dic[x] = count
            if count > max_count:
                max_count = count
        
        dis = (self.resolution[0] - (2 * self.border)) / (max_count - 1)

        for x in count_pos_x_dic.keys():
            pos_x_dic[x] = (self.resolution[0] / 2) - ((count_pos_x_dic[x] - 1) * dis / 2)

        for i, no in enumerate(nodes):
            pos_x = pos_list[i]
            
            pos_y = int(pos_x_dic[pos_x])
            pos_x_dic[pos_x] += dis

            pos_dic[no] = (pos_x, pos_y)

        for conn in connections:
            weight = conn.weight
            col_val = min(255, abs(weight) * 300)
            if weight >= 0:
                color = (255 - col_val, 255 - col_val, col_val)
            else:
                color = (col_val, 255 - col_val, 255 - col_val)
            cv.line(self.img, pos_dic[conn.input_node], pos_dic[conn.output_node], color, min(4, max(1, (int(abs(weight * 3))))))

        for no in pos_dic:
            cv.circle(self.img, pos_dic[no], 1, (0, 255, 0), 2)


    def show(self):
        cv.imshow("NeuralNet", self.img)
        cv.waitKey(1)