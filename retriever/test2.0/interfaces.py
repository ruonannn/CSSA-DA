"""
Retriever模块标准接口定义
用于支持并行开发 - 各成员按此接口开发，确保最终能完美集成

作者：组长
创建时间：2025-08-19
用途：让5个成员能够并行开发而不互相阻塞
"""

from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass
import numpy as np

# =============================================================================
# 数据结构定义 - 所有成员使用统一的数据格式
# =============================================================================

@dataclass
class QAItem:
    """标准问答数据项"""
    id: str
    question: str
    answer: str
    source: str = ""
    link: str = ""
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class SearchResult:
    """检索结果数据项"""
    qa_item: QAItem
    similarity_score: float
    rank: int

# =============================================================================
# 成员A：数据处理工程师接口
# =============================================================================

class IDataProcessor:
    """数据处理器接口 - 成员A实现"""
    
    def load_raw_data(self, file_path: str) -> List[Dict]:
        """
        加载原始数据文件
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            List[Dict]: 原始数据列表
            
        示例返回：
        [
            {"id": "001", "question": "...", "answer": "...", ...},
            {"id": "002", "question": "...", "answer": "...", ...}
        ]
        """
        raise NotImplementedError
    
    def clean_text(self, text: str) -> str:
        """
        清洗单个文本
        
        Args:
            text: 原始文本
            
        Returns:
            str: 清洗后的文本
            
        示例：
        输入："  墨尔本怎么坐公交车？？！  "
        输出："墨尔本怎么坐公交车？"
        """
        raise NotImplementedError
    
    def validate_qa_item(self, item: Dict) -> Tuple[bool, str]:
        """
        验证单个问答项
        
        Args:
            item: 问答数据项
            
        Returns:
            Tuple[bool, str]: (是否有效, 错误信息)
        """
        raise NotImplementedError
    
    def process_all_data(self, file_path: str) -> List[QAItem]:
        """
        处理所有数据的主函数
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            List[QAItem]: 处理后的标准问答数据
        """
        raise NotImplementedError

# =============================================================================
# 成员B：文本向量化工程师接口
# =============================================================================

class ITextVectorizer:
    """文本向量化器接口 - 成员B实现"""
    
    def preprocess_text(self, text: str) -> str:
        """
        预处理文本（分词、去停用词等）
        
        Args:
            text: 原始文本
            
        Returns:
            str: 预处理后的文本
            
        示例：
        输入："墨尔本怎么坐公交车？"
        输出："墨尔本 公交车"
        """
        raise NotImplementedError
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """
        训练向量化器并转换文本列表
        
        Args:
            texts: 文本列表
            
        Returns:
            np.ndarray: 向量矩阵，形状为(文本数, 特征数)
        """
        raise NotImplementedError
    
    def transform(self, text: str) -> np.ndarray:
        """
        转换单个文本为向量
        
        Args:
            text: 单个文本
            
        Returns:
            np.ndarray: 文本向量，形状为(特征数,)
        """
        raise NotImplementedError
    
    def get_feature_names(self) -> List[str]:
        """
        获取特征词汇表
        
        Returns:
            List[str]: 特征词汇列表
        """
        raise NotImplementedError
    
    def get_vector_dimension(self) -> int:
        """
        获取向量维度
        
        Returns:
            int: 向量维度数
        """
        raise NotImplementedError

# =============================================================================
# 成员C：相似度计算工程师接口
# =============================================================================

class ISimilarityCalculator:
    """相似度计算器接口 - 成员C实现"""
    
    def calculate_similarities(self, query_vector: np.ndarray, 
                             document_vectors: np.ndarray) -> np.ndarray:
        """
        计算查询向量与文档向量的相似度
        
        Args:
            query_vector: 查询向量，形状为(特征数,)
            document_vectors: 文档向量矩阵，形状为(文档数, 特征数)
            
        Returns:
            np.ndarray: 相似度数组，形状为(文档数,)
        """
        raise NotImplementedError
    
    def get_top_k_indices(self, similarities: np.ndarray, k: int) -> List[int]:
        """
        获取相似度最高的k个索引
        
        Args:
            similarities: 相似度数组
            k: 返回数量
            
        Returns:
            List[int]: 按相似度降序排列的索引列表
        """
        raise NotImplementedError
    
    def rank_results(self, qa_items: List[QAItem], similarities: np.ndarray, 
                    k: int) -> List[SearchResult]:
        """
        对结果进行排序并返回Top-K
        
        Args:
            qa_items: 问答数据列表
            similarities: 相似度数组
            k: 返回数量
            
        Returns:
            List[SearchResult]: 排序后的检索结果
        """
        raise NotImplementedError

# =============================================================================
# 成员D：存储管理工程师接口
# =============================================================================

class IStorageManager:
    """存储管理器接口 - 成员D实现"""
    
    def save_vectorizer(self, vectorizer: Any, file_path: str) -> bool:
        """
        保存向量化器
        
        Args:
            vectorizer: 向量化器对象
            file_path: 保存路径
            
        Returns:
            bool: 是否保存成功
        """
        raise NotImplementedError
    
    def load_vectorizer(self, file_path: str) -> Any:
        """
        加载向量化器
        
        Args:
            file_path: 文件路径
            
        Returns:
            Any: 向量化器对象
        """
        raise NotImplementedError
    
    def save_vectors(self, vectors: np.ndarray, file_path: str) -> bool:
        """
        保存向量矩阵
        
        Args:
            vectors: 向量矩阵
            file_path: 保存路径
            
        Returns:
            bool: 是否保存成功
        """
        raise NotImplementedError
    
    def load_vectors(self, file_path: str) -> np.ndarray:
        """
        加载向量矩阵
        
        Args:
            file_path: 文件路径
            
        Returns:
            np.ndarray: 向量矩阵
        """
        raise NotImplementedError
    
    def save_qa_data(self, qa_items: List[QAItem], file_path: str) -> bool:
        """
        保存问答数据
        
        Args:
            qa_items: 问答数据列表
            file_path: 保存路径
            
        Returns:
            bool: 是否保存成功
        """
        raise NotImplementedError
    
    def load_qa_data(self, file_path: str) -> List[QAItem]:
        """
        加载问答数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            List[QAItem]: 问答数据列表
        """
        raise NotImplementedError
    
    def cache_query_result(self, query: str, results: List[SearchResult]) -> None:
        """
        缓存查询结果
        
        Args:
            query: 查询文本
            results: 查询结果
        """
        raise NotImplementedError
    
    def get_cached_result(self, query: str) -> Optional[List[SearchResult]]:
        """
        获取缓存的查询结果
        
        Args:
            query: 查询文本
            
        Returns:
            Optional[List[SearchResult]]: 缓存的结果，如果没有则返回None
        """
        raise NotImplementedError

# =============================================================================
# 成员E：测试验证工程师接口
# =============================================================================

class ITestValidator:
    """测试验证器接口 - 成员E实现"""
    
    def test_data_loading(self, processor: IDataProcessor) -> Dict[str, Any]:
        """
        测试数据加载功能
        
        Args:
            processor: 数据处理器
            
        Returns:
            Dict[str, Any]: 测试结果报告
        """
        raise NotImplementedError
    
    def test_vectorization(self, vectorizer: ITextVectorizer) -> Dict[str, Any]:
        """
        测试向量化功能
        
        Args:
            vectorizer: 向量化器
            
        Returns:
            Dict[str, Any]: 测试结果报告
        """
        raise NotImplementedError
    
    def test_similarity_calculation(self, calculator: ISimilarityCalculator) -> Dict[str, Any]:
        """
        测试相似度计算功能
        
        Args:
            calculator: 相似度计算器
            
        Returns:
            Dict[str, Any]: 测试结果报告
        """
        raise NotImplementedError
    
    def test_storage_operations(self, storage: IStorageManager) -> Dict[str, Any]:
        """
        测试存储操作
        
        Args:
            storage: 存储管理器
            
        Returns:
            Dict[str, Any]: 测试结果报告
        """
        raise NotImplementedError
    
    def benchmark_end_to_end_performance(self, retriever) -> Dict[str, Any]:
        """
        端到端性能测试
        
        Args:
            retriever: 完整检索系统
            
        Returns:
            Dict[str, Any]: 性能测试报告
        """
        raise NotImplementedError
    
    def generate_test_report(self, test_results: Dict[str, Dict]) -> str:
        """
        生成测试报告
        
        Args:
            test_results: 各项测试结果
            
        Returns:
            str: 格式化的测试报告
        """
        raise NotImplementedError

# =============================================================================
# Mock实现 - 用于并行开发
# =============================================================================

class MockDataProcessor(IDataProcessor):
    """Mock数据处理器 - 供其他成员并行开发时使用"""
    
    def load_raw_data(self, file_path: str) -> List[Dict]:
        return [
            {"id": f"mock_{i:03d}", "question": f"测试问题{i}", 
             "answer": f"测试答案{i}", "tags": ["测试"]}
            for i in range(1, 11)  # 10条测试数据
        ]
    
    def clean_text(self, text: str) -> str:
        return text.strip()
    
    def validate_qa_item(self, item: Dict) -> Tuple[bool, str]:
        return True, ""
    
    def process_all_data(self, file_path: str) -> List[QAItem]:
        raw_data = self.load_raw_data(file_path)
        return [QAItem(id=item["id"], question=item["question"], 
                      answer=item["answer"], tags=item.get("tags", []))
                for item in raw_data]

class MockTextVectorizer(ITextVectorizer):
    """Mock文本向量化器"""
    
    def __init__(self, dimension: int = 100):
        self.dimension = dimension
        np.random.seed(42)  # 确保一致性
    
    def preprocess_text(self, text: str) -> str:
        return text.lower().strip()
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        return np.random.rand(len(texts), self.dimension)
    
    def transform(self, text: str) -> np.ndarray:
        return np.random.rand(self.dimension)
    
    def get_feature_names(self) -> List[str]:
        return [f"feature_{i}" for i in range(self.dimension)]
    
    def get_vector_dimension(self) -> int:
        return self.dimension

class MockSimilarityCalculator(ISimilarityCalculator):
    """Mock相似度计算器"""
    
    def calculate_similarities(self, query_vector: np.ndarray, 
                             document_vectors: np.ndarray) -> np.ndarray:
        # 简单的点积相似度
        return np.dot(document_vectors, query_vector)
    
    def get_top_k_indices(self, similarities: np.ndarray, k: int) -> List[int]:
        return np.argsort(similarities)[::-1][:k].tolist()
    
    def rank_results(self, qa_items: List[QAItem], similarities: np.ndarray, 
                    k: int) -> List[SearchResult]:
        top_indices = self.get_top_k_indices(similarities, k)
        results = []
        for rank, idx in enumerate(top_indices):
            results.append(SearchResult(
                qa_item=qa_items[idx],
                similarity_score=similarities[idx],
                rank=rank + 1
            ))
        return results

# =============================================================================
# 使用示例
# =============================================================================

def example_parallel_development():
    """示例：如何使用Mock实现进行并行开发"""
    
    # 成员B可以这样开发和测试向量化功能
    mock_processor = MockDataProcessor()
    qa_items = mock_processor.process_all_data("mock_data.json")
    
    # 使用自己实现的向量化器
    # vectorizer = MyTextVectorizer()  # 成员B的实现
    # vectors = vectorizer.fit_transform([item.question for item in qa_items])
    
    print("✅ 成员B可以独立开发向量化功能")
    
    # 成员C可以这样开发和测试相似度计算
    mock_vectorizer = MockTextVectorizer()
    mock_calculator = MockSimilarityCalculator()
    
    # calculator = MySimilarityCalculator()  # 成员C的实现
    # similarities = calculator.calculate_similarities(query_vec, doc_vecs)
    
    print("✅ 成员C可以独立开发相似度计算功能")

if __name__ == "__main__":
    example_parallel_development()
