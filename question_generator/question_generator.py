"""
Question Generator module using OpenAI API.
Generates relevant Chinese questions for articles.
"""

from openai import OpenAI
from typing import List, Dict, Any
from .config import Config
from .utils import extract_article_content, validate_article_structure

class QuestionGenerator:
    """Handles question generation using OpenAI API."""
    
    def __init__(self):
        """Initialize the question generator with OpenAI API key."""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
    
    def generate_questions_for_article(self, article: Dict[str, Any]) -> List[str]:
        """Generate questions for a single article."""
        if not validate_article_structure(article):
            return []
        
        content = extract_article_content(article)
        if not content:
            return []
        
        title = article.get('title', '')
        
        # Create the prompt for question generation
        prompt = self._create_question_prompt(title, content)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的教育内容分析师，专门为留学相关的文章生成高质量的中文问题。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                n=1
            )
            
            # Extract and parse the generated questions
            questions_text = response.choices[0].message.content.strip()
            questions = self._parse_questions(questions_text)
            
            return questions[:Config.QUESTIONS_PER_ARTICLE]
            
        except Exception as e:
            print(f"❌ Error generating questions: {e}")
            return []
    
    def _create_question_prompt(self, title: str, content: str) -> str:
        """Create a prompt for question generation."""
        return f"""
请为以下留学相关文章生成{Config.QUESTIONS_PER_ARTICLE}个高质量的中文问题。

文章标题：{title}

文章内容：
{content}

要求：
1. 问题必须用简体中文
2. 问题应该涵盖不同难度层次（基础、中级、高级）
3. 问题类型应该多样化：
   - 事实性问题（关于具体数据、费用、要求等）
   - 比较性问题（对比不同选项、地区、学校等）
   - 实用性问题（如何申请、准备、操作等）
   - 分析性问题（为什么、影响、趋势等）
4. 问题应该具体、明确，避免过于宽泛
5. 问题应该对读者有实际价值

请直接返回问题列表，每个问题一行，不要添加编号或其他格式。
"""
    
    def _parse_questions(self, questions_text: str) -> List[str]:
        """Parse the generated questions from the API response."""
        questions = []
        lines = questions_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Remove common prefixes like numbers, dashes, etc.
            line = line.lstrip('0123456789.-•* ')
            
            if line and len(line) > 5:  # Minimum question length
                questions.append(line)
        
        return questions
    
    def generate_questions_for_articles(self, articles: List[Dict[str, Any]]) -> Dict[int, List[str]]:
        """Generate questions for multiple articles."""
        results = {}
        
        for i, article in enumerate(articles):
            questions = self.generate_questions_for_article(article)
            if questions:
                results[i] = questions
        
        return results
