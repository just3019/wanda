import threading

import wanda_utils

TOKEN = '00754768297fe9da7e9055e4a63532d1248d2858'
PLAZAID = '1105202'
PROVINCE = ''
PLACE = '衢州'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()