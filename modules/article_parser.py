"""
기사 파싱 모듈
기사 URL로부터 제목, 본문, 이미지 등을 추출
"""
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import validators


class ArticleParser:
    """기사 크롤링 및 파싱 클래스"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse(self, url: str) -> dict:
        """
        기사 URL을 파싱하여 필요한 정보 추출
        
        Args:
            url: 기사 URL
            
        Returns:
            dict: {
                'url': 원본 URL,
                'title': 기사 제목,
                'content': 기사 본문,
                'summary': 기사 요약,
                'images': 이미지 URL 리스트,
                'keywords': 키워드 리스트,
                'category': 카테고리 (추정)
            }
        """
        # URL 유효성 검사
        if not validators.url(url):
            raise ValueError("유효하지 않은 URL입니다")
        
        try:
            # newspaper3k 사용
            article = Article(url, language='ko')
            article.download()
            article.parse()
            article.nlp()
            
            # 이미지 추가 추출 (BeautifulSoup)
            images = self._extract_images(url)
            
            # 카테고리 추정
            category = self._estimate_category(article.title, article.text)
            
            return {
                'url': url,
                'title': article.title,
                'content': article.text,
                'summary': article.summary if article.summary else article.text[:300],
                'images': images,
                'keywords': article.keywords[:5] if article.keywords else [],
                'category': category,
                'publish_date': str(article.publish_date) if article.publish_date else None
            }
            
        except Exception as e:
            raise Exception(f"기사 파싱 중 오류 발생: {str(e)}")
    
    def _extract_images(self, url: str) -> list:
        """기사 내 이미지 URL 추출"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            images = []
            
            # article 태그 내 이미지 우선
            article_tag = soup.find('article') or soup.find('div', class_=['article', 'content', 'post'])
            
            if article_tag:
                img_tags = article_tag.find_all('img')
            else:
                img_tags = soup.find_all('img')
            
            for img in img_tags:
                src = img.get('src') or img.get('data-src')
                if src:
                    # 상대 경로 처리
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        from urllib.parse import urljoin
                        src = urljoin(url, src)
                    
                    # 크기 필터 (너무 작은 이미지 제외)
                    width = img.get('width')
                    if width and int(width) < 200:
                        continue
                    
                    images.append(src)
            
            return images[:10]  # 최대 10개
            
        except Exception as e:
            print(f"이미지 추출 중 오류: {e}")
            return []
    
    def _estimate_category(self, title: str, content: str) -> str:
        """기사 카테고리 추정 (간단한 키워드 기반)"""
        text = (title + ' ' + content).lower()
        
        # 카테고리별 키워드
        categories = {
            'breaking_news': ['속보', '긴급', '발생', '검찰', '경찰', '정치', '국회', '대통령'],
            'economy': ['경제', '주식', '부동산', 'it', '기업', '금융', '시장', '투자'],
            'lifestyle': ['문화', '생활', '여행', '음식', '패션', '건강', '맛집', '영화']
        }
        
        scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[category] = score
        
        # 가장 높은 점수의 카테고리 반환
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return 'breaking_news'  # 기본값


if __name__ == '__main__':
    # 테스트
    parser = ArticleParser()
    
    # 테스트 URL (실제 사용 시 변경 필요)
    test_url = "https://www.segye.com/newsView/20240101000001"
    
    try:
        result = parser.parse(test_url)
        print("파싱 결과:")
        print(f"제목: {result['title']}")
        print(f"카테고리: {result['category']}")
        print(f"키워드: {result['keywords']}")
        print(f"이미지 개수: {len(result['images'])}")
        print(f"본문 길이: {len(result['content'])} 자")
    except Exception as e:
        print(f"테스트 실패: {e}")
