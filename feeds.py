"""카테고리별 RSS 피드 목록.

피드를 추가/삭제하려면 이 파일만 수정하면 됩니다.
(2026-11 기준으로 응답을 확인한 주소들입니다.)

※ 한겨레는 브라우저가 아닌 User-Agent 요청을 403 으로 차단하므로 비활성화했습니다.
  사용하려면 한겨레의 이용 정책을 확인한 뒤 주석을 해제하세요.
"""

CATEGORIES = ["정치", "경제", "문화", "사회", "국제", "지역", "스포츠", "IT과학"]

# (언론사, 카테고리, RSS URL)
FEEDS: list[tuple[str, str, str]] = [
    # 정치
    ("연합뉴스", "정치", "https://www.yna.co.kr/rss/politics.xml"),
    #     ("한겨레", "정치", "https://www.hani.co.kr/rss/politics/"),
    ("경향신문", "정치", "https://www.khan.co.kr/rss/rssdata/politic_news.xml"),
    ("동아일보", "정치", "https://rss.donga.com/politics.xml"),
    ("조선일보", "정치", "https://www.chosun.com/arc/outboundfeeds/rss/category/politics/?outputType=xml"),
    ("SBS", "정치", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=01"),
    # 경제
    ("연합뉴스", "경제", "https://www.yna.co.kr/rss/economy.xml"),
    #     ("한겨레", "경제", "https://www.hani.co.kr/rss/economy/"),
    ("경향신문", "경제", "https://www.khan.co.kr/rss/rssdata/economy_news.xml"),
    ("동아일보", "경제", "https://rss.donga.com/economy.xml"),
    ("조선일보", "경제", "https://www.chosun.com/arc/outboundfeeds/rss/category/economy/?outputType=xml"),
    ("SBS", "경제", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=02"),
    # 문화
    ("연합뉴스", "문화", "https://www.yna.co.kr/rss/culture.xml"),
    #     ("한겨레", "문화", "https://www.hani.co.kr/rss/culture/"),
    ("경향신문", "문화", "https://www.khan.co.kr/rss/rssdata/culture_news.xml"),
    ("동아일보", "문화", "https://rss.donga.com/culture.xml"),
    ("조선일보", "문화", "https://www.chosun.com/arc/outboundfeeds/rss/category/culture-life/?outputType=xml"),
    ("SBS", "문화", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=08"),
    # 사회
    ("연합뉴스", "사회", "https://www.yna.co.kr/rss/society.xml"),
    #     ("한겨레", "사회", "https://www.hani.co.kr/rss/society/"),
    ("경향신문", "사회", "https://www.khan.co.kr/rss/rssdata/society_news.xml"),
    ("동아일보", "사회", "https://rss.donga.com/national.xml"),
    ("조선일보", "사회", "https://www.chosun.com/arc/outboundfeeds/rss/category/national/?outputType=xml"),
    ("SBS", "사회", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=03"),
    # 국제
    ("연합뉴스", "국제", "https://www.yna.co.kr/rss/international.xml"),
    #     ("한겨레", "국제", "https://www.hani.co.kr/rss/international/"),
    ("경향신문", "국제", "https://www.khan.co.kr/rss/rssdata/kh_world.xml"),
    ("동아일보", "국제", "https://rss.donga.com/international.xml"),
    ("조선일보", "국제", "https://www.chosun.com/arc/outboundfeeds/rss/category/international/?outputType=xml"),
    ("SBS", "국제", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=07"),
    # 지역
    ("연합뉴스", "지역", "https://www.yna.co.kr/rss/local.xml"),
    ("경향신문", "지역", "https://www.khan.co.kr/rss/rssdata/local_news.xml"),
    # 스포츠
    ("연합뉴스", "스포츠", "https://www.yna.co.kr/rss/sports.xml"),
    #     ("한겨레", "스포츠", "https://www.hani.co.kr/rss/sports/"),
    ("경향신문", "스포츠", "https://www.khan.co.kr/rss/rssdata/kh_sports.xml"),
    ("동아일보", "스포츠", "https://rss.donga.com/sports.xml"),
    ("조선일보", "스포츠", "https://www.chosun.com/arc/outboundfeeds/rss/category/sports/?outputType=xml"),
    ("SBS", "스포츠", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=09"),
    # IT과학
    #     ("한겨레", "IT과학", "https://www.hani.co.kr/rss/science/"),
    ("경향신문", "IT과학", "https://www.khan.co.kr/rss/rssdata/science_news.xml"),
    ("동아일보", "IT과학", "https://rss.donga.com/science.xml"),
    ("전자신문", "IT과학", "https://rss.etnews.com/Section901.xml"),
]
