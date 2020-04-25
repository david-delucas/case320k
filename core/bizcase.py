import pandas as pd

def calc_depreciation_schedule():
    return None


def cost_of_capital():

    return None

def npv():
    return None

def capex():
    return None

def allocate_costs():
    return None

def import_sheet():
    return None

def import_csv():
    return None

def get_assumptions(type="global"):
    return None


def FixedRateDepreciationTable(salvage, cost, life):
    rate = 1 - ((salvage / cost) ** (1 / life))

    for year in range(1, life + 1):
        dv = cost * rate
        cost -= dv
        yield year, round(dv, 2), cost


if __name__ == '__main__':
    print("Year\tDepreciation\tBook Value at the year-end")
    for year, depreciation, new_value in FixedRateDepreciationTable(1000, 100000, 10):
        print("{0:4}\t{1:>18}\t{2:26}".format(year, depreciation, new_value))