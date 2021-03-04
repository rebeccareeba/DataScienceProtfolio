
def c2p(val):
    if val is not None:
        percent = "{:.0%}".format(val)
    else:
        percent = val

    return percent

def c2d(amount):
    if amount is not None:
        dollars = "${:,.2f}".format(amount)
    else:
        dollars = amount

    return dollars

def forAllManufacturers(m):
    converted = []
    for r in m:
        converted.append([r[0], r[1], r[2], c2d(r[3]), c2d(r[4]), c2d(r[5])])

    return converted

def forSingleManufacturer(m, p):
    convertedM = [[m[0][0], m[0][1], c2p(m[0][2]), m[0][3], c2d(m[0][4]), c2d(m[0][5]), c2d(m[0][6])]]
    convertedP = []
    for r in p:
        convertedP.append([r[0], r[1], r[2], c2d(r[3])])

    return convertedM, convertedP

def forCategory(val):
    converted = []
    for r in val:
        converted.append([r[0], r[1], r[2], c2d(r[3])])

    return converted

def forActualVSPredicted(val):
    converted = []
    for r in val:
        converted.append([r[0], r[1], c2d(r[2]), r[3], r[4], r[5], c2d(r[6]), c2d(r[7]), c2d(r[8])])

    return converted

def forStoreRevenueByYearByState(val):
    converted = []
    for r in val:
        converted.append([r[0], r[1], r[2], r[3], r[4], c2d(r[5])])

    return converted

def forRevenueByPopulation(val):
    converted = []
    for r in val:
        converted.append([r[0], c2d(r[1]), c2d(r[2]), c2d(r[3]), c2d(r[4])])

    return converted