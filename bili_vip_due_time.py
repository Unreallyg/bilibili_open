import urllib3 as ub
import time as t
import json

ub.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
rq = ub.PoolManager(cert_reqs = 'CERT_NONE')
ub.disable_warnings()

ua = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54' ,
    'referer' : 'https://www.bilibili.com',
    'Content-Type' : 'application/json'
}

while True: 
    u=input('uid: ').strip()
    if u.isdigit() and u==str(int(u)):
        try:
            user = 'http://api.bilibili.com/x/web-interface/card?mid='+u
            info = rq.request('GET' , user , headers = ua)
            info = json.loads(info.data.decode('utf-8'))
            #print(json.dumps(info , ensure_ascii=False , indent=4 , separators=(',', ': ')))
            name,date,sts = info['data']['card']['name'],info['data']['card']['vip']['due_date'],info['data']['card']['vip']['status']
            if date == 0:
                print('\n账号 {} {}\n'.format(name,'没充过大会员捏'))
            else:
                if sts == 0:
                    st=t.localtime(date/1000)
                    print('\n账号 {} 的{}\n'.format(name,t.strftime('大会员已失效，上次大会员已于%Y年%m月%d日到期',st)))
                else:
                    st=t.localtime(date/1000)
                    print('\n账号 {} 的{}\n'.format(name,t.strftime('大会员生效中，本次大会员将于%Y年%m月%d日到期',st)))
                
        except Exception as e:
            print('\nError:\n'+str(e)+'\n')
    else:
        print('\n输入非uid，重新输入\n')

        
