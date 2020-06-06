import requests
from bs4 import BeautifulSoup as Bs


def get_proxy_xseo():
    proxy = []
    request = requests.get('http://xseo.in/proxylist')
    soup = Bs(request.text, 'lxml')
    key = soup.find('script', attrs={'type': 'text/javascript'})
    sub_key = str(key)[31:len(key)-11].split(';')
    info = soup.find_all('font', attrs={'class': 'cls1'})
    del info[0]
    for n in info:
        if len(str(n)) > 67:
            ip = str(n)[19: str(n).index('<font class="cls4">')]
            port = str(n)[str(n).index('document.write(""+') + 18: str(n).index(')</script>')]
            pro = str(ip + ':')
            for ip_n in port.split('+'):
                for key_n in sub_key:
                    if key_n[:1] == ip_n:
                        pro += str(key_n[2:])
            print(pro)
            proxy.append(pro)
    return proxy


if __name__ == '__main__':
    get_proxy_xseo()
