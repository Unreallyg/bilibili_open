import urllib3 as ub
import json
from os.path import exists as osPathExists
from os import makedirs as osMakedirs
import time as t

rq=ub.PoolManager()
ua = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36' ,
    'referer' : 'https://www.bilibili.com',
    'Content-Type' : 'application/json'
}

while True:
    uid = input('动态ID：')
    try:
        num = int(eval(input('获取人数(大于全部点赞人数则获取全部)：').strip()))
    except:
        while True:
            num = input('输入为非数字，请重新输入：').strip()
            if num.isdigit():
                num = int(eval(num))
                break
    temp = list()
    temp.append(f'\n本次输入查询人数：{num}\n\n')
    ima = t.strftime('查询时间(GMT+8:00)：%Y年%m月%d日 %H:%M:%S',t.localtime(t.time()))
    stop = False
    for p in range(1,99999999):
        try:
            like = 'https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/spec_item_likes?'\
                   +'ps=50&dynamic_id='+str(uid)+'&pn='+str(p)
            info = rq.request('GET' , like , headers = ua)
            info = json.loads(info.data)
            l = info['data']['item_likes']
            count=50*(p-1)+1
            for i in range(len(l)):
                if count <= num:
                    data = '{}. {}    UID: {}'.format(count,l[i]['uname'],l[i]['uid'])
                    print(data)
                    temp.append(data+'\n'*2)
                    count+=1
                else:
                    stop = True
                    break
            if stop:
                temp.append(ima+'\n')
                spl = '-'*90+'\n'+'#'*60+'\n'+'-'*90+'\n'
                temp.append(spl)
                if not osPathExists('B站动态点赞列表查询/'):
                    osMakedirs('B站动态点赞列表查询/')
                filename = '动态ID：{}.txt'.format(uid)
                with open('B站动态点赞列表查询/'+filename,'a',encoding='UTF-8')as f:
                    f.writelines(temp)
                break
        except KeyError:
            temp.append(ima+'\n')
            spl = '-'*90+'\n'+'#'*60+'\n'+'-'*90+'\n'
            temp.append(spl)
            if not osPathExists('B站动态点赞列表查询/'):
                osMakedirs('B站动态点赞列表查询/')
            filename = '动态ID：{}.txt'.format(uid)
            with open('B站动态点赞列表查询/'+filename,'a',encoding='UTF-8')as f:
                f.writelines(temp)
            break
        except Exception as e:
            print(f'Error:\n{e}')
            
