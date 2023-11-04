import QuantLib as ql
import re
from datetime import date, datetime
import numpy as np
import xlwings as xw

def str2date(x):
    d = datetime.strptime(x, "%m/%d/%Y")
    return d.date()

def to_date(x):
    """
    to_date(x)
    "2020/01/01" => ql.Date(1, 1, 2020)
    "2020-01-01" => ql.Date(1, 1, 2020)
    
    date(2020, 1, 2) => ql.Date(2, 1, 2020)
    """
    if isinstance(x, str):
        sYear, sMonth, sDay = re.split('[/-]', x)
        return ql.Date(int(sDay), int(sMonth), int(sYear))

    elif isinstance(x, date):
        return ql.Date(x.day, x.month, x.year)

    else:
        assert False, "the input is neither date nor string"

def to_period(x):
    """
    to_period(x)
    0.25 => ql.Period(91, ql.Days)
    """
    return ql.Period(int(x*365), ql.Days)
    
def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
"""
south_korea = ql.SouthKorea()
today = to_date(date.today())

eval_date = ql.Settings.instance().evaluationDate

null_curve = ql.ZeroCurve([today, today + ql.Period(1, ql.Days)], [0.0, 0.0], ql.ActualActual(), south_korea)
null_curve.enableExtrapolation()
"""
def get_excel_volatility(file_name):
    """
    get_excel_volatility(file_name)
    """
    app = xw.App(visible=False)
    wb = xw.Book(file_name)
    ws = wb.sheets["sheet1"]
    data = ws.range("A1:M9").value
    maturities, raw_vol = [x[0] for x in data[2:]], [x[2:] for x in data[2:]]
    moneyness = list(map(lambda x: 0.01 * float(x[:-1]), data[0][2:]))

    wb.close()
    app.quit()  

    return np.array(moneyness), np.array(maturities), np.array(raw_vol)
