import os
import sys
#dir=sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
#print(dir)
import util.readPara1206 as rp


list_value=rp.read_api_File("util/api.ini")
# print(list_value)
# sym_list_value=rp.read_Ini_File()
# check_authCode=rp.verify_usedRight()
#use_right=rp.file_name('log')
#print(list_value)

access_key = list_value[0]
secret_key = list_value[1]
gateApi = list_value[2]
# used_code = list_value[3]
#access_key = "152696e6-10a6dda2-787fcb1a-bewr5drtmh"
#secret_key = "18f45246-85b7228d-996e0d98-82540"
GATEIO = {
    "USDT_1":
        {
            "ACCESS_KEY": access_key,
            "SECRET_KEY": secret_key,
            "SERVICE_API": gateApi,
        },

}

BITEX = {
    "USDT_1":
        {
            "ACCESS_KEY": access_key,
            "SECRET_KEY": secret_key,

        },
}

if __name__ == '__main__':
    # print_hi('PyCharm')
    print(list_value)