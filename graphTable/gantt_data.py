import csv
import re
from workflows.multiwl import color, PRICE, type_dict

class Gantt:

    def __init__(self):
        super(Gantt, self).__init__()


    def strTypeAttri(self, csv_file, key_str):
        """
        返回进程号列表
        :param csv_file: 输出文件
        :return: 进程号（相当于虚拟机标识）
        """
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            attr = [row[key_str] for row in reader]
        return attr


    def vm(self, pid_num):
        """
        返回虚拟机标识列表
        :param pid_num: 进程号列表
        :return: 虚拟机标识列表
        """
        vm_num = []
        d = {'x': -1}
        counter = 0
        for i in range(len(pid_num)):
            if not pid_num[i] in d.keys():
                d.update({pid_num[i]: counter})
                tmp = counter
                counter += 1
            else:
                tmp = d[pid_num[i]]
            vm_num.append(tmp)
        return vm_num


    def task_xiabiao(self, task):
        """
        返回任务下标列表
        :param task: 任务列表
        :return: 任务下标列表
        """
        task_num = []
        for i in task:
            i = ''.join(i.split('ID'))
            task_num.append(int(i))
        return task_num


    def vm_xiabiao(self, vm):
        """
        返回虚拟机下标列表
        :param vm: 虚拟机列表
        :return: 虚拟机下标列表
        """
        vm_id = []
        for i in vm:
            i = ''.join(i.split('v'))
            vm_id.append(int(i))
        return vm_id


    def color_num(self, task_owners):
        """
        创建颜色列表（同一工作流中的任务用一种颜色）
        :return: 颜色列表
        """
        color_num = []
        for i in task_owners:
            # print(i, color[i])
            color_num.append(color[i])
        return color_num


    def numTypeAttri(self, csv_file, key_str):
        """
        创建任务起始时间戳列表
        :param csv_file:
        :return: 任务起始时间戳列表
        """
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            numType_attri = [round(float(row[key_str]), 3) for row in reader]
        return numType_attri


    def get_wl(self, vm_num):
        wl = []
        for i in set(vm_num):
            wl.append(vm_num.count(i))
        return wl



    def get_ass(self, ass1_file, key_str):
        res1 = []
        fa = open(ass1_file, 'r')
        for line in fa.readlines():
            rect = '^'+key_str+'.*'
            res = re.match(rect, line)
            if not res == None:
                res1.append(res.group().replace(key_str, ''))
        return res1


    def get_etc_vm(self, pre_ass, V):
        # 获得vm的执行时间
        csp1 = []
        csp2 = []
        csp3 = []
        for z in V[0:1]:
            for x in pre_ass:
                y = eval(x)
                for i, j in y.items():
                    for k, l in j.items():
                        if i == z:
                            vm_etc = (i, l)
                            # print(vm_etc)
                            csp1.append(vm_etc)
        for z in V[1:2]:
            for x in pre_ass:
                y = eval(x)
                for i, j in y.items():
                    for k, l in j.items():
                        if i == z:
                            vm_etc = (i, l)
                            # print (vm_etc)
                            csp2.append(vm_etc)
        for z in V[2:len(V)]:
            for x in pre_ass:
                y = eval(x)
                for i, j in y.items():
                    for k, l in j.items():
                        if i == z:
                            vm_etc = (i, l)
                            # print (vm_etc)
                            csp3.append(vm_etc)
        return csp1, csp2, csp3


    def fairness(self, csp):
        etc = []
        pfetc = []
        for x in csp:
            etc.append(x[1])
            pfetc.append(x[1]*x[1])
        fairness = round(
            sum(etc)*sum(etc)/(len(etc)*sum(pfetc)), 6)
        return fairness


    def costList(self, pre_ass):
        costlist = []
        for x in pre_ass:
            y = eval(x)
            for i,j in y.items():
                for k,l in j.items():
                    x = i+str(type_dict[k[1][2]]+1)
                    vm_profit = (i, PRICE[x] * l)
                    print(vm_profit)
                    costlist.append(vm_profit)
        return costlist


    def cost(self, costList, vm):
        vm_pro = []
        for v in vm:
            vm_set = []
            for i, j in costList:
                if i==v:
                    vm_set.append(j)
            vm_pro.append(round(sum(vm_set), 3))
        return vm_pro