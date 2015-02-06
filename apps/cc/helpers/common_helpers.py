# -*- coding:utf8 -*-
import logging
import datetime
import pymongo
import sys

file   = '/www/log/cc.log'

logger = logging.getLogger('')
# create file handler which logs even debug messages
formatter = logging.Formatter("%(asctime)s - %(message)s")

fh = logging.FileHandler(file)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.INFO)

COUNTRY_CODE = {
    u'中国':'CH',
    u'澳门':'MC',
    u'香港':'HK',
    u'台湾':'TW',
}
REGION_CODE = {
    u'上海市':'SH' , 
    u'浙江省':'ZJ' ,
    u'海南省': 'HA', 
    u'西藏自治区': 'XZ', 
    u'云南省': 'YN', 
    u'安徽省': 'AH', 
    u'湖北省': 'HU', 
    u'陕西省': 'SA', 
    u'重庆市': 'CQ', 
    u'贵州省': 'GZ', 
    u'湖南省': 'HN', 
    u'四川省': 'SC', 
    u'山西省': 'SX', 
    u'河南省': 'HE', 
    u'江西省': 'JX', 
    u'内蒙古自治区':'NM' , 
    u'广西壮族自治区': 'GX', 
    u'黑龙江省':'HL' , 
    u'福建省': 'FJ', 
    u'广东省': 'GD', 
    u'北京市': 'BJ', 
    u'河北省': 'HB', 
    u'辽宁省': 'LN', 
    u'山东省': 'SD', 
    u'天津市': 'TJ', 
    u'江苏省': 'JS', 
    u'青海省': 'QH', 
    u'甘肃省': 'GS', 
    u'新疆维吾尔自治区': 'XJ', 
    u'吉林省': 'JL', 
    u'宁夏回族自治区': 'NX',
    u'香港特别行政区':'HK',#6668
    u'澳门特别行政区':'MC',#3681
    u'台湾省':'TW',#tp
}
ISP = {
    u'联通':'CUCC',
    u'移动':'CMCC',
    u'铁通':'CTT',
    u'电信':'CTCC',
    u'宽频':'HKBN',
    u'其他':'OTHER'
}

def get_pv_by_city(type):
    now_date = datetime.datetime.now()
    str_last_date = (now_date-datetime.timedelta(hours=1)).strftime('%Y%m%d%H')+'0000'
    str_now_date = now_date.strftime('%Y%m%d%H')+'0000'
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    client.the_database.authenticate('huxiu','huxiu@123',source='admin')
    common_db = client['common']
    tjj_db = client['tjj']
    data = []

    for k in REGION_CODE:
        ips = common_db.ips.find({'region':REGION_CODE[k]}).distinct('ip')
        if int(type) == 0:
            region_pv_count = tjj_db.cc.find({'time':{"$gte": str_last_date,'$lt':str_now_date},'ip':{'$in':ips}}).count()
        elif int(type) == 1:
            region_pv_count = len(tjj_db.cc.find({'time':{"$gte": str_last_date,'$lt':str_now_date},'ip':{'$in':ips}}).distinct('cookie'))
        elif int(type) == 2:
            region_pv_count = len(tjj_db.cc.find({'time':{"$gte": str_last_date,'$lt':str_now_date},'ip':{'$in':ips}}).distinct('ip'))
        elif int(type) == 3:
            region_pv_count = tjj_db.cc.find({'uid':{"$gt":0},'time':{"$gte": str_last_date,'$lt':str_now_date},'ip':{'$in':ips}}).count()
        if region_pv_count == 0:
            region_pv_count = 1
        if REGION_CODE[k] == 'TW':
            data.append({'hc-key':'tw-tp','value':region_pv_count})
        elif REGION_CODE[k] == 'HK':
            data.append({'hc-key':'cn-6668','value':region_pv_count})
        elif REGION_CODE[k] == 'MC':
            data.append({'hc-key':'cn-3681','value':region_pv_count})
        else:
            data.append({'hc-key':'cn-'+REGION_CODE[k].lower(),'value':region_pv_count})
    client.close()
    return data

def find_by_uid(uid,sign_type):
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    client.the_database.authenticate('huxiu','huxiu@123',source='admin')
    db = client['tjj']
    collection = db['cc']

    now_date = datetime.datetime.now()
    str_last_date = (now_date-datetime.timedelta(days=3)).strftime('%Y%m%d')+'000000'
    str_now_date = now_date.strftime('%Y%m%d')+'000000'

    user = list(set([k['cookie'] for k in collection.find({'uid':int(uid),"time": {"$gte": str_last_date,'$lt':str_now_date}})]))

    if sign_type == 1:
        paths = collection.find({'uid':int(uid),'cookie':{'$in':list(user)},"time": {"$gte": str_last_date,'$lt':str_now_date}}).sort('time',pymongo.ASCENDING)
    elif sign_type == 2:
        paths = collection.find({'uid':0,'cookie':{'$in':list(user)},"time": {"$gte": str_last_date,'$lt':str_now_date}}).sort('time',pymongo.ASCENDING)
    else:
        paths = collection.find({'cookie':{'$in':list(user)},"time": {"$gte": str_last_date,'$lt':str_now_date}}).sort('time',pymongo.ASCENDING)
    client.close()
    return paths

def into_mongodb(args):
    logging.info(args['ip']+','+args['page']+','+args['last_page']+','+args['user_agent']+','+args['cookie']+','+str(args['uid']))
    
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    client.the_database.authenticate('huxiu','huxiu@123',source='admin')
    db = client['tjj']
    collection = db['cc']
    try:
        collection.insert(args)
    except:
        pass
    client.close()
    return 
