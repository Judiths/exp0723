from xml.etree.ElementTree import ElementTree
from workflows.DAG import Graph


class SingleWorkflow:
    # '分解单个的scientific workflow；构造新的job类型'
    job_tag = '{http://pegasus.isi.edu/schema/DAX}job'
    child_tag = '{http://pegasus.isi.edu/schema/DAX}child'
    parent_tag = '{http://pegasus.isi.edu/schema/DAX}parent'
    types_new = ['8M', '16M', '32M']


    def __init__(self, xml_file):
        self.xml_file = xml_file

    def jobs_old(self):
        # '解析DAG节点'
        tree = ElementTree(file=self.xml_file)
        root = tree.getroot()
        jobs = []
        for elem in root.iter(tag=self.job_tag):
            jobs.append(elem.attrib)
        return jobs

    def types_old(self):
        types = []
        res = []
        for job in self.jobs_old():
            types.append(job['name'])
        for i, type in enumerate({}.fromkeys (types).keys()):
            res.append(type)
        return res


    def types_trans(self):
        indexes = []
        types_inter = []
        for p in range(len(self.types_old())):
            tmp = p % len(self.types_new)
            q = {self.types_old()[p]: self.types_new[tmp]}
            indexes.append(tmp)
            types_inter.append(q)
        return types_inter


    def jobs_new(self):
        jobs_new = []
        for item in self.jobs_old():
            for j in self.types_trans():
                if item['name']==list(j.keys())[0]:
                    item['name'] = j[item['name']]
                    jobs_new.append(item)
        return jobs_new


    def dependencies(self):
        # '解析DAG拓扑结构'
        tree = ElementTree (file=self.xml_file)
        deps = []
        # namespace = self.xml_file.strip('.xml')
        for child in tree.iter(tag=self.child_tag):
            child_id = child.get('ref')
            parents = []
            for parent in child.findall(self.parent_tag):
                parents.append(parent.get('ref'))
            dependency = {'child': child_id, 'parents': parents}
            deps.append(dependency)
        return deps


    def order(self):
        dag = Graph()
        nodes = []
        for i in self.jobs_new():
            nodes.append(i['id'])
        dag.add_nodes(nodes)
        for item in self.dependencies():
            for i in item['parents']:
                dag.add_edge((i, item['child']))
        order = dag.breadth_first_search('ID00000')
        return order


    def findbyID(self, id):
        for job in self.jobs_new():
            if job['id']==id:
                task ={'id': job['id'], 'namespace': job['namespace'], 'name': job['name']}
                # task =(job['id'],job['namespace'],job['name'])
                # print(task)
                return task


    def tasks(self):
        tasks = []
        for i in self.order():
            tasks.append(self.findbyID(i))
        # print('tasks 完毕！')
        return tasks