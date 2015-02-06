# -*- coding:utf8 -*-
import datetime
from urlparse import urlparse
from urllib import urlencode,unquote

import pymongo

def __fix_datetime_to_hours(str_start_time):
    hours = []
    now_time = datetime.datetime.now()
    if str_start_time:
        start_time = datetime.datetime.strptime(str_start_time[0:10],'%Y%m%d%H')
        hour = int((now_time-start_time).total_seconds()/60/60)
        hours.append(start_time.strftime('%Y%m%d%H')+'0000')
        for k in range(hour):
            hours.append((start_time+datetime.timedelta(hours=k+1)).strftime('%Y%m%d%H')+'0000')
    return hours

def find_page_rank(page,type='total',days=2):
    s_time = datetime.datetime.now()
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    client.the_database.authenticate('huxiu','huxiu@123',source='admin')
    db = client['tjj']
    m_page = page.replace('www','m')
    
    str_start_date = (datetime.datetime.now()-datetime.timedelta(hours=days*24-1)).strftime('%Y%m%d%H')+'0000'

    hours = __fix_datetime_to_hours(str_start_date)
    hour_data = {}
    for i in hours:
        hour_data[i] = 0
    page_data = list(db.cc.find({'page':page}))+list(db.cc.find({'page':m_page}))
    #page_data = list(db.cc.find({'page':{'$in':[page,m_page]},'time':{'$gte':hours[0],'$lte':hours[-1]}}))
    print (datetime.datetime.now()-s_time).total_seconds()
    

    info_data = {}
    info_data['total_count'] = len(page_data)
    info_data['in_count'] = 0
    info_data['baidu_count'] = 0
    info_data['google_count'] = 0
    info_data['weibo_count'] = 0
    info_data['android_count'] = 0
    info_data['ios_count'] = 0
    info_data['m_count'] = 0
    info_data['weixin_count'] = 0
    for k in page_data:
        if k['last_page'] =='' or k['last_page'].find('huxiu.com')>=0:
            info_data['in_count'] += 1
        if k['last_page'].find('baidu') >= 0:
            info_data['baidu_count'] += 1
        if k['last_page'].find('google') >= 0:
            info_data['google_count'] += 1
        if k['last_page'].find('weibo') >= 0:
            info_data['weibo_count'] += 1
        if k['user_agent'].find('Android') >= 0:
            info_data['android_count'] += 1
        if k['user_agent'].find('iPhone') >= 0 or k['user_agent'].find('iPad') >= 0:
            info_data['ios_count'] += 1
        if k['page'].find('m.huxiu.com') >= 0:
            info_data['m_count'] += 1
        if k['user_agent'].find('MicroMessenger') >= 0:
            info_data['weixin_count'] += 1

        if type == 'total' and hour_data.has_key(k['time'][0:10]+'0000'):
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'in' and hour_data.has_key(k['time'][0:10]+'0000') and (k['last_page'] =='' or k['last_page'].find('huxiu.com')>=0):
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'baidu' and hour_data.has_key(k['time'][0:10]+'0000') and k['last_page'].find('baidu') >= 0:
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'google' and hour_data.has_key(k['time'][0:10]+'0000') and k['last_page'].find('google') >= 0:
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'weibo' and hour_data.has_key(k['time'][0:10]+'0000') and k['last_page'].find('weibo') >= 0:
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'android' and hour_data.has_key(k['time'][0:10]+'0000') and k['user_agent'].find('Android') >= 0:
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'ios' and hour_data.has_key(k['time'][0:10]+'0000') and (k['user_agent'].find('iPhone') >= 0 or k['user_agent'].find('iPad') >= 0):
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'm' and hour_data.has_key(k['time'][0:10]+'0000') and k['page'].find('m.huxiu.com') >= 0:
            hour_data[k['time'][0:10]+'0000'] += 1
        if type == 'weixin' and hour_data.has_key(k['time'][0:10]+'0000') and k['user_agent'].find('MicroMessenger') >= 0:
            hour_data[k['time'][0:10]+'0000'] += 1
    info_data['pre_hour_data'] = [{'time':key,'count':value}for key,value in hour_data.items()]
    print (datetime.datetime.now()-s_time).total_seconds()
    client.close()
    return info_data

def find_page_static(page,type='total'):
    now_time = datetime.datetime.now()
    info_data = {}
    s_time = datetime.datetime.now()
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    client.the_database.authenticate('huxiu','huxiu@123',source='admin')
    db = client['tjj']

    m_page = page.replace('www','m')
    p_page_data = list(db.cc.find({'page':page}))
    m_page_data = list(db.cc.find({'page':m_page}))


    m_weixin_data = list(db.cc.find({'page':m_page.split('/1.html')[0]+'?f=weixinmenu'}))
    m_weibo_data = list(db.cc.find({'page':m_page+'?url_type=39&object_type=webpage&pos=1'}))
    m_chouti_data = list(db.cc.find({'page':m_page+'?f=chouti'}))
    p_chouti_data = list(db.cc.find({'page':page+'?f=chouti'}))
    m_wangzhan_data = list(db.cc.find({'page':m_page+'?f=wangzhan'}))+list(db.cc.find({'page':m_page+'?from=timeline&isappinstalled=0'}))
    p_wangzhan_data = list(db.cc.find({'page':page+'?f=wangzhan'}))
    m_xianguo_data = list(db.cc.find({'page':m_page+'?f=xianguo'}))
    p_xianguo_data = list(db.cc.find({'page':page+'?f=xianguo'}))

    #print '搜索时间',(datetime.datetime.now()-now_time).total_seconds()

    page_data = p_page_data+p_wangzhan_data
    m_page_data = m_page_data+m_weixin_data+m_weibo_data+m_chouti_data+m_xianguo_data+m_wangzhan_data
    total_page_data = page_data+m_page_data+p_chouti_data+p_xianguo_data

    hours = __fix_datetime_to_hours((datetime.datetime.now()-datetime.timedelta(hours=24)).strftime('%Y%m%d%H')+'0000')
    hour_pv_data = {}
    hour_uv_data = {}
    for i in hours:
        hour_pv_data[i] = 0
        hour_uv_data[i] = []

    huxiu_url = ['www.huxiu.com','www.huxiu.com/focus','www.huxiu.com/opinions','www.huxiu.com/book','www.huxiu.com/products','www.huxiu.com/tags','www.huxiu.com/photo','www.huxiu.com/collections','www.huxiu.com/article']
    sou_url = ['www.baidu.com','news.baidu.com','m.baidu.com','zhidao.baidu.com','baike.baidu.com','www.so.com','j.news.so.com','www.sougou.com','www.google.com','www.google.com.hk','cn.bing.com']
    news_url = ['sh.qihoo.com','news.baidu.com','news.so.com','yule.baidu.com','internet.baidu.com','jian.news.baidu.com','www.hao123.com','dig.chouti.com','www.xianguo.com','mail.qq.com','set3.mail.qq.com','set1.mail.qq.com','www.toutiao.com','web.toutiao.com','nativeapp.toutiao.com','m.toutiao.com','i.maxthon.com','mail.163.com','www.inoreader.com','tb10.kuku98.com','offlintab.firefoxchina.cn','expo.bootcss.com','digg.com','www.duba.com','www.techweb.com.cn','news.sogou.com','www.qufenqi.com','feedly.com']
    sj_url = ['weibo.com','www.weibo.com','s.weibo.com','mp.weixin.qq.com','user.qzone.qq.com','openapi.qzone.qq.com','www.zhihu.com','www.bjdvd.org','t.wondershare.cn']
    
    #虎嗅站内访问
    huxiu_url_data = {}
    for k in huxiu_url:
        huxiu_url_data[k] = 0
    huxiu_url_data['other'] = 0

    #搜索引擎访问
    sou_url_data = {}
    for k in sou_url:
        sou_url_data[k] = 0

    #新闻站访问数
    news_url_data = {}
    for k in news_url:
        news_url_data[k] = 0

    #社交网站访问数
    sj_url_data = {}
    for k in sj_url:
        sj_url_data[k] = 0

    #所有的其他访问
    other = 0
    #直接访问
    direct = 0

    #a_count = 0
    for k in total_page_data:
    #    a_count += 1
        if hour_pv_data.has_key(k['time'][0:10]+'0000'):
            hour_pv_data[k['time'][0:10]+'0000'] += 1
            hour_uv_data[k['time'][0:10]+'0000'].append(k['cookie'])
    out_page_rank = 0
    #print a_count
    for k in page_data:
        last_page = k['last_page']
        
        page = k['page']
        m_last_page = last_page.replace('www','m')
        if m_last_page == page:
            out_page_rank += 1

        if last_page == "":
            direct += 1
        else:
            uri_last_page = last_page.split('/')[2]
            if uri_last_page.find('huxiu.com')>=0:
                last_page_p = last_page.split('/')
                try:
                    if last_page_p[3].find('focus') >= 0:
                        if uri_last_page == 'www.huxiu.com':
                            last_page = 'www.huxiu.com/focus'
                        #else:
                        #    last_page = 'm.huxiu.com'
                    else:
                        if uri_last_page == 'www.huxiu.com':
                            if last_page_p[3] != '':
                                last_page = 'www.huxiu.com/'+last_page_p[3]
                            #else:
                            #    last_page = 'www.huxiu.com'
                        else:
                            if last_page_p[3] != '':
                                last_page = 'm.huxiu.com/'+last_page_p[3]
                            #else:
                            #    last_page = 'm.huxiu.com'
                except:
                    if uri_last_page == 'www.huxiu.com':
                        last_page = 'www.huxiu.com'
                    #else:
                    #    last_page = 'm.huxiu.com'

                if last_page in huxiu_url:
                    huxiu_url_data[last_page] += 1
                else:
                    huxiu_url_data['other'] += 1
            else:
                if uri_last_page in sou_url:
                    sou_url_data[uri_last_page] += 1
                elif uri_last_page in sj_url:
                    sj_url_data[uri_last_page] += 1
                elif uri_last_page in news_url:
                    if uri_last_page.find('news.baidu.com') >= 0:
                        if last_page == 'http://news.baidu.com/':
                            news_url_data['news.baidu.com'] += 1
                        else:
                            news_url_data[uri_last_page] += 1
                    else:
                        news_url_data[uri_last_page] += 1
                else:
                    other += 1

    news_url_data['dig.chouti.com'] += len(p_chouti_data)
    news_url_data['www.xianguo.com'] += len(p_xianguo_data)

    sou_url_data['news.baidu.com'] = sou_url_data['news.baidu.com']-news_url_data['news.baidu.com']
    
    info_data['huxiu_rank'] = [{'url':key,'count':value}for key,value in huxiu_url_data.items()]
    info_data['sou_rank'] = [{'url':key,'count':value}for key,value in sou_url_data.items()]
    info_data['news_rank'] = [{'url':key,'count':value}for key,value in news_url_data.items()]
    info_data['sj_rank'] = [{'url':key,'count':value}for key,value in sj_url_data.items()]
    
    info_data['pv_data_by_hour'] = [{'time':key,'count':value}for key,value in hour_pv_data.items()]
    info_data['uv_data_by_hour'] = [{'time':key,'count':len(set(value))}for key,value in hour_uv_data.items()]
    
    info_data['tatal_rank'] = [
        {'count':sum([value for key,value in huxiu_url_data.items()])+out_page_rank,'name':u'站内跳转'},
        {'count':len(m_page_data),'name':'M端'},
        {'count':direct,'name':u'直接访问'},
        {'count':sum([value for key,value in sou_url_data.items()]),'name':u'搜索'},
        {'count':sum([value for key,value in news_url_data.items()]),'name':u'资讯站'},
        {'count':sum([value for key,value in sj_url_data.items()]),'name':u'社交'},
        {'count':other,'name':u'其他'}
    ]

    
    #print '整理数据时间',(datetime.datetime.now()-now_time).total_seconds()
    #count = 0
    #for k in info_data['tatal_rank']:
    #    count += k['count']
    #print count
    return info_data

#if __name__ == '__main__':
#    find_page_static('http://www.huxiu.com/article/105959/1.html','total')



