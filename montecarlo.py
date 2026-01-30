import random

# basic avg finder
def avgPrice(arr):
    total = 0
    for x in arr:
        total += x
    return total / len(arr)


# trading sim
def monteCarlo1(length):
    results = []

    for a in range(length):
        nw = 9900
        share = 100
        stockCount = 1

        buyCount = 0
        sellCount = 0

        his100 = []
        his10 = []

        for b in range(365):
            change = random.uniform(-0.02, 0.02)
            share += share * change

            # price history
            his100.append(share)
            his10.append(share)

            if len(his100) > 100:
                his100.pop(0)
            if len(his10) > 10:
                his10.pop(0)

            rap100 = avgPrice(his100)
            rap10 = avgPrice(his10)

            ratio = rap10 / rap100

            # filtering out normal noise
            if ratio < 0.995:
                sellCount += 1
                buyCount = 0
            elif ratio > 1.005:
                buyCount += 1
                sellCount = 0
            else:
                buyCount = 0
                sellCount = 0

            # rules
            if buyCount == 7 and nw >= share:
                stockCount += 1
                nw -= share
                buyCount = 0

            if sellCount == 7 and stockCount > 0:
                stockCount -= 1
                nw += share
                sellCount = 0

        nw = stockCount * share + nw
        results.append(nw)

    return results


# hold sim
def monteCarlo2(length):
    results = []

    for a in range(length):
        nw = 9900
        share = 100
        stockCount = 1

        for b in range(365):
            change = random.uniform(-0.02, 0.02)
            share += share * change

        nw = stockCount * share + nw
        results.append(nw)

    return results


# analysing both methods
def statsAnalysis(length):
    mc1 = monteCarlo1(length)
    mc2 = monteCarlo2(length)

    diffs = []
    for i in range(len(mc1)):
        diffs.append(mc1[i] - mc2[i])

    avgDiff = avgPrice(diffs)
    maxDiff = max(diffs)
    minDiff = min(diffs)
    wins = 0
    for d in diffs:
        if d>0:
            wins+=1

    print(f"Average difference: {avgDiff}")
    print(f"Max difference: {maxDiff}")
    print(f"Min difference: {minDiff}")
    print(f"Strategy beat baseline {wins} out of {length} times")


# func call
statsAnalysis(500)

    

    
    