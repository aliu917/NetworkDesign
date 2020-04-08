class DisjointSet:

    def __init__(self, n):
        self.elements = n * [n+1]       #Intialize all parent pointers to out of range
        self.n = n


    def makeSet(self, n):
        self.elements[n] = -1


    def find(self, x):
        if self.elements[x] > self.n:
            return
        if self.elements[x] < 0:
            return x
        self.elements[x] = self.find(self.elements[x])
        return self.elements[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y: return
        if self.elements[x] < self.elements[y]:
            temp = x
            x = y
            y = temp
        if self.elements[x] == self.elements[y]:
            self.elements[y] -= 1
        self.elements[x] = y


    #TODO: This is potentially very time consuming
    def get_all_sets(self):
        all_sets = {}
        for i in range(len(self.elements)):
            group = self.find(i)
            if not group:
                continue
            if group in all_sets:
                all_sets[group].add(i)
            else:
                s = set()
                s.add(i)
                all_sets[group] = s
        return all_sets


dj_set = DisjointSet(10)
for i in range(8):
    dj_set.makeSet(i)
dj_set.union(1, 4)
dj_set.union(1, 5)
dj_set.union(2, 3)
dj_set.union(5, 3)

for i in range(10):
    print("Finding ", i, ": ", dj_set.find(i))

print("all sets")
print(dj_set.get_all_sets())
