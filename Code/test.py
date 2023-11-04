import fitting
import ssvi
import phi
from datetime import date, timedelta
import numpy as np
import matplotlib.pyplot as plt
from functools import partial
#import vol_utils
from vol_utils import str2date

calc_date = date(2021, 4, 13)
s = ["06/12/2021", "06/10/2021", "07/08/2021", "08/12/2021", "09/09/2021", "10/14/2021", "12/09/2021", "03/10/2022", "06/09/2022", "12/08/2022", "06/08/2023", "12/13/2023", "06/13/2024"]

#dates = list(map(vol_utils.str_to_date, s))
dates = list(map(str2date, s))

strikes = [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5]
vol=[
     [0.536091427, 0.492408395, 0.442358013, 0.411745009, 0.33155612, 0.298842838, 0.260912045, 0.207692158, 0.18227194, 0.117269395, 0.095865392, 0.100341039, 0.122615191, 0.171786038, 0.175387023, 0.199367039, 0.211582377, 0.254487434, 0.283667392, 0.299169568, 0.306463469],
     [0.473610048,0.408112931,0.399178775,0.330497145,0.285291557,0.283817819,0.24318878,0.207842142,0.174317669,0.150417068,0.117072669,0.116668458,0.13992336,0.142376156,0.148851713,0.175549644,0.187021551,0.214196344,0.222206467,0.229180889,0.278099419],
     [0.41569667,0.38710528,0.366185592,0.300360358,0.293180493,0.228429961,0.199018495,0.205160902,0.172663529,0.122588912,0.134222615,0.117089432,0.109214253,0.125142111,0.147025595,0.174323345,0.17843938,0.216773705,0.22236511,0.234356316,0.246609368],
     [0.376890638,0.355498824,0.338081113,0.288706516,0.256094094,0.235647726,0.208595973,0.1621284,0.142411069,0.151725121,0.141498814,0.125426724,0.145957744,0.129958711,0.136626485,0.166811865,0.167002751,0.205477374,0.193391573,0.201473509,0.209180297],
     [0.389667601,0.340887349,0.296384973,0.282934802,0.236495757,0.226187335,0.211197521,0.191383801,0.158488921,0.137957113,0.122618663,0.132392029,0.115614387,0.121273978,0.139935489,0.147239141,0.175945292,0.17132726,0.194346874,0.200481626,0.23293379],
     [0.363111083,0.328704898,0.292502727,0.252984527,0.244936658,0.226834433,0.209362735,0.192034209,0.164111476,0.154993215,0.130629062,0.141209439,0.137937211,0.123011101,0.14187836,0.150482203,0.177759153,0.195042703,0.192629693,0.208662201,0.207090454],
     [0.33297772,0.301467092,0.274580454,0.254395018,0.242110583,0.225933457,0.178525614,0.180613875,0.137316194,0.125899706,0.150095497,0.13846727,0.138193349,0.155723831,0.134927995,0.149651271,0.180798225,0.183358051,0.205489945,0.201725109,0.188400024],
     [0.296645901,0.269274588,0.252234076,0.239006479,0.225974909,0.21215817,0.193430321,0.16600369,0.146653962,0.147802393,0.125384942,0.138792335,0.151036559,0.140556824,0.142221445,0.167518314,0.149287246,0.193277158,0.197981125,0.203203886,0.185416068],
     [0.276149775,0.267377064,0.257684985,0.231008405,0.229410741,0.201830504,0.163780437,0.17231314,0.144902043,0.14797076,0.127612619,0.143006877,0.156296231,0.155158905,0.153138959,0.17163533,0.160075106,0.161647374,0.184620169,0.201284594,0.200718305],
     [0.288149921,0.243774673,0.224686628,0.217682634,0.206132095,0.185903478,0.19357274,0.164277543,0.151611709,0.16714264,0.133961281,0.155225495,0.154708059,0.1581292,0.163455462,0.141142465,0.145822354,0.155944268,0.159491421,0.173669272,0.191940383],
     [0.256715928,0.226993358,0.210702598,0.202799726,0.187429298,0.187856542,0.184440599,0.168071254,0.156894241,0.151702389,0.155613907,0.141142854,0.13459152,0.140408418,0.17374586,0.150469481,0.170319824,0.183177562,0.177046617,0.18705256,0.199960633],
     [0.260284095,0.237635128,0.205851111,0.192054744,0.207798503,0.177250169,0.160956534,0.156428047,0.166125328,0.157808781,0.162650243,0.161258402,0.154090597,0.15141293,0.176132788,0.177957854,0.162129901,0.157216446,0.16705591,0.176977494,0.201333272],
     [0.230598779,0.233650794,0.236639818,0.214781736,0.200237878,0.182011518,0.162842937,0.182731015,0.1776529,0.173479434,0.155573434,0.176582618,0.157654456,0.166282606,0.179974881,0.17613885,0.157744531,0.192277301,0.183388046,0.171902475,0.203745891]
]

mult_strikes = [strikes for i in range(len(vol))]

fitter = [ssvi.Ssvi([-0.3, 0.01], phi.QuotientPhi([0.4, 0.4])) for i in range(len(dates))]
surface = fitting.SurfaceFit(calc_date, dates, mult_strikes, vol, fitter,
                             weight_cut = 0.7,
                             calendar_buffer = 0.001)

surface.calibrate(maxiter = 50000, verbose = True)
surface.visualize()
