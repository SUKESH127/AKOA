class TradeReconciliation:
    def __init__(self):
        self.recordList = []
    def process(self, line):
        currentLine = line.split(',')
        # process trade record
        if currentLine[0] != 'RECONCILIATION':
            self.recordList.append(currentLine)
            return currentLine[2]
        # handle reconciliation request
        forwardUnmatches, backwardUnmatches = [], []
        for record in self.recordList:
            if record[0] == currentLine[1]:
                forwardUnmatches.append(record)
            else:
                backwardUnmatches.append(record)
        if (len(backwardUnmatches) > 0 and len(forwardUnmatches) == 0) or (len(backwardUnmatches) == 0 and len(forwardUnmatches) > 0):
            return len(forwardUnmatches)
        # go through unmatch and check if forward and backward match candidates align to catch matches
        matches = 0
        for forwardMatch in forwardUnmatches:
            for backwardMatch in backwardUnmatches:
                if forwardMatch[1:] == backwardMatch[1:]:
                    matches += 1
        realMatches = len(forwardUnmatches) - matches # remove artifical unMatches
        return realMatches

input1 = [
    "AKUNA,A,10,12:01:00",
    "AKUNA,B,-15,12:05:00",
    "RECONCILIATION,AKUNA,EXCHANGE1",
    "RECONCILIATION,EXCHANGE1,AKUNA",
    "EXCHANGE1,B,-15,12:05:00",
    "EXCHANGE1,B,-20,12:07:00",
    "RECONCILIATION,AKUNA,EXCHANGE1",
    "RECONCILIATION,EXCHANGE1,AKUNA",
    "RECONCILIATION,EXCHANGE2,AKUNA",
]

TF = TradeReconciliation()
for i in input1:
    print(TF.process(i))