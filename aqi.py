
from crawler import get_data, get_web_page, get_data_index

class Aqi:
    @staticmethod
    def get_pm25aqi(pm25):
        try:
            pm25=float(pm25)
            if pm25<15.5:
                pm25AQI=((50-0)/(15.4-0))*(pm25-0)+0
                return pm25AQI
            if pm25<35.5:
                pm25AQI=((100-51)/(35.4-15.5))*(pm25-15.5)+51
                return pm25AQI
            if pm25<54.5:
                pm25AQI=((150-101)/(54.4-35.5))*(pm25-35.5)+101
                return pm25AQI
            if pm25<150.5:
                pm25AQI=((200-151)/(150.4-54.5))*(pm25-54.5)+151
                return pm25AQI
            else:
                return -1
        except:
            return -1
    @staticmethod
    def get_o3aqi(o3):
        try:
            o3=float(o3)
            if o3<55:
                o3AQI=((50-0)/(54-0))*(o3-0)+0
                return o3AQI
            if o3<71:
                o3AQI=((100-51)/(70-55))*(o3-55)+51
                return o3AQI
            if o3<86:
                o3AQI=((150-101)/(85-71))*(o3-71)+101
                return o3AQI
            else:
                return -1
        except:
            return -1
    @staticmethod
    def get_pm10aqi(pm10):
        try:
            pm10=float(pm10)
            if pm10<55:
                pm10AQI=((50-0)/(54-0))*(pm10-0)+0
                return pm10AQI
            if pm10<126:
                pm10AQI=((100-51)/(125-55))*(pm10-55)+51
                return pm10AQI
            if pm10<255:
                pm10AQI=((150-101)/(254-126))*(pm10-126)+101
                return pm10AQI
            else:
                return -1
        except:
            return -1
    @staticmethod
    def get_coaqi(co):
        try:
            co=float(co)
            if co<4.5:
                coAQI=((50-0)/(4.5-0))*(co-0)+0
                return coAQI
            if co<9.5:
                coAQI=((100-51)/(9.4-4.5))*(co-4.5)+51
                return coAQI
            if co<12.5:
                coAQI=((150-101)/(12.4-9.5))*(co-9.5)+101
                return coAQI
            else:
                return -1
        except:
            return -1
    @staticmethod
    def get_so2aqi(so2):
        try:
            so2=float(so2)
            if so2<36:
                so2AQI=((50-0)/(35-0))*(so2-0)+0
                return so2AQI
            if so2<76:
                so2AQI=((100-51)/(75-36))*(so2-36)+51
                return so2AQI
            if so2<186:
                so2AQI=((150-101)/(185-76))*(so2-76)+101
                return so2AQI
            else:
                return -1
        except:
            return -1
    @staticmethod
    def get_no2aqi(no2):
        try:
            no2=float(no2)
            if no2<54:
                no2AQI=((50-0)/(53-0))*(no2-0)+0
                return no2AQI
            if no2<101:
                no2AQI=((100-51)/(100-54))*(no2-54)+51
                return no2AQI
            if no2<361:
                no2AQI=((150-101)/(360-101))*(no2-101)+101
                return no2AQI
            else:
                return -1
        except:
            return -1
    @staticmethod
    def now_aqi(data):
        pm25aqi=Aqi.get_pm25aqi(data['PM2.5'])
        pm10aqi=Aqi.get_pm10aqi(data['PM10'])
        o3aqi=Aqi.get_o3aqi(data['O3'])
        coaqi=Aqi.get_coaqi(data['CO'])
        so2aqi=Aqi.get_so2aqi(data['SO2'])
        no2aqi=Aqi.get_no2aqi(data['NO2'])
        #print(pm25aqi,pm10aqi,o3aqi,coaqi,so2aqi,no2aqi)
        return max(pm25aqi,pm10aqi,o3aqi,coaqi,so2aqi,no2aqi)
    @staticmethod
    def aqi_with_simple_format(data):
        out=""
        out=data["SiteName"]+"\n    AQI : "+data["AQI"]+"\n    Now AQI : "\
        +str(Aqi.now_aqi(data))+"\n    空氣品質 ： "+data["Status"]+"\n"
        return out
    @staticmethod
    def aqi_with_complex_format(data):
        pm25aqi=Aqi.get_pm25aqi(data['PM2.5'])
        pm10aqi=Aqi.get_pm10aqi(data['PM10'])
        o3aqi=Aqi.get_o3aqi(data['O3'])
        coaqi=Aqi.get_coaqi(data['CO'])
        so2aqi=Aqi.get_so2aqi(data['SO2'])
        no2aqi=Aqi.get_no2aqi(data['NO2'])
        aqi=max(pm25aqi,pm10aqi,o3aqi,coaqi,so2aqi,no2aqi)
        out=""
        out=data["SiteName"]+"\n    AQI : "+data["AQI"]+"\n    Now AQI : "\
        +str(aqi)+"\n    空氣品質 ： "+data["Status"]+"\n"\
        +"    PM2.5:%8.2f"%pm25aqi+"%6s"%data['PM2.5']+"μg/m3\n"\
        +"    PM10: %8.2f"%pm10aqi+"%6s"%data['PM10']+"μg/m3\n"\
        +"    O3:   %8.2f"%o3aqi+"%6s"%data['O3']+"ppb\n"\
        +"    CO:   %8.2f"%coaqi+"%6s"%data['CO']+"ppm\n"\
        +"    SO2:  %8.2f"%so2aqi+"%6s"%data['SO2']+"ppb\n"\
        +"    NO2:  %8.2f"%no2aqi+"%6s"%data['NO2']+"ppb\n"
        return out
if __name__ == "__main__":
    r=get_data()
    index=get_data_index(r)
    data=r[71]
    pm25aqi=Aqi.get_pm25aqi(data['PM2.5'])
    pm10aqi=Aqi.get_pm10aqi(data['PM10'])
    o3aqi=Aqi.get_o3aqi(data['O3'])
    coaqi=Aqi.get_coaqi(data['CO'])
    so2aqi=Aqi.get_so2aqi(data['SO2'])
    no2aqi=Aqi.get_no2aqi(data['NO2'])
    print("AQI:  %8.2f"%max(pm25aqi,pm10aqi,o3aqi,coaqi,so2aqi,no2aqi))
    print("PM2.5:%8.2f"%pm25aqi,"%6s"%data['PM2.5'],"μg/m3")
    print("PM10: %8.2f"%pm10aqi,"%6s"%data['PM10'],"μg/m3")
    print("O3:   %8.2f"%o3aqi,"%6s"%data['O3'],"ppb")
    print("CO:   %8.2f"%coaqi,"%6s"%data['CO'],"ppm")
    print("SO2:  %8.2f"%so2aqi,"%6s"%data['SO2'],"ppb")
    print("NO2:  %8.2f"%no2aqi,"%6s"%data['NO2'],"ppb")
    #%%
    print(Aqi.aqi_with_complex_format(data))