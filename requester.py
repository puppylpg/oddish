import requests

import timer

cookie_str = r'_ga=GA1.2.162602080.1551374933; _ntes_nnid=8ce0cf6bdce55512e73f49cb8a49960e,1552104955025; _ntes_nuid=8ce0cf6bdce55512e73f49cb8a49960e; mail_psc_fingerprint=d80ec72871726e9b192181fd1a3633d6; usertrack=CrH5y11BrGaqLV9AAwiDAg==; vinfo_n_f_l_n3=d81bf3a25989eb31.1.2.1561837557589.1561866895199.1568433963014; __f_=1571910788620; OUTFOX_SEARCH_USER_ID_NCOO=29659292.15961449; Device-Id=33u998YqmNWbhH5GbWUo; nts_mail_user=thingsregister@163.com:-1:1; csrf_token=2c8d53c77a70deb83621717194d4615b3fca8fad; game=csgo; _gid=GA1.2.1251254888.1575035437; Locale-Supported=zh-Hans; r_ntcid=730:57; NTES_YD_SESS=tG2nZowAlrjr45l_b0r4dCP7cclSNqHrTDHBL.vWUH.6uWdmu57zsxGBCpF9Qc_widWltCqK44w2wicTMfqDPMS7_P1ANNmsTqXqxoF5uL29PLmT7vK7FaYgTLzPfbgrpL1XO8nBPXiafVzvHlE1ZQsMr4E5hf1O9aS_RUHVMkJqX96lMZzFOUkWnRUQ.LJLnwBVFd8W3KuPHu0XhwHdIjq73kGCgakUYJczMN8t53Wlb; S_INFO=1575049340|0|3&80##|18810702051; P_INFO=18810702051|1575049340|1|netease_buff|00&99|bej&1575035452&netease_buff#bej&null#10#0#0|&0|null|18810702051; session=1-CPFnKjtkqi52ckZ1VNKNbGcXaUaaZ1uy_E6YfLLzaANY2046524528; _gat_gtag_UA_109989484_1=1'
cookies = {}
for line in cookie_str.split(';'):
    k, v = line.split('=', 1)
    cookies[k] = v

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}


def get_json(url):
    timer.sleep_awhile()
    return requests.get(url, headers=headers, cookies=cookies).json()
