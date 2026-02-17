import random
import matplotlib.pyplot as plt

# basic avg finder
def avgPrice(arr):
    total = 0
    for x in arr:
        total += x
    return total / len(arr)


#year prices generator to allow even comparison between mc1 and mc2
def priceGen():
    prices = []
    share = 100
    pmod = 0.5
    
    #to add drift
    for i in range(365):
        a = random.random()
        
        if a>pmod:
            change = random.uniform(0, 0.02)
            share+=share*change
            pmod-=0.003
        else:
            change = random.uniform(-0.02, 0)
            share+=share*change
            pmod+=0.003
        prices.append(share)
    
    return prices
        


# trading sim
def monteCarlo1(priceList, fee):
    
    nwtrend = []

    prices = priceList
    
    cash = 0
    stockCount = 10000/prices[0]

    buyCount = 0
    sellCount = 0

    his100 = []
    his10 = []

    for i in range(len(prices)):
        share = prices[i]
        
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
            cash -= share*(1+fee)
            buyCount = 0

        if sellCount == 7 and stockCount > 0:
            stockCount -= 1
            cash += share*(1-fee)
            sellCount = 0

        nw = stockCount * share + cash
        nwtrend.append(nw)
            
    cash += stockCount * prices[-1]

    return cash, nwtrend


# hold sim
def monteCarlo2(priceList):
    results = []
    nwtrend = []

    prices = priceList
    nw = 0
    stockCount = 10000/prices[0]
        

    for i in range(len(prices)):
        share = prices[i]
        nw1 = stockCount * share + nw
        nwtrend.append(nw1)

    nw =  stockCount * prices[-1]
    return nw,nwtrend



# analysing both methods
def statsAnalysis(length):
    diffs = []
    plt.figure()
    plt.title("Holding - no trading")
    for i in range(length):
        p = priceGen()
        mc2,mc2list = monteCarlo2(p)
        plt.plot(mc2list)
    plt.figure()
    plt.title("Your trading method")
    for j in range(length):
        p = priceGen()
        mc1,mc1list = monteCarlo1(p)
        mc2,mc2list = monteCarlo2(p)
        plt.plot(mc1list)   

        
        diffs.append(mc1-mc2)
        
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
    print(f"Strategy beat baseline {wins} out of {length} times - winrate = {wins/length}")
    plt.figure()
    plt.plot(diffs)
    plt.title("Difference: MC1 minus MC2")
    plt.xlabel("Simulation Index")
    plt.ylabel("£ Difference")
    plt.show()
  
#analysing effect trading fees have on meth   
def statsAnalysis2(length,feeList):

    avgdiffs = []
    
    plt.figure()
    for fee in feeList:
        diffs = []
        for i in range(length):
            p = priceGen()
            mc1,mc1list = monteCarlo1(p, fee)
            mc2,mc2list = monteCarlo2(p)
            diffs.append(mc1-mc2)
        
        avgDiff = avgPrice(diffs)
        maxDiff = max(diffs)
        minDiff = min(diffs)

        avgdiffs.append(avgDiff)
    
    plt.plot(feeList, avgdiffs)
    plt.title("Avg diffs vs trading fees")
    plt.xlabel("Fee")
    plt.ylabel("avg diffs")
    plt.show()


#generates lots of fees
feeList = []
fee = 0
for i in range(1, 11):
    step = i/100
    fee+=step
    feeList.append(fee)


# func call
statsAnalysis2(1000, feeList)

    

    
    
