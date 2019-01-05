import datetime
import smbus
from time import  strftime

def _bcd_to_int(bcd):
    """Decode a 2x4bit BCD to a integer.
    """
    out = 0 
    for d in (bcd >> 4, bcd):
        for p in (1, 2, 4 ,8):
            if d & 1:
                out += p
            d >>= 1
        out *= 10
    return (out / 10)


def _int_to_bcd(n):
    """Encode a one or two digits number to the BCD.
    """
    bcd = 0
    for i in (n // 10, n % 10):
        for p in (8, 4, 2, 1):
            if i >= p:
                bcd += 1
                i -= p
            bcd <<= 1
    return bcd >> 1
class DS3231:
    w  = ["Mon","Tues","Wed","Thur","Fri","Sat","Sun"]
    def __init__(self, twi ,address=0x68, register=0x00):
        self.address = address
        self.register = register
        self._bus = smbus.SMBus(twi) 
        self._datetimelist = []
        self.rtctime = []

   
    def _ds3231SetTime(self,NowTime):
        self._bus.write_i2c_block_data(self.address,self.register,NowTime)
    #/dev/i2c-1
    def _ds3231ReadTime(self):
        return self._bus.read_i2c_block_data(self.address,self.register,7)
# sec min hour week day month year


    def setTime(self,seconds=None, minutes=None, hours=None, weekday =None ,
            date=None, month=None, year=None):

        #    seconds
        if seconds <60 and seconds >= 0:
            self._datetimelist.append(_int_to_bcd(seconds))
        else:
            _datetimelist = []
            raise ValueError('Seconds is out of range [0,59].')   
        #    minutes  
        if minutes <60 and minutes >= 0:
            self._datetimelist.append(_int_to_bcd(minutes))
        else:
            self._datetimelist = []
            raise ValueError('Minutes is out of range [0,59].')   

        #    hours
        if hours <24 and hours >= 0:
            self._datetimelist.append(_int_to_bcd(hours))
        else:
            self._datetimelist = []
            raise ValueError('Hours is out of range [0,23].')  
        #    weekday
        if weekday <7 and weekday >= 0:
            self._datetimelist.append(_int_to_bcd(weekday))
        else:
            self._datetimelist = []
            raise ValueError('weekday is out of range [1,7].')  
        #   day
        if date <=31 and date >= 1:
            self._datetimelist.append(_int_to_bcd(date))
        else:
            self._datetimelist = []
            raise ValueError('date is out of range [1,31].')    
        #   month
        if hours <24 and hours >= 0:
            self._datetimelist.append(_int_to_bcd(hours))
        else:
            self._datetimelist = []
            raise ValueError('month is out of range [1,12].')             
         #  year

        if year <100 and year >= 0:
            self._datetimelist.append(_int_to_bcd(year))
        else:
            self._datetimelist = []
            raise ValueError('year is out of range [0,99].') 

        self._ds3231SetTime(self._datetimelist)


    def setNow(self):
        t =  datetime.datetime.now()
        week = datetime.datetime.today().weekday()
        sec = int(t.strftime("%S"))
        min = int(t.strftime("%M"))
        hour = int(t.strftime("%H"))
        day = int(t.strftime("%d"))
        month = int(t.strftime("%m"))
        year = int(t.strftime("%Y")[2:])
        print(year)
        NowTime = [_int_to_bcd(sec),_int_to_bcd(min),_int_to_bcd(hour)
                ,_int_to_bcd(week),_int_to_bcd(day),_int_to_bcd(month),_int_to_bcd(year)]
        self._bus.write_i2c_block_data(self.address,self.register,NowTime)
    def readTime(self):
        t = self._ds3231ReadTime()
        sec = _bcd_to_int(t[0])
        min = _bcd_to_int(t[1])
        hour = _bcd_to_int(t[2])
        day = _bcd_to_int(t[4])
        month = _bcd_to_int(t[5])
        year = _bcd_to_int(t[6])
        time = datetime.datetime(year=year,month=month,day=day,hour=hour,minute=min,second=sec)
        print(time)
        return time
if __name__ == "__main__":
    dt = DS3231(0)
    dt.readTime() 
