from datetime import datetime

dict = {
    '科技':1,
    '娱乐':2,
    '游戏':3,
    '体育':4,
    '军事':5,
    '动漫':6,
    '财经':8,
    '搞笑':9,
    '国际':10,
}

user_id = [1,2,7,8,9,10,11,12,13,16,19,21,23]
import json
import pymysql
import random

def main():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', database='panda_new',charset='utf8')
    cursor = conn.cursor()
    now_date = datetime.now().strftime('%Y-%m-%d')

    sql ="""insert into tb_news(title,source,index_image_url,index_image_url_list,digest, content,report_time,digest_label,category_id,source_avatar_url ,create_time,update_time,clicks,status,reason,user_id,is_spider) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,0,'',%s,1) """

    with open('/home/python/Desktop/DDNews/Scrapy/Toutiao/news.txt','r+',encoding='utf-8')as f:

        new_info_str = '1'
        #插入数目
        count = 0
        while new_info_str:

            try:
                #获取读取数据的每一行数据
                new_info_str = f.readline()
                new_dict = json.loads(new_info_str)
                category = dict.get(new_dict['category'])
                if not category:
                    continue

                title = new_dict['title']
                source = new_dict['author']
                index_image_url = new_dict['index_url']
                index_image_url_list = new_dict['index_urls']
                digest = new_dict['digest']
                content = new_dict['content']
                source_avatar_url = new_dict['source_avatar_url']
                print(new_dict)
                report_time = new_dict['time']
                userid = random.choice(user_id)
                #如果关键字标签的话提取前前15个字符串
                digest_label = str(new_dict['digest_label'][:15]) if new_dict['digest_label'] else 'null'
                count +=1
                cursor.execute(sql,(title,source,index_image_url,index_image_url_list,digest,content,report_time,digest_label,category,source_avatar_url,now_date,now_date,userid))
                conn.commit()
            except Exception as e:
                print(e)
        print(count)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
