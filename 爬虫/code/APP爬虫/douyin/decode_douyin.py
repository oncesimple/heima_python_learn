import json
try:
    from douyin.handle_mongo import save_task
except:
    from handle_mongo import save_task

def response(flow):
    if 'aweme/v1/user/follower/dataList/' in flow.request.url:
        for user in json.loads(flow.response.text)['followers']:
            douyin_info = {}
            douyin_info['share_id'] = user['uid']
            douyin_info['douyin_id'] = user['short_id']
            save_task(douyin_info)

