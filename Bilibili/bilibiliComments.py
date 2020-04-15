#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Function:
	Bilibili评论爬虫
Author:
	Li Xingqian
'''

import requests
import re
import os
import sys
import json
import pandas as pd
import pickle
import time
import xlsxwriter

# B站API详情 https://github.com/Vespa314/bilibili-api/blob/master/api.md

# 评论用户及其信息
info_list = []


# 获取一个AV号视频下所有评论
def getAllCommentList(item):
    url = "http://api.bilibili.com/x/reply?type=1&oid=" + str(item) + "&pn=1&nohot=1&sort=0"
    r = requests.get(url)
    numtext = r.text
    json_text = json.loads(numtext)
    commentsNum = json_text["data"]["page"]["count"]
    page = commentsNum // 20 + 2
    print(f"所有评论共计{page}页{commentsNum}条")
    #page = 2
    for n in range(1,page):
        url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn="+str(n)+"&type=1&oid="+str(item)+"&sort=2&nohot=1"
        req = requests.get(url)
        text = req.text
        try:
            json_text_list = json.loads(text)
            print(f"正在爬取第 {n} 页 ")
            num=0
            vip = ["无","大会员","年度大会员"]
            for i in json_text_list["data"]["replies"]:
                num += 1 
                #print(f"  已获取 第{n}页 第{num}条评论")
                info_list.append([
            				  "一级评论",
            	              i["member"]["uname"],
                              i["content"]["message"],
                              i["like"],
                              i["rcount"],
                              time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i["ctime"])),
                              i["member"]["sex"],
                              i["member"]["sign"],
                              i["member"]["level_info"]["current_level"],
                              vip[i["member"]["vip"]["vipType"]]
                              ])
                if i["replies"]:
                    page_sub = i["rcount"] // 10 + 2
                    print(f"    开始爬取 第{n}页第{num}条 子评论")
                    for m in range(1,page_sub):
                        url_sub = "https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn="+str(m)+"&type=1&oid="+str(item)+"&ps=10&root="+str(i["rpid"])
                        req_sub = requests.get(url_sub)
                        text_sub = req_sub.text
                        json_text_list_sub = json.loads(text_sub)
                        num_sub=0
                        for j in json_text_list_sub["data"]["replies"]:
                            num_sub += 1 
                            #print(f"      已获取 第{m}页 第{num_sub}条 子评论")
                            info_list.append([
            				                 "二级评论",
            	                             j["member"]["uname"],
                                             j["content"]["message"],
                                             j["like"],
                                             j["rcount"],
                                             time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(j["ctime"])),
                                             j["member"]["sex"],
                                             j["member"]["sign"],
                                             j["member"]["level_info"]["current_level"],
                                             vip[j["member"]["vip"]["vipType"]]
                              ])
                        
        
        except:
            pass

    time.sleep(0.3)


    return info_list
     

def saveCSVData(data,savename):
	df = pd.DataFrame(data, columns=['评论等级','评论人网名','评论内容','点赞数','回复数','评论时间','评论人性别','评论人个性签名','评论人账户等级','评论人是否会员'])
	#df = df.drop_duplicates()
	print("正在保存数据")
	df.to_csv(f'./csv/{out_filename}.csv', index=True)
    #df.to_excel(f'./xlsx/{out_filename}.xlsx', index=True)
	try:
		bb = pd.ExcelWriter(f'./xlsx/{out_filename}.xlsx', engine='xlsxwriter')
		df.to_excel(bb, sheet_name='comments')
		bb.save()
		return True
	except Exception as e:
		raise e
	


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Bilibili comments spider")
	parser.add_argument('-i', dest='oid', help='Bilibili oid',default='2076781')
	parser.add_argument('-o', dest='csv_out', help='csv format file out name', default='results')
	args = parser.parse_args()
	oid = args.oid
	out_filename = args.csv_out

	if not oid or not out_filename :
		raise ValueError('argument error')

	info_list.clear()
	info_list = getAllCommentList(oid)
	print(f"已爬取到数据共计{len(info_list)}条")
	if saveCSVData(info_list,out_filename):
		print(f"CSV已经保存数据到: csv/{out_filename}.csv")
		print(f"XLSX已经保存数据到: xlsx/{out_filename}.xlsx")

