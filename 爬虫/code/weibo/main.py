import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36 '
}
Cookie = 'SINAGLOBAL=8147786075675.765.1578269395935; UOR=login.taobao.com,weibo.com,www.google.com; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; login_sid_t=b54487dc995b804de39bb2ba68e040fe; cross_origin_proto=SSL; YF-V5-G0=8c4aa275e8793f05bfb8641c780e617b; _s_tentry=passport.weibo.com; wb_view_log=1536*8641.25; Apache=807621139898.1981.1585980783546; ULV=1585980783552:5:1:1:807621139898.1981.1585980783546:1584433489613; WBtopGlobal_register_version=3d5b6de7399dfbdb; SCF=AhK_39-x47N9DBo7Mx3ZO4cdK_l-nFzrJ_UfhDdHPYt29SATPkNdNh3kp4nqyfcxipb1040VhrBV0KcGYg481AY.; SUB=_2A25zjFXcDeRhGeBH4lYT9S7PyD2IHXVQ-MAUrDV8PUNbmtANLXHskW9NQYi0AkzHL0u8c-9TKvijRW5aQITpicjN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2aewaL9FnwlbXk5UvxK5i5JpX5K2hUgL.Foq41KBESK50e022dJLoIEBLxKqL1h-L1K-LxKnL1KqL1hqLxKnL12eL1KMLxKnL12qL12et; SUHB=0IIVUZ40EkOnI3; ALF=1586585611; SSOLoginState=1585980812; un=17609209703; wvr=6; wb_view_log_6994250331=1536*8641.25; YF-Page-G0=95d69db6bf5dfdb71f82a9b7f3eb261a|1586015049|1586014970; webim_unReadCount=%7B%22time%22%3A1586015052109%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A5%2C%22msgbox%22%3A0%7D'
url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4489984075719139&root_comment_max_id=166744210360&root_comment_max_id_type=0&root_comment_ext_param=&page=4&filter=hot&sum_comment_number=82&filter_tips_before=1&from=singleWeiBo&__rnd=1586015055315'
r = requests.get(url,headers=headers,Cookie=Cookie)
print(r.text)
