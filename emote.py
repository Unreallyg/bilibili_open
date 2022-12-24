from os.path import exists as osPathExists
from os import makedirs as osMakedirs
#import errors
from requests import get as rqGet
url=input('https://api.bilibili.com/x/emote/package?business=watch_full&ids=').strip()
url='https://api.bilibili.com/x/emote/package?business=watch_full&ids='+url
i = rqGet(url)
res = i.json()
if res['code'] == 0:
    base_dir =  res['data']['packages'][0]['text']
    emoji_list = [
        (item['text'][1:-1], item['url'])
        for item in res['data']['packages'][0]['emote']
    ]
    if not osPathExists(base_dir + '/'):
        osMakedirs(base_dir + '/')

    for i, item in enumerate(emoji_list):
        img_name = item[0]
        try:
            with open(base_dir + '/' + img_name + '.png',
                      'wb') as emoji_file:
                emoji_file.write(rqGet(item[1]).content)
        except OSError:
            #errors._show_error(4)
            img_name = img_name.split('_')[0] + '_{}'.format(i)
            try:
                with open(base_dir + '/' + img_name + '.png', 'wb') as emoji_file:
                    emoji_file.write(rqGet(item[1]).content)
            except:
                pass
            final_status = 101
        #except:
            #errors._show_error(1)
    input('done')
else:
    print('???')

