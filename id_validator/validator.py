#!/usr/bin/env python
# encoding: utf-8

from . import utils
from . import helper
from . import data
import random
from datetime import datetime


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def is_valid(id_card, strict_mode=False):
    """
    检测身份证合法性
    :param id_card:
    :param strict_mode
    :return:
    """
    id_card = str(id_card)
    code = helper.get_id_argument(id_card)
    if not helper.check_address_code(code['address_code'], code['birthday_code'], strict_mode):
        print('address_code 错误:',code['address_code'])
        return False

    if not helper.check_birthday_code(code['birthday_code']):
        print('birthday_code 错误:',code['birthday_code'])
        return False

    if not helper.check_order_code(code['order_code']):
        print('order_code 错误:',code['order_code'])
        return False

    if code['type'] == 15:
        return True

    check_bit = helper.generator_check_bit(code['body'])
    if check_bit != code['check_bit']:
        print('check_bit 错误:',check_bit)
        return False

    return True


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def get_info(id_card, strict_mode=False):
    """
    获取身份证信息
    :param id_card:
    :param strict_mode:
    :return:
    """
    id_card = str(id_card)

    if not is_valid(id_card, strict_mode):
        return dict()

    code = helper.get_id_argument(id_card)
    address_info = helper.get_address_info(code['address_code'], code['birthday_code'], strict_mode)
    info = dict()
    info['address_code'] = code['address_code']
    info['abandoned'] = helper.check_abandoned(code['address_code'])
    info['address'] = address_info['province'] + address_info['city'] + address_info['district']
    info['address_tree'] = [address_info['province'], address_info['city'], address_info['district']]
    info['age'] = datetime.now().year - int(code['birthday_code'][0:4])
    info['birthday_code'] = code['birthday_code'][0:4] + '-' + code['birthday_code'][4:6] + '-' + code['birthday_code'][
                                                                                                  6:8]
    info['constellation'] = helper.get_constellation(code['birthday_code'])
    info['chinese_zodiac'] = helper.get_chinese_zodiac(code['birthday_code'])
    info['sex'] = 0 if int(code['order_code']) % 2 == 0 else 1
    info['length'] = code['type']
    info['check_bit'] = code['check_bit']

    return info


def fake_id(eighteen=True, address=None, birthday=None, sex=None):
    """
    伪造身份证
    :param eighteen:
    :param address:
    :param birthday:
    :param sex:
    :return:
    """
    if address is None:
        address_code, address = random.choice(list(data.get_address_code().items()))
    else:
        address_code = helper.generator_address_code(address)
    birthday_code = helper.generator_birthday_code(address_code, address, birthday)
    order_code = helper.generator_order_code(sex)

    if not eighteen:
        return address_code + birthday_code[2:] + order_code

    body = address_code + birthday_code + order_code
    check_bit = helper.generator_check_bit(body)

    return body + check_bit


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def upgrade_id(id_card):
    """
    身份证号码升级（15 位升级为 18 位）
    :param id_card:
    :return:
    """
    if not is_valid(id_card):
        return False
    code = helper.get_id_argument(id_card)
    body = code['address_code'] + code['birthday_code'] + code['order_code']
    return body + helper.generator_check_bit(body)
