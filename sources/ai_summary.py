"""AI摘要生成模块"""
import re
from typing import List, Dict, Any

class SimpleSummarizer:
    """简单文本摘要器 - 无需外部API"""
    
    def __init__(self, max_length: int = 150):
        self.max_length = max_length
    
    def summarize(self, text: str, title: str = "") -> str:
        """生成文本摘要"""
        if not text or len(text) <= self.max_length:
            return text
        
        # 清理文本
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 提取关键句子 (简单启发式)
        sentences = re.split(r'(?<=[。！？.!?])\s+', text)
        
        if len(sentences) <= 2:
            return text[:self.max_length] + "..."
        
        # 评分句子重要性
        scored_sentences = []
        for i, sent in enumerate(sentences):
            score = self._score_sentence(sent, title)
            scored_sentences.append((score, i, sent))
        
        # 选择高分句子
        scored_sentences.sort(reverse=True)
        selected = scored_sentences[:2]
        selected.sort(key=lambda x: x[1])  # 按原文顺序排列
        
        summary = ' '.join([s[2] for s in selected])
        
        if len(summary) > self.max_length:
            summary = summary[:self.max_length].rsplit(' ', 1)[0] + "..."
        
        return summary
    
    def _score_sentence(self, sentence: str, title: str) -> float:
        """给句子打分"""
        score = 0.0
        sentence_lower = sentence.lower()
        
        # 长度因子 (中等长度优先)
        length = len(sentence)
        if 50 <= length <= 200:
            score += 1.0
        elif length > 200:
            score += 0.5
        
        # 位置因子 (开头句子更重要)
        # 由调用者控制
        
        # 关键词因子
        important_words = ['announced', 'launched', 'developed', 'achieved', 
                          '发布', '推出', '实现', '完成', '突破', '首次']
        for word in important_words:
            if word in sentence_lower:
                score += 0.5
        
        # 数字因子 (包含数据更可信)
        if re.search(r'\d+', sentence):
            score += 0.3
        
        # 与标题相关度
        if title:
            title_words = set(title.lower().split())
            sent_words = set(sentence_lower.split())
            overlap = len(title_words & sent_words)
            score += overlap * 0.2
        
        return score


class KeywordExtractor:
    """关键词提取器"""
    
    def __init__(self):
        self.stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', 
                         '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
                         '你', '会', '着', '没有', '看', '好', '自己', '这'}
    
    def extract(self, text: str, top_k: int = 5) -> List[str]:
        """提取关键词"""
        # 简单TF统计
        words = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z]+', text)
        word_freq = {}
        
        for word in words:
            word = word.lower()
            if len(word) < 2 or word in self.stopwords:
                continue
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 返回高频词
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:top_k]]


class ContentAnalyzer:
    """内容分析器"""
    
    def __init__(self):
        self.summarizer = SimpleSummarizer()
        self.keyword_extractor = KeywordExtractor()
    
    def analyze(self, title: str, content: str) -> Dict[str, Any]:
        """分析内容并返回结构化数据"""
        summary = self.summarizer.summarize(content, title)
        keywords = self.keyword_extractor.extract(title + " " + content)
        
        # 情感倾向 (简单规则)
        sentiment = self._analyze_sentiment(title + " " + content)
        
        # 重要性评分
        importance = self._score_importance(title, content)
        
        return {
            "summary": summary,
            "keywords": keywords,
            "sentiment": sentiment,
            "importance": importance
        }
    
    def _analyze_sentiment(self, text: str) -> str:
        """简单情感分析"""
        positive = ['突破', '成功', '首次', '创新', '领先', '打破', 'progress', 'success', 'breakthrough']
        negative = ['失败', '问题', '争议', '批评', 'delay', 'failure', 'issue', 'problem']
        
        p_count = sum(1 for w in positive if w in text.lower())
        n_count = sum(1 for w in negative if w in text.lower())
        
        if p_count > n_count:
            return "positive"
        elif n_count > p_count:
            return "negative"
        return "neutral"
    
    def _score_importance(self, title: str, content: str) -> float:
        """评估重要性"""
        score = 0.0
        text = (title + " " + content).lower()
        
        # 重要实体提及
        important_entities = ['openai', 'google', 'microsoft', 'nvidia', 'tesla', 'spacex',
                             'meta', 'anthropic', 'deepmind', '苹果', '谷歌', '微软', '英伟达',
                             'spacex', 'nasa', '发布', '收购', '融资', 'IPO', ' billion', '亿']
        
        for entity in important_entities:
            if entity in text:
                score += 0.5
        
        # 限制在0-5范围
        return min(5.0, max(0, score))
