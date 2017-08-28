# -*- coding: utf-8 -*-


class ErrorCode(Exception):
    def __init__(self, eid, message):
        self.eid = eid
        self.message = message

    def __str__(self):
        return self.message

STATE_OK = ErrorCode(200, 'ok')
STATE_CREATE_OK = ErrorCode(201, '创建资源ok')
STATE_UNKNOWN = ErrorCode(451, '未知错误')
STATE_LOGIN_ERR = ErrorCode(401, '登陆验证错误')
STATE_PARAM_ERR = ErrorCode(402, '参数错误')
STATE_DB_UPDATE_ERR = ErrorCode(422, '数据库更新错误')
STATE_EmptyData_ERR = ErrorCode(400, '数据库查询为空数据')
