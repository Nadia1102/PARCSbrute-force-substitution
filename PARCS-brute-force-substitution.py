from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        text = self.read_input()
        n = len(text)
        step = n / len(self.workers)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(int(i * step), int(i * step + step), text[int(i * step):int(i * step + step):]))

        # reduce
        reduced = self.myreduce(mapped)

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b, text):
        goal = 'login'
        count = a + 1
        for entry in text:
            password = entry.strip()
            if password == goal:
                return password
            else:
                count += 1
                if count > b:
                    return 'Fail'

    @staticmethod
    @expose
    def myreduce(mapped):
        output = ''
        for x in mapped:
            if x == 'Fail':
                continue
            else:
                output = x.value.strip()
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readlines()
        f.close()
        return line

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()