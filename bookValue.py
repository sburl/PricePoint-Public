import pandas as pd

#value book given lowest list price and Amazon offer of giftcard
def bookValue(listed, redeem, salesRank):

    depreciation = 0.00

    #sales rank is proxy for how long book will take to sell
    if salesRank > 100000:
        depreciation += 0.35
    elif salesRank > 50000:
        depreciation += 0.30
    elif salesRank > 25000:
        depreciation += 0.25
    elif salesRank > 10000:
        depreciation += 0.20
    elif salesRank > 5000:
        depreciation += 0.15
    elif salesRank > 2500:
        depreciation += 0.10
    elif salesRank > 1000:
        depreciation += 0.05

    #higher priced items are more susceptible to price swings
    if listed > 100:
        depreciation += 0.10
    elif listed > 50:
        depreciation += 0.05

    #fixed costs and margin
    shippingAndBox = 6
    profit = 10

    #account for amazon fees
    gross = 0.7 * listed

    net = gross - shippingAndBox

    #offer is highest of value of amazon gift card / expected after margin
    if redeem > net:
        offer = 0.7 * redeem
    else:
        offer = (net * (1 - depreciation)) - profit

    estimatedProfit = listed - offer

    if offer < 5:
        return (0,0)
    else:
        return (offer, estimatedProfit)

#take csv of price data and generate upper bound of price to pay
def bulkEstimate():

    #set data/export file
    path = "YOUR PATH HERE"
    export = "YOUR PATH HERE"

    df = pd.read_csv(path)

    newData = []

    #iterate over items in sheet, determine offer, record in new dataframe
    index = 0
    for entries in range(len(df)):

        isbn = str(df["ISBN13"][index])
        isbn = isbn[0:3] + isbn[4:]

        listed = df["Retail"][index]
        redeem = df["Trade In"][index]
        salesRank = df["Rank"][index]

        index += 1

        (offer, estimatedProfit) = bookValue(listed, redeem, salesRank)

        newData.append((isbn, offer, estimatedProfit))

    newdf = pd.DataFrame(newData)
    newdf.columns = ["ISBN13", "Offer", "Estimated Profit"]

    newdf.to_csv(export, encoding='utf-8', index = False)

bulkEstimate()
