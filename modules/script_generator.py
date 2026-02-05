"""
스크립트 생성 모듈
기사 내용을 기반으로 인트로/본문/아웃트로 스크립트 생성
"""
import os
from openai import OpenAI
from config import OPENAI_API_KEY, SCRIPT_PROMPTS


class ScriptGenerator:
    """AI 기반 스크립트 생성 클래스"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            print("⚠️ OPENAI_API_KEY가 설정되지 않았습니다. 테스트 모드로 작동합니다.")
            self.client = None
        else:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def generate(self, article: dict) -> dict:
        """
        기사 정보로부터 전체 스크립트 생성
        
        Args:
            article: article_parser.parse()의 결과
            
        Returns:
            dict: {
                'intro': 인트로 멘트,
                'narration': 본문 나레이션 (문장 리스트),
                'outro': 아웃트로 멘트
            }
        """
        if not self.client:
            # 테스트 모드: 더미 데이터 반환
            return self._generate_dummy(article)
        
        try:
            # 인트로 생성
            intro = self._generate_intro(article)
            
            # 본문 나레이션 생성
            narration = self._generate_narration(article)
            
            # 아웃트로 생성
            outro = self._generate_outro()
            
            return {
                'intro': intro,
                'narration': narration,
                'outro': outro
            }
            
        except Exception as e:
            print(f"스크립트 생성 중 오류: {e}")
            return self._generate_dummy(article)
    
    def _generate_intro(self, article: dict) -> str:
        """인트로 멘트 생성 (5초 분량)"""
        prompt = SCRIPT_PROMPTS['headline'].format(
            title=article['title'],
            summary=article['summary']
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 뉴스 브리핑 전문 작가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_narration(self, article: dict) -> list:
        """본문 나레이션 생성 (50초 분량, 문장 단위 리스트)"""
        prompt = SCRIPT_PROMPTS['narration'].format(
            content=article['content'][:1000]  # 토큰 제한 고려
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 뉴스 브리핑 전문 작가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        narration_text = response.choices[0].message.content.strip()
        
        # 문장 단위로 분리
        sentences = [s.strip() for s in narration_text.split('.') if s.strip()]
        
        return sentences
    
    def _generate_outro(self) -> str:
        """아웃트로 멘트 생성 (5초 분량)"""
        # 아웃트로는 고정 멘트 사용
        return "구독과 좋아요로 더 많은 뉴스를 받아보세요"
    
    def _generate_dummy(self, article: dict) -> dict:
        """테스트용 더미 스크립트 생성"""
        print("⚠️ 테스트 모드: 더미 스크립트 사용")
        
        title = article.get('title', '제목 없음')
        content = article.get('content', '')
        
        # 본문을 적당히 나눔
        sentences = content.split('.')[:5]
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        
        if not sentences:
            sentences = [
                "이번 사건은 많은 관심을 받고 있습니다.",
                "관련 당국은 조사를 진행 중입니다.",
                "앞으로의 진행 상황을 지켜봐야 할 것 같습니다."
            ]
        
        return {
            'intro': f"속보입니다. {title[:30]}",
            'narration': sentences,
            'outro': "구독과 좋아요로 더 많은 뉴스를 받아보세요"
        }


if __name__ == '__main__':
    # 테스트
    generator = ScriptGenerator()
    
    test_article = {
        'title': '테스트 뉴스 제목',
        'summary': '이것은 테스트 요약입니다.',
        'content': '테스트 본문입니다. 첫 번째 문장입니다. 두 번째 문장입니다. 세 번째 문장입니다.'
    }
    
    scripts = generator.generate(test_article)
    print("생성된 스크립트:")
    print(f"인트로: {scripts['intro']}")
    print(f"본문: {scripts['narration']}")
    print(f"아웃트로: {scripts['outro']}")
