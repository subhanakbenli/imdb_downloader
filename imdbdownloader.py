import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import concurrent.futures

# DOWNLOAD MOVIES ON IMDb
def get_films(index):
        all_flm_list=[]
        start=datetime.datetime.now()
        url="http://www.imdb.com"
        categories=['drama','thriller','comedy','romance','News','Game-Show','Talk-Show','reality-tv','action','adventure','animation','biography','crime','family','fantasy',
'film-noir','history','horror','music','musical','mystery','sci-fi','sport','war','western']
        sort=categories[int(index)]
        next = True
        url_genre = url + "/search/title/?title_type=feature&genres={}&explore=genres".format(sort)
        count=0  
        while next==True:
            
            # connect to url
            response=requests.get(url_genre)
            html_icerigi=response.content
            soup=BeautifulSoup(html_icerigi,"html.parser")
            movies_informations=(soup.find_all("div",{"class":"lister-item-content"}))
            for flm_infos in zip(movies_informations):
                flm_infos = BeautifulSoup(str(flm_infos),"html.parser")

                # movie name
                flm_name = str(flm_infos.find("h3",{"class":"lister-item-header"}).find("a").text.strip())

                # movie date , movie number
                try:
                    date_name = (flm_infos.find("span",{"class":"lister-item-year text-muted unbold"}).text.strip().split(" "))
                    if len(date_name)>1:
                        flm_name = flm_name +"   "+date_name[0]
                        flm_date = date_name[1].replace("(","").replace(")","")
                    else:
                        _try1 = date_name[0].find("1")
                        _try2 = date_name[0].find("2")
                        if _try1 ==-1 and _try2==-1 :
                            flm_name = (flm_name +"   "+date_name[0])
                            flm_date = ("*not found")
                        else:
                            flm_date = date_name[0].replace("(","").replace(")","")
                except: flm_date="*failure"
                
                # duration
                try:
                    flm_duration = (flm_infos.find("span",{"class":"runtime"}))
                    if str(flm_duration) == "None":
                        flm_duration = "*not found"
                    else:
                        flm_duration = flm_duration.text.replace(" min","")
                except: flm_duration = "*failure"

                # certificate
                try:
                    flm_certificate = flm_infos.find("span",{"class":"certificate"})
                    if str(flm_certificate) == "None":
                        flm_certificate = "*not found"
                    else:
                        flm_certificate = flm_certificate.text
                except: flm_certificate = "*failure"

                # genres 
                try:   
                    flm_genres = (flm_infos.find("span",{"class":"genre"}))
                    if str(flm_genres) =="None":
                        flm_genres = "*not found"
                    else:
                        flm_genres = flm_genres.text.strip()
                except: flm_genres = "*failure"

                # imdb score 
                try:
                    flm_imdb = (flm_infos.find("div",{"class":"inline-block ratings-imdb-rating"}))
                    if str(flm_imdb) == "None":
                        flm_imdb = "*not found"
                    else :
                        flm_imdb =flm_imdb.text.strip()
                except: flm_imdb = "*failure"

                # votes and gross
                try:
                    votes_gross = flm_infos.find("p",{"class":"sort-num_votes-visible"})
                    if str(votes_gross) == "None":
                        flm_votes = "*not found"
                        flm_gross = "*not found"
                    else:
                        votes_gross = votes_gross.text.strip().replace("\n","")
                        _try1 = votes_gross.find("Votes")
                        _try2 = votes_gross.find("Gross")
                        if (_try1 != -1) and (_try2 != -1) :
                            votes_gross = votes_gross.split("|")
                            flm_votes = (votes_gross[0].split(":")[1])
                            flm_gross = (votes_gross[1].split(":")[1]).replace("$","").replace("M","")
                        elif (_try1 == -1) and (_try2 != -1):
                            flm_votes = "*not found"
                            flm_gross = votes_gross.split(":")[1].replace("$","").replace("M","")
                        elif (_try1 != -1) and (_try2 ==-1): 
                            flm_votes = votes_gross.split(":")[1]
                            flm_gross = "*not found"
                        else:
                            flm_votes = "*not found"
                            flm_gross = "*not found"
                except:
                    flm_votes = "*failure"
                    flm_gross = "*failure"

                # link
                try : 
                    flm_link = url + (flm_infos.find("a").get("href"))
                except: flm_link = "*failure" 

                # directors and stars of the movie
                try:
                    directors_stars = (flm_infos.find("p",{"class":""}))
                    if str(directors_stars) == "None":
                        flm_directors = "*not found"
                        flm_stars = "*not found"
                    else:
                        directors_stars = directors_stars.text.strip().replace("\n","")
                        _try1 = directors_stars.find("Director")
                        _try2 = directors_stars.find("Star")
                        if (_try1 != -1) and (_try2 != -1):
                            directors_stars = directors_stars.split("|")
                            flm_directors = directors_stars[0].split(":")[1]
                            flm_stars = directors_stars[1].split(":")[1]
                        elif (_try1 == -1) and (_try2 != -1):
                            flm_directors = "*not found"
                            flm_stars = directors_stars.split(":")[1]
                        elif (_try1 != -1) and (_try2 == -1):
                            flm_directors = directors_stars.split(":")[1]
                            flm_stars = "*not found"
                        else:
                            flm_directors = "*not found"
                            flm_stars = "*not found"
                except: 
                    flm_directors="*failure"
                    flm_stars="*failure"

                # add to list
                flm_data=[flm_name,flm_date,flm_certificate,flm_duration,flm_genres,flm_imdb,[flm_directors],[flm_stars],flm_votes,flm_gross,flm_link]
                all_flm_list.append(flm_data)
                count+=1

            # next page
            next_page = (soup.find("a",{"lister-page-next next-page"}))
            if str(next_page) == "None":
                next = False
            else:
                url_genre = (url+next_page.get("href"))
            if count%300==0:
                print(sort,count) 
        end=datetime.datetime.now()
        print(sort,count," is over.Download duration:",end-start)
        return all_flm_list

# ADD TO DATABASE
def add_database():
    print("""imdbdeki filmleri çekme programına hoş geldiniz. 
!! filmlerin bilgileri indirilirken programı kapatmayınız,
işlem süresi internet hızınıza göre değişir.(yaklaşık 7-10 saat),
işlemi başaltmak için "start" yazınız
çıkmak için herhangi bir tuşa basınız.""")
    entry=input(">>>")
    if entry.lower()=="start":
        print("işlem başlatıldı")
    else:
        print("çıkış yapılıyor")
        quit()

    # run simultaneously
    st=datetime.datetime.now()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        category_index=[no for no in range(22) ]
        data_list=executor.map(get_films,category_index)
        table_names=['Drama','Thriller','Comedy','Romance','News','GameShow','TalkShow','RealityTV','Action','Adventure','Animation','Biography','Crime','Family','Fantasy',
    'Filmnoir','History','Horror','Music','Musical','Mystery','Scifi','Sport','War','Western']
    
    # add everyone to database one by one 
    conn=sqlite3.connect("imdb.db")
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS AllMovies (Id integer NULL PRIMARY KEY AUTOINCREMENT,Film Text,Date Int,Certificate Text,Duration Int,Genres Text,Imdb Int,Directors Text,Stars Text,Votes Int,Gross[milion $] Int,Link Text)")
    conn.commit()
    for category_informations,table_name in zip(data_list,table_names):
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (Id integer NULL PRIMARY KEY AUTOINCREMENT,Film Text,Date Int,Certificate Text,Duration Int,Genres Text,Imdb Int,Directors Text,Stars Text,Votes Int,Gross[milion $] Int,Link Text)".format(table_name))        
        conn.commit()

        for movie_info in category_informations:
            # own category table
            cursor.execute("SELECT * FROM {} WHERE Link = ?".format(str(table_name)),(movie_info[10],))
            find_film=cursor.fetchall()
            if len(find_film)>0:
                continue               
            cursor.execute("INSERT INTO {} (Film,Date,Certificate,Duration,Genres,Imdb,Directors,Stars,Votes,Gross,Link) values(?,?,?,?,?,?,?,?,?,?,?)".format(table_name),(movie_info[0],movie_info[1],movie_info[2],movie_info[3],movie_info[4],movie_info[5],str(movie_info[6]),str(movie_info[7]),movie_info[8],movie_info[9],movie_info[10],))
            conn.commit()   
            # all movies table      
            cursor.execute("SELECT * FROM AllMovies WHERE Link = ?",(movie_info[10],))
            find_film=cursor.fetchall()
            if len(find_film)>0:
                continue
            cursor.execute("INSERT INTO AllMovies (Film,Date,Certificate,Duration,Genres,Imdb,Directors,Stars,Votes,Gross,Link) values(?,?,?,?,?,?,?,?,?,?,?)",(movie_info[0],movie_info[1],movie_info[2],movie_info[3],movie_info[4],movie_info[5],str(movie_info[6]),str(movie_info[7]),movie_info[8],movie_info[9],movie_info[10],))
            conn.commit()

        print(table_name)
    fnsh=datetime.datetime.now()
    print(fnsh-st)

if __name__== "__main__":
        add_database()
