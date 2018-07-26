# coding=utf-8
import csv
import random
import numpy as np
from datetime import datetime
from queue import PriorityQueue, Queue

from numpy import array, zeros
from scipy.optimize import linear_sum_assignment
from workflows.multiwl import y_truth, y_pred, type_dict, PRICE, V, WL

class OptsClass:

    default_pos = 'D:\\PycharmProjects\\arima_MDGT\\graphdat\\C_30\\'

    csv_pos = 'D:\\PycharmProjects\\arima_MDGT\\arima\\'


    def __init__(self):
        super(OptsClass, self).__init__()


    def origin(self, csv_file):
        # 读取原始数据 matrix.csv
        data = []
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                y = [float(i) for i in list(row.values())]
                data.append(y)
        return data


    def wl(self, wl, index):
        c = []
        current = WL[index]
        f = open(self.default_pos + 'wl.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        for i, task in enumerate(wl):
            x = type_dict[task[1][2]]
            print(task, x)
            c.append([current[0 + x], current[3 + x], current[6 + x]])
        t_wl = np.array(c).T
        f.write(str(t_wl) + '\n')
        f.close()
        return t_wl


    def inputET(self, tasks, index):
        c = []
        # current = y_truth[index]
        current = y_pred[index]
        f = open(self.default_pos+'et.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        for i, task in enumerate(tasks):
            x = type_dict[task[1][2]]
            print(task, x)
            c.append([current[0 + x], current[3 + x], current[6 + x]])
        t_et = np.array(c).T
        f.write(str(t_et) + '\n')
        f.close()
        return t_et


    def task2queue(self, bag_of_tasks, start, end, level):
        # 任务集切分
        ta_queue = PriorityQueue(10000)
        tasks = bag_of_tasks[start:end]
        for task in tasks:
            ta_queue.put((level, task))
            bag_of_tasks.remove(task)
        return ta_queue, bag_of_tasks


    def tasks_pool(self, bag_of_tasks, L):
        ta_pool = Queue()
        for l in range(L):
            if not len(bag_of_tasks) == 0:
                tll = []
                # tl, tx = t_queue('t', tn, 0, random.randint(8, 10), l)
                tl, tx = self.task2queue(bag_of_tasks, 0, 3, l)
                while not tl.empty():
                    tll.append(tl.get())
                ta_pool.put(tll)
        return ta_pool


    def rand_wl(self, t, rs, re):
        """
        生成基于随机数的负载列表
        :param t: 当前任务队列的集合
        :param rs: 随机数下限
        :param re: 随机数上限
        :return: wl
        """
        c = []
        f = open(self.default_pos+'wl.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        for i in range(len(V)):
            c.append([random.randint(rs, re) for j, t in enumerate(t)])
        wl = array(c)
        f.write(str(wl) + '\n')
        f.close()
        return wl


    def inputPT(self, t, et):
        pt = zeros(et.shape)
        f = open(self.default_pos+'pt.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        for i, v in enumerate(V):
            for j, x in enumerate(t):
                m = v + str(type_dict[x[1][2]] + 1)
                pt[i][j] = et[i][j] * PRICE[m]
        f.write(str(pt) + '\n')
        f.close()
        return pt


    def ass1(self, t, et):
        """
        生成部署方案１－最小化最大完成时间
        :param t: 任务
        :param et: 执行时间矩阵
        :return: 预部署方案1
        """
        pre_ass1 = {}
        f1 = zeros(et.shape)
        delays = []
        f = open(self.default_pos+'ass1.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        c_row_ind, c_col_ind = linear_sum_assignment(et)
        c_min_sum = et[c_row_ind, c_col_ind].sum()
        f.write('f1' + '\t' + str(c_min_sum) + '\n')
        for i in range(min(et.shape)):
            f1[c_row_ind[i]][c_col_ind[i]] = et[c_row_ind[i]][c_col_ind[i]]
            pre_ass1[V[c_row_ind[i]]] = {t[c_col_ind[i]]: round(et[c_row_ind[i]][c_col_ind[i]], 4)}
            delays.append((V[c_row_ind[i]], t[c_col_ind[i]], et[c_row_ind[i]][c_col_ind[i]]))
        f.write(str(f1) + '\n')
        f.write('ass1' + str(pre_ass1) + '\n')
        f.close()
        return pre_ass1, f1, delays


    def ass1_fifo(self, t, et):
        """
        生成部署方案１-- fifo 最大完成时间
        :param t: 任务
        :param et: 执行时间矩阵
        :return: 预部署方案1
        """
        pre_ass1_fifo = {}
        f1 = zeros(et.shape)
        delays = []
        f = open(self.default_pos+'ass1.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        c_row_ind, c_col_ind = [i for i in range(et.shape[0])], [j for j in range(et.shape[1])]
        random.shuffle(c_row_ind)
        random.shuffle(c_col_ind)
        # f.write('f1' + '\t' + str(c_min_sum) + '\n')
        for i in range(min(et.shape)):
            f1[c_row_ind[i]][c_col_ind[i]] = et[c_row_ind[i]][c_col_ind[i]]
            pre_ass1_fifo[V[c_row_ind[i]]] = {t[c_col_ind[i]]: round(et[c_row_ind[i]][c_col_ind[i]], 4)}
            delays.append((V[c_row_ind[i]], t[c_col_ind[i]], et[c_row_ind[i]][c_col_ind[i]]))
        f.write(str(f1) + '\n')
        f.write('ass1' + str(pre_ass1_fifo) + '\n')
        f.close()
        return pre_ass1_fifo, f1, delays


    def ass2(self, t, wl, et):
        # 获取基于最小权匹配的workload部署方案
        pre_ass2 = {}
        f2 = zeros(wl.shape)
        backup = zeros(et.shape)
        delays = []
        f = open(self.default_pos+'ass2.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        wl_row_ind, wl_col_ind = linear_sum_assignment (wl)
        wl_min_sum = wl[wl_row_ind, wl_col_ind].sum()
        f.write('f2' + '\t' + str(wl_min_sum) + '\n')
        for i in range(min(wl.shape)):
            f2[wl_row_ind[i]][wl_col_ind[i]] = wl[wl_row_ind[i]][wl_col_ind[i]]
            backup[wl_row_ind[i]][wl_col_ind[i]] = et[wl_row_ind[i]][wl_col_ind[i]]
            pre_ass2[V[wl_row_ind[i]]] = {t[wl_col_ind[i]]: et[wl_row_ind[i]][wl_col_ind[i]]}
            delays.append((V[wl_row_ind[i]], t[wl_col_ind[i]], et[wl_row_ind[i]][wl_col_ind[i]]))
        f.write(str(f2) + '\n')
        f.write(str(backup) + '\n')
        f.write('ass2' + str(pre_ass2) + '\n')
        f.close()
        return pre_ass2, f2, delays


    def ass2_fifo(self, t, wl, et):
        # 基于fifo的workload部署方案
        pre_ass2_fifo = {}
        f2 = zeros(wl.shape)
        backup = zeros(et.shape)
        delays = []
        f = open(self.default_pos+'ass2.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        wl_row_ind, wl_col_ind = [i for i in range(wl.shape[0])], [j for j in range(wl.shape[1])]
        random.shuffle(wl_row_ind)
        random.shuffle(wl_col_ind)
        # f.write('f2' + '\t' + str(wl_min_sum) + '\n')
        for i in range(min(wl.shape)):
            f2[wl_row_ind[i]][wl_col_ind[i]] = wl[wl_row_ind[i]][wl_col_ind[i]]
            backup[wl_row_ind[i]][wl_col_ind[i]] = et[wl_row_ind[i]][wl_col_ind[i]]
            pre_ass2_fifo[V[wl_row_ind[i]]] = {t[wl_col_ind[i]]: et[wl_row_ind[i]][wl_col_ind[i]]}
            delays.append((V[wl_row_ind[i]], t[wl_col_ind[i]], et[wl_row_ind[i]][wl_col_ind[i]]))
        f.write(str(f2) + '\n')
        f.write(str(backup) + '\n')
        f.write('ass2' + str(pre_ass2_fifo) + '\n')
        f.close()
        return pre_ass2_fifo, f2, delays


    def ass3(self, t, et, pt):
        """
        生成部署方案3--最小化用户成本
        :param t: 任务
        :param et: 执行时间矩阵
        :param pt: 价格矩阵
        :return: 预部署方案3
        """
        pre_ass3 = {}
        f3 = zeros(et.shape)
        backup = zeros(et.shape)
        delays = []
        f = open(self.default_pos+'ass3.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        # r_row_ind, r_col_ind = km.km_max(pt)
        r_row_ind, r_col_ind = linear_sum_assignment(pt)
        r_max_sum = pt[r_row_ind, r_col_ind].sum()
        f.write('f3' + '\t' + str(r_max_sum) + '\n')
        for i in range(min(et.shape)):
            f3[r_row_ind[i]][r_col_ind[i]] = pt[r_row_ind[i]][r_col_ind[i]]
            pre_ass3[V[r_row_ind[i]]] = {t[r_col_ind[i]]: round(et[r_row_ind[i]][r_col_ind[i]], 4)}
            backup[r_row_ind[i]][r_col_ind[i]] = et[r_row_ind[i]][r_col_ind[i]]
            delays.append((V[r_row_ind[i]], t[r_col_ind[i]], et[r_row_ind[i]][r_col_ind[i]]))
        f.write(str(f3) + '\n')
        f.write(str(backup) + '\n')
        f.write('ass3' + str(pre_ass3) + '\n')
        f.close()
        return pre_ass3, f3, delays


    def ass3_fifo(self, t, et, pt):
        """
        生成部署方案3--fifo用户成本匹配
        :param t: 任务
        :param et: 执行时间矩阵
        :param pt: 价格矩阵
        :return: 预部署方案3
        """
        pre_ass3_fifo = {}
        f3 = zeros(et.shape)
        backup = zeros(et.shape)
        delays = []
        f = open(self.default_pos+'ass3.in', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
        r_row_ind, r_col_ind = [i for i in range(pt.shape[0])], [j for j in range(pt.shape[1])]
        random.shuffle(r_row_ind)
        random.shuffle(r_col_ind)
        for i in range(min(et.shape)):
            f3[r_row_ind[i]][r_col_ind[i]] = pt[r_row_ind[i]][r_col_ind[i]]
            pre_ass3_fifo[V[r_row_ind[i]]] = {t[r_col_ind[i]]: round(et[r_row_ind[i]][r_col_ind[i]], 4)}
            backup[r_row_ind[i]][r_col_ind[i]] = et[r_row_ind[i]][r_col_ind[i]]
            delays.append((V[r_row_ind[i]], t[r_col_ind[i]], et[r_row_ind[i]][r_col_ind[i]]))
        f.write(str(f3) + '\n')
        f.write(str(backup) + '\n')
        f.write('ass3' + str(pre_ass3_fifo) + '\n')
        f.close()
        return pre_ass3_fifo, f3, delays