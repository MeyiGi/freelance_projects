from bs4 import BeautifulSoup
from src.utils import get_titles

def extract_posts(file_path) -> list:
    results = []
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    # try:
        ######################################################################################################
        # https://www.pinpointnews.co.kr/news/articleList.html?sc_sub_section_code=S2N14&view_type=sm
        if 'pinpointnews' in file_path:
            posts = soup.select("section#section-list ul li")
            for post in posts:
                title = post.select_one("h4 a").get_text(strip=True)
                description = post.select_one("p a").get_text(strip=True)
                results.append(title + "|" + description)

            print("pinpointnews:", len(results))

        ######################################################################################################
        # https://biz.heraldcorp.com/economy
        elif 'heraldcorp' in file_path:
            titles = soup.select("section.section_list p.news_title")
            descriptions = soup.select("section.section_list p.news_text")
            for title, description in zip(titles, descriptions):
                title = title.get_text(strip=True)
                description = description.get_text(strip=True)
                results.append(title + "|" + description)

            print("heraldcorp:", len(results))
        
        ######################################################################################################
        # https://www.widedaily.com/news/articleList.html?sc_section_code=S1N26&view_type=sm
        elif 'widedaily' in file_path:
            posts = soup.select("section.section-body section#section-list ul li")
            for post in posts:
                title = post.select_one("h2.titles a").get_text(strip=True)
                description = post.select_one("p.lead a").get_text(strip=True)
                results.append(title + "|" + description)

            print("widedaily:", len(results))

        ######################################################################################################
        # https://thebigdata.co.kr/list.php?ct=g0000 
        elif 'thebigdata' in file_path:
            posts = soup.select("div.mcon04_lt div.mclist01 ul li")
            for post in posts:
                title = post.select_one("div.e1 a").get_text(strip=True)
                description = post.select_one("div.e2 a").get_text(strip=True)
                results.append(title + "|" + description)

            print("thebigdata:", len(results))
        
        ######################################################################################################
        # https://www.gukjenews.com/news/articleList.html?view_type=sm
        elif 'gukjenews' in file_path:
            posts = soup.select("div#anchorCon section#section-list ul li")
            for post in posts:
                title = post.select_one("h4.titles a").get_text(strip=True)
                description = post.select_one("p a").get_text(strip=True)
                results.append(title + "|" + description)

            print("gukjenews:", len(results))
        
        ######################################################################################################
        # https://www.globalepic.co.kr/list.php?ct=g0200
        elif 'globalepic' in file_path:
            titles = soup.select(".e1")
            for title in titles:
                results.append(title.get_text(strip=True) + "|" + "no description")

            print("globalepic:", len(results))

        ######################################################################################################
        # https://www.financialpost.co.kr/news/articleList.html?view_type=sm
        elif 'financialpost' in file_path:
            posts = soup.select("ul.type2 li")
            for post in posts:
                title = post.select_one("h2.titles a").get_text(strip=True)
                description = post.select_one("p a").get_text(strip=True)
                results.append(title + "|" + description)

            print("financialpost:", len(results))
        
        ######################################################################################################
        # https://www.newspim.com/section/economy
        elif 'newspim' in file_path:
            titles = soup.select(".sec_headbox .subject a , .thumb+ .txt .subject a")
            for title in titles:
                title = title.get_text(strip=True)
                results.append(title + "|" + "no description")

            print("newspim:", len(results))
        
        ######################################################################################################
        # https://www.ggilbo.com/news/articleList.html?view_type=sm
        elif 'ggilbo' in file_path:
            posts = soup.select("section#section-list ul li")
            for post in posts:
                title = post.select_one("h4 a").get_text(strip=True)
                description = post.select_one("p").get_text(strip=True)
                results.append(title + "|" + description)

            print("ggilbo:", len(results))
                
        ######################################################################################################
        # https://www.smarttoday.co.kr/news/articleList.html?view_type=sm
        elif 'smarttoday' in file_path:
            posts = soup.select("section#section-list ul li")
            for post in posts:
                title = post.select_one("div.view-cont h2.titles a").get_text(strip=True)
                description = post.select_one("div.view-cont p.lead a").get_text(strip=True)
                results.append(title + "|" + description)

            print("smarttoday:", len(results))
        
        ######################################################################################################
        # https://www.finance-scope.com/article/list/scp_SC007000000
        elif 'finance-scope' in file_path:
            posts = soup.select("div#articleList div.img_mark_reporter")
            for post in posts:
                title = post.select_one("div.pick_ttl a").get_text(strip=True)
                results.append(title + "|" + "no description")

            print("finance-scope:", len(results))

        ######################################################################################################
        # https://www.paxetv.com/news/articleList.html?sc_section_code=S1N12&view_type=sm
        elif 'paxetv' in file_path:
            titles = soup.select(".list-titles strong")
            descriptions = soup.select(".list-summary .line-height-3-2x")
            for title, description in zip(titles, descriptions):
                title = title.get_text(strip=True)
                description = description.get_text(strip=True)
                results.append(title + "|" + description)

            print("paxetv:", len(results))
        
        ######################################################################################################
        # https://www.businesspost.co.kr/BP?command=mobile_list&sub=8
        elif 'businesspost' in file_path:
            titles = soup.select(".txtListTitle")
            for title in titles:
                title = title.get_text(strip=True)
                results.append(title + "|" + "no description")

            print("businesspost:", len(results))

        ######################################################################################################
        # https://biz.newdaily.co.kr/news/section.html?catid=all
        elif 'newdaily' in file_path:
            section = soup.find('section', class_='grid--2nd--column').find('article')
            titles = section.find('ul').find_all('li')
            descriptions = section.find('ul').find_all('li')
            for title, description in zip(titles, descriptions):
                title = title.select_one("h3 a").get_text(strip=True)
                description = description.select_one("p").get_text(strip=True)
                results.append(title + "|" + description)

            print("newdaily:", len(results))

        ######################################################################################################
        # https://g-enews.com/list.php?ct=g000000
        elif 'g-enews' in file_path:
            titles = soup.select(".l_lt .elip2")
            for title in titles:
                title = title.get_text(strip=True)
                results.append(title + "|" + "no description")

            print("g-enews:", len(results))

        ######################################################################################################
        # https://daily.hankooki.com/news/articleList.html?sc_sub_section_code=S2N13&view_type=sm
        elif 'hankooki' in file_path:
            sections = soup.find('section', class_='section-body').find('section', id='section-list').find('ul').find_all('li')
            for section in sections:
                title = section.find('h4').find('a').get_text(strip=True)
                description = section.find("p").find("a").get_text(strip=True)
                results.append(title + "|" + description)

            print("hankooki:", len(results))

        ######################################################################################################
        # https://news.mtn.co.kr/category-news/all
        elif 'mtn' in file_path:
            titles = soup.select("h3")
            descriptions = soup.select("li p:nth-child(2)")
            for title, description in zip(titles, descriptions):
                title = title.get_text(strip=True)
                description = description.get_text(strip=True)
                results.append(title + "|" + description)

            print("mtn:", len(results))

        ######################################################################################################
        # https://www.econonews.co.kr/news/articleList.html?view_type=sm
        elif 'econonews' in file_path:
            titles = soup.select(".titles a")
            descriptions = soup.select(".line-6x2 a")
            for title, description in zip(titles, descriptions):
                title = title.get_text(strip=True)
                description = description.get_text(strip=True)
                results.append(title + "|" + description)

            print("econonews:", len(results))

        ######################################################################################################
        # https://www.thelec.kr/news/articleList.html?sc_section_code=S1N8&view_type=sm
        elif 'thelec' in file_path:
            titles = soup.select(".list-titles strong")
            for title in titles:
                title = title.get_text(strip=True)
                return title + "|" + "no description"

            print("thelec:", len(results))

        ######################################################################################################
        # https://www.choicenews.co.kr/news/articleList.html?view_type=sm
        elif 'choicenews' in file_path:
            titles = soup.find('section', id='section-list').find('ul', class_='type2').find_all('li')
            descriptions = soup.find('section', id='section-list').find('ul', class_='type2').find_all('li')
            for title, description in zip(titles, descriptions):
                title = title.find('h4').find('a').get_text(strip=True)
                description = description.find('p').get_text(strip=True)
                results.append(title + "|" + description)

            print("choicenews:", len(results))

        ######################################################################################################
        # https://www.pointdaily.co.kr/news/articleList.html?view_type=sm
        elif 'pointdaily' in file_path:
            titles = soup.find('section', class_='section-body').find('section', id='section-list').find('ul').find_all('li')
            descriptions = soup.find('section', class_='section-body').find('section', id='section-list').find('ul').find_all('li')
            for title, description in zip(titles, descriptions):
                title = title.find('h4').find('a').get_text(strip=True)
                description = description.find('p').get_text(strip=True)
                results.append(title + "|" + description)

            print("pointdaily:", len(results))

        ######################################################################################################
        # https://www.nbntv.co.kr/news/articleList.html?view_type=sm
        elif 'nbntv' in file_path:
            titles = soup.find('div', id='sections').find('section', id='section-list').find('ul').find_all('li')
            descriptions = soup.find('div', id='sections').find('section', id='section-list').find('ul').find_all('li')
            for title, description in zip(titles, descriptions):
                title = title.find('h2').find('a').get_text(strip=True)
                description = description.find('h2').get_text(strip=True)
                results.append(title + "|" + description)

            print("nbntv:", len(results))

        ######################################################################################################
        # https://www.jbnews.com/news/articleList.html?view_type=sm
        elif 'jbnews' in file_path:
            titles = soup.find('div', id='sections').find('section', id='section-list').find('ul').find_all('li')
            descriptions = soup.find('div', id='sections').find('section', id='section-list').find('ul').find_all('li')
            for title, description in zip(titles, descriptions):
                title = title.find('h4').find('a').get_text(strip=True)
                description = description.find('p').get_text(strip=True)
                results.append(title + "|" + description)

            print("jbnews:", len(results))

        ######################################################################################################
        # https://www.techm.kr/news/articleList.html?view_type=sm
        elif 'techm' in file_path:
            titles = soup.find('div', id='sections').find('section', id='section-list').find('ul').find_all('li')
            posts = soup.select("section.tech-news div.item")
            for title in titles:
                title = title.find('h4').find('a').get_text(strip=True)
                results.append(title + "|" + "no description")

            print("techm:", len(results))

        ######################################################################################################
        # https://www.news2day.co.kr/
        elif 'news2day' in file_path:
            titles = soup.select(".item_box_hd h3")
            descriptions = soup.select(".item_box_hd .item_txt")
            for title, description in zip(titles, descriptions):
                title = title.get_text(strip=True)
                description = description.get_text(strip=True)
                results.append(title + "|" + description)

            print("news2day:", len(results))

        ######################################################################################################
        # https://www.dnews.co.kr/m_home/
        elif 'dnews' in file_path:
            titles = soup.select(".in , .title")
            for title in titles:
                title = title.get_text(strip=True)
                results.append(title + "|" + "no description")

            print("dnews:", len(results))

        ######################################################################################################
        # https://www.asiae.co.kr/list/economy
        elif 'asiae' in file_path:
            titles = soup.select(".txt_box a , .article_type strong")
            descriptions = soup.select(".desc")
            for title, description in zip(titles, descriptions):
                title = title.get_text(strip=True)
                description = description.get_text(strip=True)
                results.append(title + "|" + description)
            
            print("asiae:", len(results))

        ##############################################F########################################################
        # https://www.ajunews.com/economy
        elif 'ajunews' in file_path:
            posts = soup.select("ul.news_list li.news_item, .list_headline_txt ul li")
            for post in posts:
                title = post.select_one(".tit").get_text(strip=True)
                description = post.select_one(".lead").get_text(strip=True)
                results.append(title + "|" + description)
            
            print("ajunews:", len(results))
        
        ######################################################################################################
        # https://www.korea.kr/briefing/pressReleaseList.do
        elif 'www.korea' in file_path:
            posts = soup.select(".article_body .list_type ul li")
            for post in posts:
                title = post.select_one("strong").get_text(strip=True)
                description = post.select_one(".lead").get_text(strip=True)
                results.append(title + "|" + description)

            print("www.koreae:", len(results))

        ######################################################################################################
        # https://www2.korea.kr/briefing/policyBriefingList.do
        elif 'www2.korea' in file_path:
            posts = soup.select(".flex")
            for post in posts:
                title = post.get_text(strip=True)
                results.append(title + "|" + 'no description')
            
            print("ww2.koreae:", len(results))


        ######################################################################################################
        # https://www.slist.kr/news/articleList.html?page=1
        elif 'slist' in file_path:
            titles = soup.select(".replace-titles")
            for title in titles:
                title = title.get_text(strip=True)
                results.append(title + "|" + "no description")
            
            print("slist:", len(results))

        ######################################################################################################    
        # https://m.naver.com/
        elif 'naver' in file_path and "search" in file_path:
            titles = soup.select(".list_news a.news_tit")
            descriptions = soup.select(".list_news .bx .dsc_txt")
            for title, description in zip(titles, descriptions):
                link = title.get("href")
                title = title.get_text(strip=True)
                description = description.get_text(strip=True)
                results.append(title + "\n" + link + "|" + description)

            print("naver search:", len(results))

        elif "naver" in file_path:
            posts = soup.select(".nclicks\\(fls\\.list\\)")
            for post in posts:
                link = post.get("href")
                title = post.get_text(strip=True)
                results.append(title + "\n" + link + "|" + "no description")

            print("naver main:", len(results))

        elif "fnnews":
            titles = soup.select("#listArea .tit_thumb a")
            for title in titles:
                title = title.get_text(strip=True)
                results.append(title + "|" + "no description")

            print("fnnews:", len(results))

        return get_titles(results)

    # except Exception as e:
    #     return "none"