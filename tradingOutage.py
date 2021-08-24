input1 = ["12:31:04.04", "12:31:05.01", "12:31:06.21", "12:31:14.39", "12:31:15.13", "12:31:16.98", "12:31:17.09"]
input2 = ["00:00:01.00", "00:00:02.08", "00:00:02.93", "00:00:12.43"]

def outage_interval(trade_data):
    def formatTimeString(timestamp):
        return timestamp.replace(".", ":").split(':')
    trade_data.sort(key=lambda x:int(x[6:8]))
    prevTime = trade_data[0]
    prev = formatTimeString(prevTime)
    # may not be sorted 
    output = []
    for i, time in enumerate(trade_data):
        current = formatTimeString(time)
        currSecond, prevSecond = int(current[2]), int(prev[2])
        if (currSecond != prevSecond) and ((prevSecond + 1) != currSecond):
            newString = str(prevTime) + "-" + str(time)
            output.append(newString)
        prevTime = trade_data[i]
        prev = formatTimeString(prevTime)
    return output

# print(outage_interval(input2))

