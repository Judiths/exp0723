# coding=utf-8
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from prehandle.options import OptsClass
from workflows.multiwl import V, C_30


class MDGTFIFO:

    def __init__(self, tasks_pool, vms, pos):
        self.tasks_pool = tasks_pool    # 任务池
        self.vms = vms                  # 虚拟机列表
        self.pos = pos                  # 文件位置

    def pre_optimal_ass_fifo(self):
        """
        生成pre_scheduling assignment
        :return: pre_opt_ass
        """
        opts = OptsClass()
        pre_opt_ass = []
        for l in range(1000):
            if not self.tasks_pool.empty():
                tl1 = self.tasks_pool.get()
                # print(self.tasks_pool.empty(), len(tl1), tl1)
                et1 = opts.inputET(tl1, l)
                ass1, f1, delays1 = opts.ass1_fifo(tl1, et1)
                pre_opt_ass += delays1
            else:
                break

            if not self.tasks_pool.empty():
                tl2 = self.tasks_pool.get()
                et2 = opts.inputET(tl2, l)
                wl = opts.wl(tl2, l)
                ass2, f2, delays2 = opts.ass2_fifo(tl2, wl, et2)
                pre_opt_ass += delays2
            else:
                break

            if not self.tasks_pool.empty():
                tl3 = self.tasks_pool.get()
                et3 = opts.inputET(tl3,l)
                pt3 = opts.inputPT(tl3, et3)
                ass3, f3, delays3 = opts.ass3_fifo(tl3, et3, pt3)
                pre_opt_ass += delays3
            else:
                break

        # taskNum = len(pre_opt_ass)
        # gameSta = round(taskNum/3)
        # print('预分配结束', taskNum, gameSta, pre_opt_ass)
        return pre_opt_ass


def task_sleep(it):
    """
    采集任务部署的时间戳等信息
    :param it: 任务部署方案
    :return: 任务的部署信息
    """
    print(it)
    icon = os.getpid()
    timestamp1 = int(round(time.time() * 1000)) / 1000
    time.sleep(it[2])
    timestamp2 = int(round(time.time() * 1000)) / 1000
    setup = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp1))
    cutting = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp2))
    return [True, icon, it[0], it[1][1][0], it[1][1][1], it[1][1][2],
            timestamp1, it[2], timestamp2, setup, cutting]


def use_submit(pre_optimal_ass, pos):
    print('开始部署\n')
    fa = open(pos + 'res.csv', 'w')
    fa.write('pid_num,vm,task_id,task_owner,task_type,setup,duration,cutting\n')
    with ProcessPoolExecutor(max_workers=len(V)) as executor:
        futures = {executor.submit(task_sleep, it): it for it in pre_optimal_ass}
        try:
            for f in as_completed(futures):
                # print('%s result is %s.' % (futures[f], f.result ()))
                fa.write(str(f.result()[1]) + ',' + str(f.result()[2]) + ',' +
                         str(f.result()[3]) + ',' + str(f.result()[4]) + ',' +
                         str(f.result()[5]) + ',' + str(f.result()[6]) + ',' +
                         str(f.result()[7]) + ',' + str(f.result()[8]) + ',' +
                         '\n')
            fa.close()
        except Exception as exc:
            print(exc)


if __name__ == '__main__':
    s = time.time()

    opts = OptsClass()
    Tn = C_30

    task_pool = opts.tasks_pool(Tn, 10000)  # 层级上限是10000
    pos = 'D:\\PycharmProjects\\arima_MDGT\\graphdat\\C_30\\baseline\\'

    mdgt = MDGTFIFO(task_pool, V, pos)

    # 预分配策略
    pre_optimal_ass_fifo = mdgt.pre_optimal_ass_fifo()
    print(pre_optimal_ass_fifo, pos)

    # 本机部署模拟
    use_submit(pre_optimal_ass_fifo, pos)