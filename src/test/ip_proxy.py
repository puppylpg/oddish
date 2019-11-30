from itertools import cycle

import requests

from src.test import proxy_pool

if __name__ == '__main__':
    proxies = ["124.205.143.213:56299"]
    # proxies = proxy_pool.get()
    print(proxies)

    url = 'https://ip.sb'
    for i in range(1, 11):
        # Get a proxy from the pool
        proxy = next(cycle(proxies))
        print("Request #%d" % i)
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            print(response.json())
        except:
            # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error")

    # url = 'https://api.ipify.org/?format=json'
    # proxies1 = {
    #     "https": 'http://209.90.63.108:80',
    #     "http": 'http://61.135.185.156:80'
    # }
    # print("Raw IP: {}".format(requests.get(url).json()))
    #
    # for i in range(1):
    #     response = requests.get(url, proxies=proxies1)
    #     print("Proxy IP: {}".format(response.json()))
    #
    # proxies1 = {
    #     "https": 'http://43.252.18.140:56788',
    #     "http": 'http://201.159.177.74:41170'
    # }
    # for i in range(1):
    #     response = requests.get(url, proxies=proxies1)
    #     print("Proxy IP: {}".format(response.json()))
