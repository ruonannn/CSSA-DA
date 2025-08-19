"""
模块二：Retriever - 简化版语义检索模块
使用基础的scikit-learn和numpy实现

作者：ruonan (xrn zmy syl sly团队)
创建时间：2025-08-18
"""

import json
import numpy as np
from typing import List, Dict, Tuple
import os
import pickle
from dataclasses import dataclass
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import re

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RetrievalResult:
    """检索结果数据类"""
    question_id: str
    question: str
    answer: str
    source: str
    link: str
    tags: List[str]
    similarity_score: float

class SimpleRetriever:
    """
    简化版语义检索器（使用TF-IDF + 余弦相似度）
    
    功能：
    - 加载问答数据
    - 使用TF-IDF进行文本向量化
    - 执行基于余弦相似度的检索
    """
    
    def __init__(
        self, 
        data_path: str = "data/qa_clean_data.json",
        vectorizer_save_path: str = "retriever/tfidf_vectorizer.pkl",
        vectors_save_path: str = "retriever/question_vectors.pkl",
        id_mapping_save_path: str = "retriever/id_mapping.json"
    ):
        """初始化检索器"""
        self.data_path = data_path
        self.vectorizer_save_path = vectorizer_save_path
        self.vectors_save_path = vectors_save_path
        self.id_mapping_save_path = id_mapping_save_path
        
        self.qa_data = []
        self.vectorizer = None
        self.question_vectors = None
        self.id_to_data_mapping = {}
        
        logger.info(f"SimpleRetriever初始化完成")
    
    def preprocess_text(self, text: str) -> str:
        """文本预处理"""
        if not text:
            return ""
        
        # 去除特殊字符，保留中文、英文、数字
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', text)
        
        # 使用jieba分词
        words = jieba.cut(text.strip())
        
        # 过滤停用词和长度小于2的词
        filtered_words = [word for word in words if len(word.strip()) >= 2]
        
        return ' '.join(filtered_words)
    
    def load_data(self) -> bool:
        """加载问答数据"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.qa_data = json.load(f)
            
            # 创建ID到数据的映射
            for idx, item in enumerate(self.qa_data):
                self.id_to_data_mapping[idx] = item
            
            logger.info(f"成功加载 {len(self.qa_data)} 条问答数据")
            return True
            
        except Exception as e:
            logger.error(f"加载数据失败：{e}")
            return False
    
    def build_vectors(self):
        """构建问题向量"""
        # 预处理所有问题
        questions = [self.preprocess_text(item['question']) for item in self.qa_data]
        
        logger.info(f"开始构建TF-IDF向量，问题数量：{len(questions)}")
        
        # 创建TF-IDF向量化器
        self.vectorizer = TfidfVectorizer(
            max_features=5000,  # 最大特征数
            ngram_range=(1, 2),  # 使用1-gram和2-gram
            min_df=1,  # 最小文档频率
            max_df=0.8  # 最大文档频率
        )
        
        # 拟合并转换问题
        self.question_vectors = self.vectorizer.fit_transform(questions)
        
        logger.info(f"TF-IDF向量构建完成，特征维度：{self.question_vectors.shape}")
    
    def save_components(self):
        """保存向量化器和向量"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.vectorizer_save_path), exist_ok=True)
            
            # 保存TF-IDF向量化器
            with open(self.vectorizer_save_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            # 保存问题向量
            with open(self.vectors_save_path, 'wb') as f:
                pickle.dump(self.question_vectors, f)
            
            # 保存ID映射
            with open(self.id_mapping_save_path, 'w', encoding='utf-8') as f:
                json.dump(self.id_to_data_mapping, f, ensure_ascii=False, indent=2)
            
            logger.info("组件保存完成")
            
        except Exception as e:
            logger.error(f"保存失败：{e}")
            raise e
    
    def load_components(self) -> bool:
        """加载已保存的组件"""
        try:
            # 检查文件是否存在
            if not all(os.path.exists(path) for path in [
                self.vectorizer_save_path, 
                self.vectors_save_path, 
                self.id_mapping_save_path
            ]):
                logger.warning("组件文件不完整，需要重新构建")
                return False
            
            # 加载TF-IDF向量化器
            with open(self.vectorizer_save_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # 加载问题向量
            with open(self.vectors_save_path, 'rb') as f:
                self.question_vectors = pickle.load(f)
            
            # 加载ID映射
            with open(self.id_mapping_save_path, 'r', encoding='utf-8') as f:
                loaded_mapping = json.load(f)
                self.id_to_data_mapping = {int(k): v for k, v in loaded_mapping.items()}
            
            logger.info("组件加载完成")
            return True
            
        except Exception as e:
            logger.error(f"加载失败：{e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[RetrievalResult]:
        """执行语义检索"""
        try:
            # 预处理查询
            processed_query = self.preprocess_text(query)
            
            # 将查询转换为向量
            query_vector = self.vectorizer.transform([processed_query])
            
            # 计算余弦相似度
            similarities = cosine_similarity(query_vector, self.question_vectors).flatten()
            
            # 获取top-k结果的索引
            top_indices = np.argsort(similarities)[::-1][:k]
            
            # 构建结果
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:  # 只返回有相似度的结果
                    data_item = self.id_to_data_mapping[idx]
                    result = RetrievalResult(
                        question_id=data_item['id'],
                        question=data_item['question'],
                        answer=data_item['answer'],
                        source=data_item.get('source', ''),
                        link=data_item.get('link', ''),
                        tags=data_item.get('tags', []),
                        similarity_score=float(similarities[idx])
                    )
                    results.append(result)
            
            logger.info(f"检索完成，返回 {len(results)} 个结果")
            return results
            
        except Exception as e:
            logger.error(f"检索失败：{e}")
            return []
    
    def build(self, force_rebuild: bool = False):
        """构建完整的检索系统"""
        logger.info("开始构建SimpleRetriever系统...")
        
        # 1. 加载数据
        if not self.load_data():
            raise Exception("数据加载失败")
        
        # 2. 尝试加载已有的组件
        if not force_rebuild and self.load_components():
            logger.info("使用已有组件")
            return
        
        # 3. 构建向量
        self.build_vectors()
        
        # 4. 保存组件
        self.save_components()
        
        logger.info("SimpleRetriever系统构建完成！")


def test_retriever():
    """测试检索器功能"""
    # 初始化检索器
    retriever = SimpleRetriever()
    
    # 构建检索系统
    retriever.build()
    
    # 测试检索
    test_queries = [
        "墨尔本怎么坐公交车？",
        "如何使用Myki卡？",
        "学生乘车有优惠吗？",
        "墨尔本的交通工具有哪些？",
        "公共交通",
        "租房"
    ]
    
    print("\n" + "="*60)
    print("🚀 开始测试简化版语义检索功能")
    print("="*60)
    
    for query in test_queries:
        print(f"\n🔍 查询：{query}")
        print("-" * 40)
        
        results = retriever.search(query, k=3)
        
        if not results:
            print("   没有找到相关结果")
            continue
            
        for i, result in enumerate(results, 1):
            print(f"{i}. 📊 相似度: {result.similarity_score:.3f}")
            print(f"   ❓ 问题: {result.question}")
            print(f"   ✅ 答案: {result.answer}")
            print(f"   🏷️  标签: {result.tags}")
            if result.source:
                print(f"   📚 来源: {result.source}")
            print()


if __name__ == "__main__":
    test_retriever()
