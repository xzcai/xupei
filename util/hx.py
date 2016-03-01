import datetime

import requests
import json

from data.database.Mongo.HxToken import HxToken

JSON_HEADER = {'content-type': 'application/json'}


def http_result(r):
    if r.status_code == requests.codes.ok:
        return True, r.json()
    else:
        return False, r.text


class HxHelper:
    __clientID = "YXA6mFx14CUXEeW0GWtM2e9ekA"
    __clientSecret = 'YXA6bggrqeXUr0TArQFjsK28u2SgnnQ'
    __appName = "test"
    __orgName = "benhu-hx"
    __reqUrlFormat = "https://a1.easemob.com/" + __orgName + "/" + __appName + "/"
    __get_token_request_body = {'grant_type': 'client_credentials', 'client_id': __clientID,
                                'client_secret': __clientSecret}

    @staticmethod
    def get_token():
        token_obj = HxToken.objects().first()
        if token_obj is None:
            result = requests.post(HxHelper.__reqUrlFormat + 'token', json.dumps(HxHelper.__get_token_request_body),
                                   headers={'content-type': 'application/json'})
            if result.status_code == requests.codes.ok:
                HxToken(value=result.json()["access_token"], past_due=datetime.datetime.now() + datetime.timedelta(
                        seconds=result.json()["expires_in"] - 10)).save()
                return result.json()["access_token"]
            else:
                return ''

        if token_obj.past_due <= datetime.datetime.now():
            result = requests.post(HxHelper.__reqUrlFormat + 'token', json.dumps(HxHelper.__get_token_request_body),
                                   headers={'content-type': 'application/json'})
            if result.status_code == requests.codes.ok:
                token_obj.value = result.json()["access_token"]
                token_obj.past_due = datetime.datetime.now() + datetime.timedelta(
                        seconds=result.json()["expires_in"] - 10)
                token_obj.save()
                return result.json()["access_token"]
            else:
                return ''
        return token_obj.value

    # 注册环信账户
    @staticmethod
    def create_account(username, password, nickname):
        try:
            token = HxHelper.get_token()
            JSON_HEADER['Authorization'] = 'Bearer ' + token
            payload = {'username': username, 'password': password, 'nickname': nickname}
            print(11111111111111111111111111111111111111111111111111)
            result = requests.post(HxHelper.__reqUrlFormat + 'users', json.dumps(payload), headers=JSON_HEADER)
            print(22222222222222222222222222222222222222222222222222)
            if result.status_code == requests.codes.ok:
                return True
            else:
                return False
        except Exception as e:
            print(44444444444444444444444444444444444444444444444)
            print(e)
            return False

    # 删除环信账户
    @staticmethod
    def delete_account(username):
        token = HxHelper.get_token()
        JSON_HEADER['Authorization'] = 'Bearer ' + token
        result = requests.delete(HxHelper.__reqUrlFormat + 'users/' + username, headers=JSON_HEADER)
        if result.status_code == requests.codes.ok:
            return True
        else:
            return False

    @staticmethod
    def create_group(group_name, desc, owner, approval=False, public=True):
        payload = {'groupname': group_name, 'desc': desc, "public": public, 'approval': approval, 'owner': owner}
        result = requests.post(HxHelper.__reqUrlFormat + 'chatgroups', json.dumps(payload), headers=JSON_HEADER)
        if result.status_code == requests.codes.ok:
            return True
        else:
            return False
