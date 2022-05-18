
# send gm message to #gm channel in different servers

import json
import os
import time
import requests


# get the auth token from GitHub secret
AUTH_TOKEN = os.environ['AUTH']


# verify if the auth or channel id is correct, fetch lastest 3 messages if succeed
def verify_auth_and_channel_id(channel_name, channel_id):
    headers = {'authorization': AUTH_TOKEN}
    params = {
        'limit': '3',
    }
    result = requests.get(
        f'https://discord.com/api/v9/channels/{channel_id}/messages', params=params,  headers=headers).json()

    if 'code' in result:
        print(f'x {channel_name} 认证失败, 提示: {result["message"]}')
        return False
    else:
        contents = [item['content'] for item in result]
        print(f'√ {channel_name} 认证通过, 最新信息: {contents} ')
        return True


# send msg gm to the given channel
def send_msg(channel_name, channel_id, msg='gm'):
    headers = {'authorization': AUTH_TOKEN}
    payload = {
        'content': {msg}
    }
    result = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', data=payload,  headers=headers).json()
    if 'code' in result:
        print(f'x {channel_name} 信息发送失败: ', result['message'])
        return False
    else:
        msg_id = result['id']
        print(f'✅ {channel_name} 信息发送成功, {msg_id = }')
        return


# get channle dict from channel json file
def get_channel_dict(channel_json='channels.json'):
    with open(channel_json, 'r') as f:
        channels = json.load(f)
    return channels


def main():
    
    # get channel dicts
    channels = get_channel_dict()

    for channel in channels.items():

        try:

            # get channel name, channel ID
            channel_name, channel_id = channel

            # verify
            flag = verify_auth_and_channel_id(channel_name, channel_id)
            
            if flag:
                # send gm
                send_msg(channel_name, channel_id)

        except Exception as e:
            print(f'❌ 运行出错, 提示: {e}')

        time.sleep(1)
    
    return


if __name__ == "__main__":
    main()
