import datetime
import logging

def initLogging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def convert_to_itemlist_ordered(sub_obj):

    for ke in sub_obj.keys():
        if len(sub_obj[ke]) > 0:
            sub_obj[ke] = sub_obj[ke][0]
        elif len(sub_obj[ke]) <= 0:
            sub_obj[ke] = ''

    pro_name = ''
    name_list = sub_obj['problem_full_name'].split(' ')
    if len(name_list) > 0:
        pro_name = name_list[0]

    item_list = []
    item_list.append(sub_obj['id'])
    item_list.append(sub_obj['submit_url'])
    item_list.append(sub_obj['submit_time'])
    item_list.append(sub_obj['user_id'])
    item_list.append(sub_obj['user_name'])
    item_list.append(sub_obj['problem_id'])
    item_list.append(sub_obj['problem_url'])
    item_list.append(pro_name)
    item_list.append(sub_obj['problem_full_name'])
    item_list.append(sub_obj['language'])
    item_list.append(sub_obj['status'])
    item_list.append(sub_obj['error_test_id'])
    item_list.append(sub_obj['time'])
    item_list.append(sub_obj['memory'])
    item_list.append("")
    return item_list


