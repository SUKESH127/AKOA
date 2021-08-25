class TradeReconciliation:
    def __init__(self):
        self.akunaDict = {} # {A: [[10, 11:59:00], [10, 11:59:00]], B: [-15, 12:05:00]}
        self.exchangeDict = {} # {A: [[10, 11:59:00], [10, 11:59:00]], B: [-15, 12:05:00]}
    
    def dictInsert(self, dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = [value]
        else:
            dictionary[key].append(value)
    
    def process(self, line):
        currentLine = line.split(',')
        source, product, data = currentLine[0], currentLine[1], currentLine[2:]
        if source == "AKUNA":
            self.dictInsert(self.akunaDict, product, data)
        else:
            self.dictInsert(self.exchangeDict, product, data)
                
    def processAll(self, data):
        for line in data:
            self.process(line)
    
    def timeInBounds(self, t1, t2): 
        time1, time2 = t1.split(':'), t2.split(':')
        time1Seconds = int(time1[0]) * 3600 + int(time1[1]) * 60 + int(time1[2]) # Xhrs * (3600secs/hr) + Ymin * (60secs/min) + Zsecs
        time2Seconds = int(time2[0]) * 3600 + int(time2[1]) * 60 + int(time2[2])
        return (abs(time2Seconds - time1Seconds) <= 300) # 300 = 5 min * 60 secs/min

    def reconciliation(self):
        akKeys, exKeys = list(self.akunaDict.keys()), list(self.exchangeDict.keys())
        if akKeys != exKeys:
            return False
        for i in range(len(akKeys)):
            akunaList, exchangeList = self.akunaDict.get(akKeys[i]), self.exchangeDict.get(exKeys[i])
            if len(akunaList) != len(exchangeList):
                return False
            for i in range(len(akunaList)):
                if akunaList[i][0] != exchangeList[i][0] or not self.timeInBounds(akunaList[i][1], exchangeList[i][1]):
                    return False
        return True

input1 = [ # True 
    "AKUNA,A,10,11:59:00",
    "AKUNA,B,-15,12:05:00",
    "EXCHANGE,A,10,12:01:00",
    "EXCHANGE,B,-15,12:09:00"
]

input2 = [ # True 
    "AKUNA,A,10,11:01:00",
    "AKUNA,A,10,11:02:00",
    "AKUNA,A,10,11:03:00",
    "EXCHANGE,A,10,11:04:00",
    "EXCHANGE,A,10,11:02:00",
    "EXCHANGE,A,10,11:03:00"
]

input3 = [ # FALSE
    "EXCHANGE,A,10,11:59:00",
    "AKUNA,A,10,11:59:00",
    "EXCHANGE,A,10,12:00:00",
    "EXCHANGE,B,12,15:01:03",
    "EXCHANGE,H,-50,16:14:02",
    "AKUNA,A,10,11:53:00",
    "AKUNA,A,10,12:00:00",
    "EXCHANGE,A,10,12:01:00",
    "AKUNA,B,12,15:01:02",
    "AKUNA,H,-50,16:19:02"
]


TF = TradeReconciliation()
TF.processAll(input3)
print(TF.reconciliation())
