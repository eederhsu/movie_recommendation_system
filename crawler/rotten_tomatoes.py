import re
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup  



### Get movie List
movieUrlList = []
respMovieList = requests.get(url="http://www.rottentomatoes.com/top/bestofrt/?year=2015")
soupMovieList = BeautifulSoup(respMovieList.text, "lxml")
nn=0
for movieI in soupMovieList.find_all("a", {"class" : "unstyled articleLink", "target":"_top"}):
    nn+=1
    movieName = movieI.string
    movieUrl = movieI["href"]
    print(nn, movieName, movieUrl)
    movieUrlList.append(movieUrl)

rtUrl = "http://www.rottentomatoes.com"

def GetMovieInfo(page_url):
    


respMovieInfo = requests.get(url="%s/m/mad_max_fury_road/" %(rtUrl))
soupMovieInfo = BeautifulSoup(respMovieInfo.text, "lxml")

movieInfoA = soupMovieInfo.find("div", {"id" : "all-critics-numbers"})
movieInfoB = soupMovieInfo.find("div", {"class" : "panel panel-rt panel-box movie_info media"})


movie_Name      = soupMovieInfo.find("h1", {"class" : "title hidden-xs"}).contents[0][1:-1]
movie_In_Thea   = movieInfoB.find("td", {"itemprop" : "datePublished"}).contents[0][1:-1]
movie_Directed  = movieInfoB.find("td", {"itemprop" : "director"}).span.string
movie_runT      = movieInfoB.find("time", {"itemprop" : "duration"}).contents[0][1:-1]
movie_company   = movieInfoB.find("span", {"itemprop" : "productionCompany"}).contents[0]
movie_info_txt  = movieInfoB.find("div", {"id" : "movieSynopsis"}).contents[0][1:-1]
movie_tomatomer = movieInfoA.find("div", {"class" : "superPageFontColor"}).contents[2][1:-1]

print('QQ\n\n')
print(movie_Name)
print(movie_In_Thea)
print(movie_Directed)
print(movie_runT)
print(movie_company)
print(movie_info_txt)
print(movie_tomatomer)






# resp = requests.get(url="http://www.rottentomatoes.com/m/%s/reviews/?page=1&type=user&sort=" %("mad_max_fury_road"))
# soup = BeautifulSoup(resp.text, "lxml")

# for tag in soup.find_all("div",{"class" : "row review_table_row"}):
#     # tag.find
#     # push_tag = tag.find("div","scoreWapper")
#     userIDnum  = tag.a['href']
#     userID     = tag.find("a", "bold unstyled articleLink").string
#     content    = tag.find("div","user_review").contents[2]
#     contentLen = len(content)
#     ratingStar = tag.find("div","user_review").span['class'][0]
#     time = tag.find("span", "fr small subtle").string
#     # s_reviewer = 


#     print("\n")
#     print(userIDnum)
#     print(userID)
#     print(content)
#     print(contentLen)
#     print(ratingStar)
#     print(time)
#     # print(push_tag)
#     break



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


#             try:
#                 link = str(tag.find_all("a"))
#                 link = link.split("\"")
#                 link = "http://www.ptt.cc"+link[1]
#                 g_id = g_id+1
#                 parseGos(link,g_id)
#             except:
#                 pass
#         sleep(0.2)
#         page += 1
# def parseGos(link , g_id):
#     resp = requests.get(url=str(link),cookies={"over18":"1"})
#     soup = BeautifulSoup(resp.text)
#     # print(resp)
#     # author
#     author  = soup.find(id="main-container").contents[1].contents[0].contents[1].string.replace(' ', '')
#     # title
#     title = soup.find(id="main-container").contents[1].contents[2].contents[1].string.replace(' ', '')
#     # date
#     date = soup.find(id="main-container").contents[1].contents[3].contents[1].string
#     # ip
#     try:
#         ip = soup.find(text=re.compile("※ 發信站:"))
#         ip = re.search("[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*",str(ip)).group()
#     except:
#         ip = "ip is not find"
#     # content
#     a = str(soup.find(id="main-container").contents[1])
#     a = a.split("</div>")
#     a = a[4].split("<span class=\"f2\">※ 發信站: 批踢踢實業坊(ptt.cc),")
#     content = a[0].replace(' ', '').replace('\n', '').replace('\t', '')
#     # message
#     num , all , g , b , n ,message = 0,0,0,0,0,{}
#     for tag in soup.find_all("div","push"):
#         num += 1
#         push_tag = tag.find("span","push-tag").string.replace(' ', '')
#         push_userid = tag.find("span","push-userid").string.replace(' ', '')
#         push_content = tag.find("span","push-content").string.replace(' ', '').replace('\n', '').replace('\t', '')
#         push_ipdatetime = tag.find("span","push-ipdatetime").string.replace('\n', '')

#         message[num]={"狀態":push_tag,"留言者":push_userid,"留言內容":push_content,"留言時間":push_ipdatetime}
#         if push_tag == '推 ':
#             g += 1
#         elif push_tag == '噓 ':
#             b += 1
#         else:
#             n += 1          
#     messageNum = {"g":g,"b":b,"n":n,"all":num}
#     # json-data
#     d={ "a_ID":g_id , "b_作者":author , "c_標題":title , "d_日期":date , "e_ip":ip , "f_內文":content , "g_推文":message, "h_推文總數":messageNum }
#     json_data = json.dumps(d,ensure_ascii=False,indent=4,sort_keys=True)+','
    
#     store(json_data) 
    
# def store(data):
#     with open('%s.json' %fileName, 'a') as f:
#         f.write(data)

# store('[') 

# crawler(int(sys.argv[1]),int(sys.argv[2]))


# store(']') 
# with open('%s.json' %fileName, 'r') as f:
#     p = f.read()
# with open('%s.json' %fileName, 'w') as f:
#     f.write(p.replace(',]',']'))
# print ('Total Error pages = %d' %errorpage)
