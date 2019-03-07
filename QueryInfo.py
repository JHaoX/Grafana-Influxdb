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

    def _parse(self):
##        i = 0
##        qlist_len = len(qlist)
##        if qlist[i] == "select":
##            i++
##            while(qlist[i] != "from"):
##                self.se.append(qlist[i])
##                i++
##        if qlist[i] == "from":
##            i++
##            while(qlist[i] != "where"):
##                self.fr.append(qlist[i])
##                i++
##        if qlist[i] == "where":
##            i++
##            while(qlist[i] != "GROUP" and i < qlist_len):
##                self.wh.applend(qlist[i])
##                i++
##        if qlist[i] == "GROUP":
##            i += 2 # group by
##            while
##            self.gb.append(qlist[i])
        

        
        if 'select' in self.query:
            select_exist = True
            select_index = self.query.index('select')

        if 'from' in self.query:
            select_exist = True
            from_index = self.query.index('from')

        if 'where' in self.query:
            select_exist = True
            where_index = self.query.index('where')

        if 'by' in self.query:
            select_exist = True
            gb_index = self.qeury.index('by')

    def get_time_range(self):
        i = self.qlist.index('>=')
        time_str = self.qlist[i+1]
        self.time_range[0] = int(time_str[:len(time_str)-2])
        i = self.qlist.index('<=')
        time_str = self.qlist[i+1]
        self.time_range[1] = int(time_str[:len(time_str)-2])

        return self.time_range

    def add_group_by(self, time:int):
        self.qs+= " GROUP BY time(" + str(time) + "ms)"
        return self.qs

            

if __name__ == '__main__':
    print("____test____")
    qs = 'SELECT mean("degrees") FROM "h2o_temperature" WHERE time >= 1546372062774ms and time <= 1547689662774ms GROUP BY time(1h) fill(null)'
    test = QueryInfo(qs)
    test.add_group_by(1000)
    tr = test.get_time_range()
    print(test.qs)
    print(tr)
