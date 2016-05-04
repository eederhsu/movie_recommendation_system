import re
import sys
import os
import json
import requests
from time import sleep
from bs4 import BeautifulSoup  

fileName = '2015top15_1'
movNum = 0

def crawler():
    print("==Start==")
    movieUrlList = []
    respMovieList = requests.get(url="http://www.rottentomatoes.com/top/bestofrt/?year=2015")
    soupMovieList = BeautifulSoup(respMovieList.text, "lxml")
    nn=0
    for movieI in soupMovieList.find_all("a", {"class" : "unstyled articleLink", "target":"_top"}):
        nn+=1
        movieName = movieI.string
        movieUrl = movieI["href"]
        print("%d %s %s" %(nn, movieName, movieUrl))
        movieUrlList.append(movieUrl)


    for movie_url in movieUrlList:
        GetMovieInfo(movie_url)



def GetMovieInfo(movie_url):
    global movNum
    movNum += 1

    # movie_url = "/m/mad_max_fury_road/"
    respMovieInfo = requests.get(url="http://www.rottentomatoes.com%s" %(movie_url))
    soupMovieInfo = BeautifulSoup(respMovieInfo.text, "lxml")

    movieInfoA = soupMovieInfo.find("div", {"id" : "all-critics-numbers"})
    movieInfoB = soupMovieInfo.find("div", {"class" : "panel panel-rt panel-box movie_info media"})


    movie_Name      = soupMovieInfo.find("h1", {"class" : "title hidden-xs"}).contents[0][1:]
    genre_store = []
    movie_Genre     = movieInfoB.find_all("span", {"itemprop" : "genre"})
    for d in movie_Genre:
        genre_store.append(d.contents[0])
    movie_In_Thea   = movieInfoB.find("td", {"itemprop" : "datePublished"}).contents[0][1:-1]
    movie_Directed  = movieInfoB.find("td", {"itemprop" : "director"}).span.string
    movie_runT      = movieInfoB.find("time", {"itemprop" : "duration"}).contents[0][1:-1]
    movie_company = ""
    if movieInfoB.find("span", {"itemprop" : "productionCompany"})!= None:
        movie_company   = movieInfoB.find("span", {"itemprop" : "productionCompany"}).contents[0]
    movie_info_txt  = movieInfoB.find("div", {"id" : "movieSynopsis"}).contents[0][1:-1]
    movie_tomatomer = movieInfoA.find("div", {"class" : "superPageFontColor"}).contents[2][1:-1]

    # print('\n\n===========movie info=============')
    if movie_Name.find('/'):
        movie_Name = movie_Name.replace('/','-')
    movieReviewerFile = open("%d. %s.txt" %(movNum, movie_Name),'a')
    print("%d %s %s %s" %(movNum, movie_Name, movie_In_Thea, movie_runT))
    # print(movie_In_Thea)
    # print(movie_Directed)
    # print(movie_runT)
    # print(movie_company)
    # print(movie_info_txt)
    # print(movie_tomatomer)


    ##### Reviewer info #####
    reviewerH_url = "http://www.rottentomatoes.com%sreviews/?page=1&type=user&sort=" %movie_url
    resp_rH = requests.get(url=reviewerH_url)
    soup_rH = BeautifulSoup(resp_rH.text, "lxml")

    total_num = soup_rH.find("span", {"class" : "pageInfo"}).string.replace('Page 1 of ', '')
    total_num = int(total_num)

    num, reviewerInfo = 0, {}
    for i in range(1,total_num+1):
        reviewerpage = "http://www.rottentomatoes.com%sreviews/?page=%d&type=user&sort=" %(movie_url, i)
        resp_page = requests.get(url=reviewerpage)
        soup_page = BeautifulSoup(resp_page.text, "lxml")
        if soup_page.find("div",{"class" : "row review_table_row"}) == None:
            print('Break\n')
            break

        for tag in soup_page.find_all("div",{"class" : "row review_table_row"}):
            num+=1
            # tag.find
            # push_tag = tag.find("div","scoreWapper")
            userIDnum  = tag.a['href']
            userID     = tag.find("a", "bold unstyled articleLink").string
            content    = tag.find("div","user_review").contents[2]
            movieReviewerFile.write("%s\n" %content)
            contentLen = len(content)
            ratingStar = tag.find("div","user_review").span['class'][0]
            time = tag.find("span", "fr small subtle").string            
            reviewerInfo[num] = {'userIDnum':userIDnum,'userID':userID,'content':content,'contentLen':contentLen,'ratingStar':ratingStar,'time':time}

            # print(userIDnum)
            print("\t%d\t%s\t%s" %(num, time, userID))
            # print(content)
            # print(contentLen)
            # print(ratingStar)
            # print(time)
            # print(push_tag)
            # break
    movie_Data = {'movie_Name':movie_Name,'movie_Genre':genre_store,'movie_In_Thea':movie_In_Thea,'movie_Directed':movie_Directed,'movie_runT':movie_runT,'movie_company':movie_company,'movie_info_txt':movie_info_txt,'movie_tomatomer':movie_tomatomer,'reviewers':reviewerInfo,'reviewerNum':num}
    json_data = json.dumps(movie_Data,ensure_ascii=False,indent=4,sort_keys=True)+','

    movieReviewerFile.close()
    store(json_data)

def store(data):
    with open('%s.json' %fileName , 'a') as f:
        f. write(data)


store('[')

crawler()

store(']')


# saveMovieList()
# GetMovieInfo('d')
# GetNumRevPage('d')
'''
參考網站： 
http://beautifulsoup.readthedocs.org/zh_CN/latest/
http://www.rottentomatoes.com/m/mad_max_fury_road/reviews/?page=1&type=user&sort=
http://www.rottentomatoes.com/top/bestofrt/?year=2015

    •   電影名稱
    •   上映日期
    •   電影播放時間
    •   Directed by:
    •   電影爛番茄指數
    •   reviewer 數量
    •   MOVIE INFO 介紹
    •   每個評價人
        ⁃   名字
        ⁃   內容
        ⁃   字數
        ⁃   評價(給幾顆星)
        ⁃   評論時間
        ⁃   是否為super reviewer


'''

