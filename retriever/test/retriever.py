"""
模块二：Retriever - 语义检索模块
模块目标：给定一个query提取k个可能的回答

作者：ruonan (xrn zmy syl sly团队)
创建时间：2025-08-18

功能：
1. 调用hugging face模型将json的问题encode成vector
2. 构建FAISS数据库
3. 使用FAISS内置功能retrieve k个最相近的问题
4. 找到对应的json并返还
"""

import json
import numpy as np
import torch
from typing import List, Dict, Tuple, Any
import os
import pickle
from dataclasses import dataclass
import logging

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

class Retriever:
    """
    语义检索器类
    
    功能：
    - 加载问答数据
    - 对问题进行向量编码
    - 构建FAISS索引
    - 执行语义检索
    """
    
    def __init__(
        self, 
        data_path: str = "data/qa_clean_data.json",
        model_name: str = "bert-base-chinese",
        index_save_path: str = "retriever/faiss_index.index",
        embeddings_save_path: str = "retriever/question_embeddings.pkl",
        id_mapping_save_path: str = "retriever/id_mapping.json"
    ):
        """
        初始化检索器
        
        Args:
            data_path: 问答数据文件路径
            model_name: 预训练模型名称
            index_save_path: FAISS索引保存路径
            embeddings_save_path: 向量嵌入保存路径
            id_mapping_save_path: ID映射保存路径
        """
        self.data_path = data_path
        self.model_name = model_name
        self.index_save_path = index_save_path
        self.embeddings_save_path = embeddings_save_path
        self.id_mapping_save_path = id_mapping_save_path
        
        # 初始化变量
        self.qa_data = []
        self.model = None
        self.tokenizer = None
        self.faiss_index = None
        self.question_embeddings = None
        self.id_to_data_mapping = {}
        
        logger.info(f"Retriever初始化完成，数据路径：{data_path}")
    
    def load_data(self) -> bool:
        """
        加载问答数据
        
        Returns:
            bool: 加载是否成功
        """
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
    
    def load_model(self):
        """
        加载预训练模型和分词器
        """
        try:
            # 这里我们先用简单的方法，后续可以替换为sentence-transformers
            from transformers import AutoTokenizer, AutoModel
            
            logger.info(f"正在加载模型：{self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            
            # 设置为评估模式
            self.model.eval()
            
            logger.info("模型加载完成")
            
        except Exception as e:
            logger.error(f"模型加载失败：{e}")
            raise e
    
    def encode_questions(self) -> np.ndarray:
        """
        对所有问题进行向量编码
        
        Returns:
            np.ndarray: 问题向量矩阵
        """
        questions = [item['question'] for item in self.qa_data]
        embeddings = []
        
        logger.info(f"开始编码 {len(questions)} 个问题...")
        
        with torch.no_grad():
            for i, question in enumerate(questions):
                if i % 50 == 0:
                    logger.info(f"编码进度：{i}/{len(questions)}")
                
                # 分词和编码
                inputs = self.tokenizer(
                    question, 
                    return_tensors='pt',
                    padding=True,
                    truncation=True,
                    max_length=512
                )
                
                # 获取模型输出
                outputs = self.model(**inputs)
                
                # 使用[CLS]标记的嵌入作为句子表示
                sentence_embedding = outputs.last_hidden_state[:, 0, :].squeeze()
                embeddings.append(sentence_embedding.numpy())
        
        self.question_embeddings = np.array(embeddings)
        logger.info(f"问题编码完成，向量维度：{self.question_embeddings.shape}")
        
        return self.question_embeddings
    
    def build_faiss_index(self):
        """
        构建FAISS索引
        """
        try:
            import faiss
            
            # 获取向量维度
            dimension = self.question_embeddings.shape[1]
            
            # 创建FAISS索引（使用内积搜索）
            self.faiss_index = faiss.IndexFlatIP(dimension)
            
            # 标准化向量（用于余弦相似度）
            normalized_embeddings = self.question_embeddings / np.linalg.norm(
                self.question_embeddings, axis=1, keepdims=True
            )
            
            # 添加向量到索引
            self.faiss_index.add(normalized_embeddings.astype('float32'))
            
            logger.info(f"FAISS索引构建完成，包含 {self.faiss_index.ntotal} 个向量")
            
        except Exception as e:
            logger.error(f"FAISS索引构建失败：{e}")
            raise e
    
    def save_index_and_embeddings(self):
        """
        保存FAISS索引和向量嵌入
        """
        try:
            import faiss
            
            # 确保目录存在
            os.makedirs(os.path.dirname(self.index_save_path), exist_ok=True)
            
            # 保存FAISS索引
            faiss.write_index(self.faiss_index, self.index_save_path)
            
            # 保存向量嵌入
            with open(self.embeddings_save_path, 'wb') as f:
                pickle.dump(self.question_embeddings, f)
            
            # 保存ID映射
            with open(self.id_mapping_save_path, 'w', encoding='utf-8') as f:
                json.dump(self.id_to_data_mapping, f, ensure_ascii=False, indent=2)
            
            logger.info("索引和嵌入保存完成")
            
        except Exception as e:
            logger.error(f"保存失败：{e}")
            raise e
    
    def load_index_and_embeddings(self) -> bool:
        """
        加载已保存的FAISS索引和向量嵌入
        
        Returns:
            bool: 加载是否成功
        """
        try:
            import faiss
            
            # 检查文件是否存在
            if not all(os.path.exists(path) for path in [
                self.index_save_path, 
                self.embeddings_save_path, 
                self.id_mapping_save_path
            ]):
                logger.warning("索引文件不完整，需要重新构建")
                return False
            
            # 加载FAISS索引
            self.faiss_index = faiss.read_index(self.index_save_path)
            
            # 加载向量嵌入
            with open(self.embeddings_save_path, 'rb') as f:
                self.question_embeddings = pickle.load(f)
            
            # 加载ID映射
            with open(self.id_mapping_save_path, 'r', encoding='utf-8') as f:
                loaded_mapping = json.load(f)
                # 将字符串键转换为整数键
                self.id_to_data_mapping = {int(k): v for k, v in loaded_mapping.items()}
            
            logger.info("索引和嵌入加载完成")
            return True
            
        except Exception as e:
            logger.error(f"加载失败：{e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[RetrievalResult]:
        """
        执行语义检索
        
        Args:
            query: 查询问题
            k: 返回的结果数量
            
        Returns:
            List[RetrievalResult]: 检索结果列表
        """
        try:
            # 对查询进行编码
            with torch.no_grad():
                inputs = self.tokenizer(
                    query,
                    return_tensors='pt',
                    padding=True,
                    truncation=True,
                    max_length=512
                )
                
                outputs = self.model(**inputs)
                query_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
            
            # 标准化查询向量
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            # 使用FAISS搜索
            similarities, indices = self.faiss_index.search(query_embedding, k)
            
            # 构建结果
            results = []
            for i, (similarity, idx) in enumerate(zip(similarities[0], indices[0])):
                if idx < len(self.qa_data):
                    data_item = self.id_to_data_mapping[idx]
                    result = RetrievalResult(
                        question_id=data_item['id'],
                        question=data_item['question'],
                        answer=data_item['answer'],
                        source=data_item.get('source', ''),
                        link=data_item.get('link', ''),
                        tags=data_item.get('tags', []),
                        similarity_score=float(similarity)
                    )
                    results.append(result)
            
            logger.info(f"检索完成，返回 {len(results)} 个结果")
            return results
            
        except Exception as e:
            logger.error(f"检索失败：{e}")
            return []
    
    def build(self, force_rebuild: bool = False):
        """
        构建完整的检索系统
        
        Args:
            force_rebuild: 是否强制重新构建
        """
        logger.info("开始构建Retriever系统...")
        
        # 1. 加载数据
        if not self.load_data():
            raise Exception("数据加载失败")
        
        # 2. 尝试加载已有的索引
        if not force_rebuild and self.load_index_and_embeddings():
            logger.info("使用已有索引")
            # 仍需要加载模型用于新查询的编码
            self.load_model()
            return
        
        # 3. 加载模型
        self.load_model()
        
        # 4. 编码问题
        self.encode_questions()
        
        # 5. 构建FAISS索引
        self.build_faiss_index()
        
        # 6. 保存索引和嵌入
        self.save_index_and_embeddings()
        
        logger.info("Retriever系统构建完成！")


def main():
    """
    主函数 - 演示如何使用Retriever
    """
    # 初始化检索器
    retriever = Retriever()
    
    # 构建检索系统
    retriever.build()
    
    # 测试检索
    test_queries = [
        "墨尔本怎么坐公交车？",
        "如何使用Myki卡？",
        "学生乘车有优惠吗？",
        "墨尔本的交通工具有哪些？"
    ]
    
    print("\n" + "="*50)
    print("开始测试语义检索功能")
    print("="*50)
    
    for query in test_queries:
        print(f"\n查询：{query}")
        print("-" * 30)
        
        results = retriever.search(query, k=3)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result.similarity_score:.3f}] {result.question}")
            print(f"   答案：{result.answer}")
            print(f"   标签：{result.tags}")
            print()


if __name__ == "__main__":
    main()
