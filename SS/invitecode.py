import config
from store import DbToMysql


def get_invite_code():
    store = DbToMysql(config.EHCO_DB)
    res = store.find_by_fields('shadowsocks_invitecode', {
                               'code_id': 1, 'isused': 0})
    if res != -1:
        if len(res) > 0:
            return res[0]['code']
        else:
            return '邀请码用光啦'
