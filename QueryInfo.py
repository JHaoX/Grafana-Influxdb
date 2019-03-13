class QueryInfo:
    def __init__(self, query:str):
##  query:  SELECT mean("degrees")
##          FROM "h2o_temperature"
##          WHERE time >= 1546372062774ms and time <= 1547689662774ms
##          GROUP BY time(1h) fill(null)
        self.qs = query
        self.qlist = query.lower().split()
        self.time_range = [0,0]
        self.se = []
        self.wh = []
        self.fr = []
        self.gb = []
        self.other_info = []
        self._parse()

    def _parse(self):
        print(self.qlist)
        i = 0
        qlist_len = len(self.qlist)
        if self.qlist[i] == "select":
            i+=1
            while(self.qlist[i] != "from"):
                self.se.append(self.qlist[i])
                i+=1
        if self.qlist[i] == "from":
            i+=1
            while(self.qlist[i] != "where"):
                self.fr.append(self.qlist[i])
                i+=1
        print(i)
        if self.qlist[i] == "where":
            i+=1
            print(self.qlist[i])
            while(i < qlist_len and self.qlist[i] != "group"):
                self.wh.append(self.qlist[i])
                i+=1
        if i < qlist_len and self.qlist[i] == "group":
            i += 2 # group by
            while(i < qlist_len):
                self.gb.append(self.qlist[i])
                i+=1
        

    def get_time_range(self):
        i = self.qlist.index('>=')
        time_str = self.qlist[i+1]
        self.time_range[0] = int(time_str[:len(time_str)-2])
        i = self.qlist.index('<=')
        time_str = self.qlist[i+1]
        self.time_range[1] = int(time_str[:len(time_str)-2])

        return self.time_range

    def add_group_by(self, time:int):
        self._take_mean()
        self.qs+= " GROUP BY time(" + str(time) + "ms)"
        return self.qs

    def _take_mean(self):
        if "mean" in self.qlist[1]:
            return
        else:
            self.qlist[1] = "mean(" + self.qlist[1] + ")"
            self.qs = " ".join(self.qlist)
        

            

if __name__ == '__main__':
    print("____test____")
    qs = 'SELECT mean("degrees") FROM "h2o_temperature" WHERE time >= 1546372062774ms and time <= 1547689662774ms GROUP BY time(1h) fill(null)'
    test = QueryInfo(qs)
    test.add_group_by(1000)
    tr = test.get_time_range()
    print(test.qs)
    print(tr)
    print(test.se)
    print(test.fr)
    print(test.wh)
    print(test.gb)
    
