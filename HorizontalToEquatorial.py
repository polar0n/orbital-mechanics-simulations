import math
from math import asin, atan2, trunc, degrees as deg

J2000y = {              # days since January 1 2000 00:00
    1998: -731.5,
    1999: -365.5,
    2000: -1.5  ,
    2001: 364.5 ,
    2002: 729.5 ,
    2003: 1094.5,
    2004: 1459.5,
    2005: 1825.5,
    2006: 2190.5,
    2007: 2555.5,
    2008: 2920.5,
    2009: 3286.5,
    2010: 3651.5,
    2011: 4016.5,
    2012: 4381.5,
    2013: 4747.5,
    2014: 5112.5,
    2015: 5477.5,
    2016: 5842.5,
    2017: 6208.5,
    2018: 6573.5,
    2019: 6938.5,
    2020: 7303.5,
    2021: 7669.5
}

J2000ML = {         # Days since the beginning of a leap year
    0: 0  ,        # January
    1: 31 ,        # February
    2: 60 ,        # March
    3: 91 ,        # April
    4: 121,        # May
    5: 152,        # June
    6: 182,        # July
    7: 213,        # August
    8: 244,        # September
    9: 274,        # October
    10: 305,        # November
    11: 335         # December
}

J2000M = {          # Days since the beginning of a non-leap year
    0: 0  ,
    1: 31 ,
    2: 59 ,
    3: 90 ,
    4: 120,
    5: 151,
    6: 181,
    7: 212,
    8: 243,
    9: 273,
    10: 304,
    11: 334
}

month = {           # Dictionary for easier retrieval of month id
    'Jan': 0 ,
    'Feb': 1 ,
    'Mar': 2 ,
    'Apr': 3 ,
    'May': 4 ,
    'Jun': 5 ,
    'Jul': 6 ,
    'Aug': 7 ,
    'Sep': 8 ,
    'Oct': 9 ,
    'Nov': 10,
    'Dec': 11
}


def sin(angle):                             # Function for simplifying big equations
    return math.sin(math.radians(angle))


def cos(angle):                             # Function for simplifying big equations
    return math.cos(math.radians(angle))


# Convert time [hours, minutes, seconds] or
def convToDecimals(time):
    if time[0] >= 0:                                    # degrees [degrees, arcminutes, arcseconds]
        # into decimal hours or degrees respectively.
        return time[0] + time[1]/60 + time[2]/3600
    else:
        # return *.* degrees or hours
        return time[0] - time[1]/60 - time[2]/3600


def convToTime(decimal):                            # Convert decimal hours or degrees
    # into time [hours, minutes, seconds] or
    time = [trunc(decimal), 0, 0]
    # degrees [degrees, arcminutes, arcseconds]
    if decimal < 0:
        decimal = -decimal                          # respectively.
    time[1] = (decimal - trunc(decimal)) * 60
    time[2] = (time[1] - trunc(time[1])) * 60
    time[1] = trunc(time[1])
    # return [hours/degrees, arc/-minutes, arc/-seconds]
    return time


def isLeap(year):               # Check if a year is a leap year
    return (year % 4) == 0


def getJ2000(time):
    # Get days since 2000 January 1 00:00 until certain time
    # time = [year, month(as id), day, hours, minutes, seconds]
    if isLeap(time[0]):
        return J2000y[time[0]] + J2000ML[time[1]] + time[2] + (time[3] + time[4]/60 + time[5]/3600) / 24
    else:
        return J2000y[time[0]] + J2000M[time[1]] + time[2] + (time[3] + time[4]/60 + time[5]/3600) / 24


def getLST(time, LONG, J2000):                                   # Get Local Sidereal Time
    return (100.46 + 0.985647*J2000 + LONG + 15*time) % 360


def getDEC(ALT, LAT, AZM):                                          # Get Declination
    return deg(asin(sin(ALT)*sin(LAT)+cos(ALT)*cos(LAT)*cos(AZM)))


def getHA(AZM, ALT, DEC, LAT):                                           # Get Hour Angle
    return deg(atan2(-(sin(AZM)*cos(ALT))/cos(DEC), (sin(ALT)-sin(LAT)*sin(DEC))/(cos(DEC)*cos(LAT))))


def getRA(LST, HA):                         # Get Right Ascension
    return ((LST - HA) % 360) / 15          # * / 15, from degrees to hours

AZM  = [186, 0, 58.68]             # [hours, minutes, seconds]
ALT  = [51, 43, 20.84]              # [degrees, arcminutes, arcseconds]
LAT  = [47, 3.393, 0]               # if South then sgn(LAT[0]) = -
LONG = [28, 50.775, 0]              # if West then sgn(LONG[0]) = -
t    = [23, 26, 50]                 # [hours, minutes, seconds]
date = [2017, month['Jul'], 2]     # [year, month, day]

AZM  = convToDecimals(AZM)
ALT  = convToDecimals(ALT)
LAT  = convToDecimals(LAT)
LONG = convToDecimals(LONG)
T    = convToDecimals(t)

J2000 = getJ2000(date + t)
LST   = getLST(T, LONG, J2000)
DEC   = getDEC(ALT, LAT, AZM)
HA    = getHA(AZM, ALT, DEC, LAT)
RA    = getRA(LST, HA)

print('DEC = ' + str([round(i, 3) for i in convToTime(DEC)]))
print('RA = ' + str([round(i, 3) for i in convToTime(RA)]))
