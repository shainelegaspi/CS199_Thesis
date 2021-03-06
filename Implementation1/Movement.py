import os, threading
from binascii import hexlify

class MovementThread(threading.Thread):
    cur_top = []
    location_start = 0
    location_end = 0
    file_content = ''
    dir_list = []

    def __init__(self, cur_top, location, file_content):
        self.cur_top = cur_top
        self.location_start = location
        self.location_end = location + 32
        self.file_content = file_content
        self.dir_list = os.listdir(os.path.dirname(os.path.realpath(__file__)))
        threading.Thread.__init__(self)

    def run(self):
        temp_top1 = ['',99999999]
        temp_top2 = ['',99999999]
        if self.location_start-32 < 0:
            temp_top1 = self.right_movement()
        elif self.location_end+32 > len(self.file_content):
            temp_top2 = self.left_movement()
        else:
            temp_top1 = self.right_movement()
            temp_top2 = self.left_movement()

        if self.cur_top[1] > temp_top1[1] and temp_top2[1] > temp_top1[1]:
            self.cur_top = temp_top1
        elif self.cur_top[1] > temp_top2[1] and temp_top1[1] > temp_top2[1]:
            self.cur_top = temp_top2

    def right_movement(self):
        temp_top = ['', 99999999]
        for iterations in range(1,33):
            count = 0
            start = self.location_start + iterations
            end = self.location_end + iterations
            temp_sig = self.file_content[start:end:]
            for filename in self.dir_list:
                with open(filename, 'r') as f:
                    content = f.read()
                    temp_content = hexlify(content)
                if temp_sig in temp_content:
                    count = count + 1
            false_positive_rate = float(count)/ len(self.dir_list)
            if temp_top[1] > false_positive_rate:
                temp_top=[]
                temp_top.append(temp_sig)
                temp_top.append(false_positive_rate)
        return temp_top

    def left_movement(self):
        temp_top = ['', 99999999]
        for iterations in range(1,33):
            count = 0
            start = self.location_start - iterations
            end = self.location_end - iterations
            temp_sig = self.file_content[start:end:]
            for filename in self.dir_list:
                with open(filename, 'r') as f:
                    content = f.read()
                    temp_content = hexlify(content)
                if temp_sig in temp_content:
                    count = count + 1
            false_positive_rate = float(count)/ len(self.dir_list)
            if temp_top[1] > false_positive_rate:
                temp_top=[]
                temp_top.append(temp_sig)
                temp_top.append(false_positive_rate)
        return temp_top

class ExtendThread(threading.Thread):
    cur_top = []
    location_start = 0
    location_end = 0
    file_content = ''
    dir_list = []

    def __init__(self, cur_top, location, file_content):
        self.cur_top = cur_top
        self.location_start = location
        self.location_end = location + 32
        self.file_content = file_content
        self.dir_list = os.listdir(os.path.dirname(os.path.realpath(__file__)))
        threading.Thread.__init__(self)

    def run(self):
        temp_top1 = ['',99999999]
        temp_top2 = ['',99999999]
        temp_top3 = ['',99999999]
        if self.location_start-32 < 0:
            temp_top1 = self.right_extend()
        elif self.location_end+32 > len(self.file_content):
            temp_top2 = self.left_extend()
        else:
            temp_top1 = self.right_extend()
            temp_top2 = self.left_extend()
            temp_top3 = self.dual_extend()

        if self.cur_top[1] > temp_top1[1] and temp_top2[1] > temp_top1[1] and temp_top3[1] > temp_top1[1]:
            self.cur_top = temp_top1
        elif self.cur_top[1] > temp_top2[1] and temp_top1[1] > temp_top2[1] and temp_top3[1] > temp_top2[1]:
            self.cur_top = temp_top2
        elif self.cur_top[1] > temp_top3[1] and temp_top1[1] > temp_top3[1] and temp_top2[1] > temp_top3[1]:
            self.cur_top = temp_top3

    def right_extend(self):
        temp_top = ['', 99999999]
        for iterations in range(1,33):
            count = 0
            end = self.location_end + iterations
            temp_sig = self.file_content[self.location_start:end:]
            for filename in self.dir_list:
                with open(filename, 'r') as f:
                    content = f.read()
                    temp_content = hexlify(content)
                if temp_sig in temp_content:
                    count = count + 1
            false_positive_rate = float(count)/ len(self.dir_list)
            if temp_top[1] > false_positive_rate:
                temp_top=[]
                temp_top.append(temp_sig)
                temp_top.append(false_positive_rate)
        return temp_top
        
    def left_extend(self):
        temp_top = ['', 99999999]
        for iterations in range(1,33):
            count = 0
            start = self.location_start - iterations
            temp_sig = self.file_content[start:self.location_end:]
            for filename in self.dir_list:
                with open(filename, 'r') as f:
                    content = f.read()
                    temp_content = hexlify(content)
                if temp_sig in temp_content:
                    count = count + 1
            false_positive_rate = float(count)/ len(self.dir_list)
            if temp_top[1] > false_positive_rate:
                temp_top=[]
                temp_top.append(temp_sig)
                temp_top.append(false_positive_rate)
        return temp_top

    def dual_extend(self):
        temp_top = ['', 99999999]
        for iterations in range(1,9):
            count = 0
            start = self.location_start - iterations
            end = self.location_end + iterations
            temp_sig = self.file_content[start:end:]
            for filename in self.dir_list:
                with open(filename, 'r') as f:
                    content = f.read()
                    temp_content = hexlify(content)
                if temp_sig in temp_content:
                    count = count + 1
            false_positive_rate = float(count)/ len(self.dir_list)
            if temp_top[1] > false_positive_rate:
                temp_top=[]
                temp_top.append(temp_sig)
                temp_top.append(false_positive_rate)
        return temp_top
