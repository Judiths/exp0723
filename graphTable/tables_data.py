#coding = utf-8
import csv


class TxtClass:
    # '处理文件的类'
    default_pos = '\\graphdat\\'

    def __init__(self):
        super(TxtClass, self).__init__()


    def txt2csv(self, file_in, file_out):
        """
        将txt文件转换成csv文件
        :param file_in: .dat文件
        :param file_out: .csv文件
        """
        fa = open(file_out, 'w')
        with open(file_in) as f:
            fa.write('source_file,no_task,st_game,make_span,'
                     'workload,cost,f1,f2,f3,F\n')
            for line in f.readlines():
                r = line.replace('\t', ',')
                fa.write(r)
        fa.close()
        print('文件转换完毕')


    def cols(self, csv_file, key_str):
        """
        根据关键词读取.csv文件列数据
        :param csv_file:
        :return:
        """
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            cols = [row[key_str] for row in reader]
        return cols


    def aver_per_set(self, csv_file, key_str, count):
        """
        返回每20组col列的平均值--去掉一个最大值，去掉一个最小值，取剩余数值的平均值
        :param key_str: make_spans, cost, fairness
        :param count: 迭代次数
        :return:
        """
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            cols = [row[key_str] for row in reader]
        aver_list = []
        x = count
        for i in range(count):
            ms = [float(k) for k in cols[x*i:x*(i+1)]]
            ms.remove(max(ms))
            ms.remove(min(ms))
            aver = round(sum(ms)/(x-2), 3)
            aver_list.append(aver)
        return aver_list


    def compose(self, csv_out1, csv_out2, curve_in, set_num):
        """
        创建curve的matlab输入文件,
        :param csv_out1: out.csv(data from our proposed method)
        :param csv_out2: baseline_out.csv(data from the baseline method)
        :param f: curve.txt
        """
        no_task = self.aver_per_set(csv_out1,'no_task', set_num)
        stg = self.aver_per_set(csv_out1, 'st_game', set_num)

        ms_al1 = self.aver_per_set(csv_out1, 'make_span', set_num)
        wl_al1 = self.aver_per_set(csv_out1, 'workload', set_num)
        prf_al1 = self.aver_per_set(csv_out1, 'cost', set_num)
        f11 = self.aver_per_set(csv_out1, 'f1', set_num)
        f12 = self.aver_per_set(csv_out1, 'f2', set_num)
        f13 = self.aver_per_set(csv_out1, 'f3', set_num)
        ff1 = self.aver_per_set(csv_out1, 'F', set_num)

        ms_al2 = self.aver_per_set(csv_out2, 'make_span', set_num)
        wl_al2 = self.aver_per_set(csv_out2, 'workload', set_num)
        prf_al2 = self.aver_per_set(csv_out2, 'cost', set_num)
        f21 = self.aver_per_set(csv_out2, 'f1', set_num)
        f22 = self.aver_per_set(csv_out2, 'f2', set_num)
        f23 = self.aver_per_set(csv_out2, 'f3', set_num)
        ff2 = self.aver_per_set(csv_out2, 'F', set_num)

        f = open(curve_in, 'w')
        f.write('no_task,st_game,make_span1,make_span2,workload1,' +
                'workload2,cost1,cost2,MDGT-csp1-F1,base-csp1-F2,' +
                'MDGT-csp2-F1,base-csp2-F2,MDGT-csp3-F1,base-csp3-F2,' +
                'F1,F2\n')
        for i in range(set_num):
            f.write(str(no_task[i]) + '\t' + str(stg[i]) + '\t' +
                str(ms_al1[i]) + '\t' + str(ms_al2[i]) + '\t' +
                str(wl_al1[i]) + '\t' + str(wl_al2[i]) + '\t' +
                str(prf_al1[i]) + '\t' + str(prf_al2[i]) + '\t' +
                str(f11[i]) + '\t' + str(f21[i]) + '\t' +
                str(f12[i]) + '\t' + str(f22[i]) + '\t' +
                str(f13[i]) + '\t' + str(f23[i]) + '\t' +
                str(ff1[i]) + '\t' + str(ff2[i]) + '\t' +
                '\n')
        f.close()
        print('%d 组对比数据采集完毕' % set_num)
