import http.client
import re
import urllib.request

#http://api.ipify.org/ - 291s
#http://api.myip.com - 263s
def getIp(proxy, timeout = None, method="http"):
    proxy_handler = urllib.request.ProxyHandler({f"{method}": f"{method}://{proxy}"})
    opener = urllib.request.build_opener(proxy_handler)
    try:
        response = opener.open(f'{method}://api.ipify.org/', timeout=timeout)
        response = response.read().decode('utf-8')
    except Exception as e:
        print(e)
        response = ""
    finally:
        opener.close()
        return response

def getUnparsedHTMLproxies():
    conn = http.client.HTTPSConnection("free-proxy-list.net")
    headers = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    conn.request("GET", "/", headers=headers)
    return conn.getresponse().read().decode("UTF-8")

def parseHTMLproxies(HTML):
    table = re.findall('<table class="table table-striped table-bordered">(.*?)<\/table>', HTML)[0]
    return re.findall('<td.*?>(.*?)<\/td>', table)

def getFreeProxies():
    HTMLproxies = getUnparsedHTMLproxies()
    return parseHTMLproxies(HTMLproxies)

def checkProxiesOperability(proxies, method="http"):
    for i in range(0, len(proxies), 8):
        proxy, port, country = [proxies[i], proxies[i+1], proxies[i+2]]
        if((country != "RU") and (getIp(f'{proxy}:{port}', 1, method) == proxy)):
            yield f'{proxy}:{port}'