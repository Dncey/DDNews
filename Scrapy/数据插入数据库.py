dict = {
    '科技':1,
    '娱乐':2,
    '游戏':3,
    '体育':4,
    '军事':5,
    '动漫':6,
    '新时代':7,
    '财经':8,
    '搞笑':9,
    '国际':10,
    '热文':11,
}
import json
import pymysql

def main():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', database='panda_new',charset='utf8')
    cursor = conn.cursor()

    sql ="""insert into tb_news(title,source,index_image_url,index_image_url_list,digest, content,report_time,digest_label,category_id,source_avatar_url ,create_time,update_time,clicks,status,reason,user_id,is_spider) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'2019-04-10','2019-04-10',0,0,'',1,1) """

    with open('/home/python/Desktop/Scrapy/Toutiaojson2.txt','r',encoding='utf-8')as f:

        new_info_str = '1'
        #插入数目
        count = 0
        while new_info_str:

            try:
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

                #如果简要标签的话提取前前15个字符串
                digest_label = str(new_dict['digest_label'][:15]) if new_dict['digest_label'] else 'null'
                count +=1

                cursor.execute(sql,(title,source,index_image_url,index_image_url_list,digest,content,report_time,digest_label,category,source_avatar_url))
                conn.commit()
            except Exception as e:
                print(e)
        print(count)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
