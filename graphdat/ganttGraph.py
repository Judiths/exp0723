from graphTable.gantt_data import Gantt
from workflows.multiwl import V


# pos = 'D:\\PycharmProjects\\arima_MDGT\\graphdat\\C_30\\mdgt\\'
pos = 'D:\\PycharmProjects\\arima_MDGT\\graphdat\\C_30\\baseline\\'
csv_file = pos+'res.csv'

g = Gantt()
pid_nums = g.strTypeAttri(csv_file, 'pid_num')
vms = g.strTypeAttri(csv_file, 'vm')
vm_num = g.vm(pid_nums)
task_ids = g.strTypeAttri(csv_file, 'task_id')
task_owners = g.strTypeAttri(csv_file, 'task_owner')
task_types = g.strTypeAttri(csv_file, 'task_type')
color_num = g.color_num(task_owners)
setups = g.numTypeAttri(csv_file, 'setup')
durations = g.numTypeAttri(csv_file, 'duration')
cuttings = g.numTypeAttri(csv_file, 'cutting')
task_xiabiao = g.task_xiabiao(task_ids)

setup_min = min(setups)
max_num = max(vm_num) + 1
setup = [round(setups[i] - setup_min, 3) for i in range(len(setups))]
cutting = [round(cuttings[j] - setup_min, 3) for j in range(len(cuttings))]
setup_max = max(cutting)

# 虚拟机上的任务个数
wl = g.get_wl(vm_num)
# 统计整个云环境的workload
total_wl = round(sum(wl)/len(wl), 3)

pre_ass1 = g.get_ass(pos+'ass1.in', 'ass1')
pre_ass2 = g.get_ass(pos+'ass2.in', 'ass2')
pre_ass3 = g.get_ass(pos+'ass3.in', 'ass3')
# print(ass1)

# 计算组内的workload的公平性
csp1, csp2, csp3 = g.get_etc_vm(pre_ass1 + pre_ass2 + pre_ass3, V)
f1 = g.fairness(csp1)
f2 = g.fairness(csp2)
f3 = g.fairness(csp3)

ff = g.fairness(csp1+csp2+csp3)
print(f1, f2, f3, ff)

# 计算成本
costlist = g.costList(pre_ass1 + pre_ass2 + pre_ass3)
# 统计每台vm上的盈利，从而计算云厂商租出vm的收入
cost_of_each_vm = g.cost(costlist, V)
# 统计整个云环境的profit
total_prf = round(sum(cost_of_each_vm)/len(cost_of_each_vm), 3)
print(cost_of_each_vm, total_prf)
print('makespan %.3f' % setup_max)

gantt_file_out = pos + 'gantt_input1.dat'
fa = open(gantt_file_out, 'w')
fa.write(str(max_num) + '\n')
fa.write(str(len(setup)) + '\n')
fa.write(str(setup_max) + '\n')
fa.write(str(vm_num) + '\n')
fa.write(str(color_num) + '\n')
fa.write(str(setup) + '\n')
fa.write(str(durations) + '\n')
fa.write(str(task_xiabiao) + '\n')
fa.write(str(wl) + '\n')
fa.write(str(cost_of_each_vm) + '\n')
fa.close()