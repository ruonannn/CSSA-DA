#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检索器模块 (Retriever Module)

该模块实现了基于向量相似性的问答检索系统，包含以下功能：
1. 文本向量化 - 使用sentence-transformers将中文问题转换为向量
2. 索引构建 - 使用FAISS构建高效的向量索引
3. ID映射 - 建立索引ID到原始数据的映射关系
4. 检索接口 - 提供search(query, k)函数返回最相似的问题

作者: CSSA-DA Team
日期: 2024
"""

import json
import numpy as np
import torch
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os
from typing import List, Dict, Any


class QARetriever:
    """问答检索器类"""
    
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
        """
        初始化检索器
        
        Args:
            model_name (str): 使用的sentence-transformers模型名称
        """
        self.model_name = model_name
        self.encoder = None
        self.index = None
        self.id_mapping = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def load_model(self):
        """加载编码模型"""
        print(f"加载编码模型: {self.model_name}")
        self.encoder = SentenceTransformer(self.model_name, device=self.device)
        
    def load_index(self, index_path: str):
        """
        加载FAISS索引
        
        Args:
            index_path (str): 索引文件路径
        """
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"索引文件不存在: {index_path}")
        
        print(f"加载FAISS索引: {index_path}")
        self.index = faiss.read_index(index_path)
        
    def load_id_mapping(self, mapping_path: str):
        """
        加载ID映射
        
        Args:
            mapping_path (str): 映射文件路径
        """
        if not os.path.exists(mapping_path):
            raise FileNotFoundError(f"映射文件不存在: {mapping_path}")
        
        print(f"加载ID映射: {mapping_path}")
        with open(mapping_path, 'r', encoding='utf-8') as f:
            self.id_mapping = json.load(f)
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        检索最相似的K个问题
        
        Args:
            query (str): 用户查询问题
            k (int): 返回结果数量，默认5个
            
        Returns:
            list: 包含相似问题信息的列表
        """
        if not all([self.encoder, self.index, self.id_mapping]):
            raise ValueError("请先加载模型、索引和ID映射!")
        
        # 1. 将查询编码为向量
        query_vector = self.encoder.encode([query], convert_to_tensor=True, device=self.device)
        query_vector_np = query_vector.cpu().numpy().astype('float32')
        
        # 2. 使用FAISS搜索最相似的向量
        distances, indices = self.index.search(query_vector_np, k)
        
        # 3. 根据索引获取完整信息
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if str(idx) in self.id_mapping:
                item = self.id_mapping[str(idx)]
                result = {
                    'rank': i + 1,
                    'similarity_score': float(1 / (1 + distance)),  # 转换为相似度分数
                    'distance': float(distance),
                    'original_id': item['original_id'],
                    'question': item['question'],
                    'answer': item['answer'],
                    'link': item['link'],
                    'tags': item['tags']
                }
                results.append(result)
        
        return results
    
    def initialize(self, index_path: str, mapping_path: str):
        """
        初始化检索器
        
        Args:
            index_path (str): FAISS索引文件路径
            mapping_path (str): ID映射文件路径
        """
        self.load_model()
        self.load_index(index_path)
        self.load_id_mapping(mapping_path)
        print("检索器初始化完成!")


def build_retriever_index(data_path: str, 
                         vectors_path: str, 
                         index_path: str, 
                         mapping_path: str,
                         model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
    """
    构建检索器索引的完整流程
    
    Args:
        data_path (str): QA数据集文件路径
        vectors_path (str): 向量保存路径
        index_path (str): FAISS索引保存路径
        mapping_path (str): ID映射保存路径
        model_name (str): 使用的模型名称
    """
    print("=== 开始构建检索器索引 ===")
    
    # 1. 加载数据
    print("1. 加载QA数据...")
    with open(data_path, 'r', encoding='utf-8') as f:
        qa_data = json.load(f)
    print(f"加载了 {len(qa_data)} 条QA数据")
    
    # 2. 提取问题文本
    questions = [item['question'] for item in qa_data]
    
    # 3. 文本向量化
    print("2. 开始文本向量化...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SentenceTransformer(model_name, device=device)
    
    question_vectors = model.encode(
        questions,
        batch_size=32,
        show_progress_bar=True,
        convert_to_tensor=True,
        device=device
    )
    
    # 保存向量
    torch.save(question_vectors, vectors_path)
    print(f"向量已保存到: {vectors_path}")
    
    # 4. 构建FAISS索引
    print("3. 构建FAISS索引...")
    vectors_np = question_vectors.cpu().numpy().astype('float32')
    dimension = vectors_np.shape[1]
    
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors_np)
    
    faiss.write_index(index, index_path)
    print(f"FAISS索引已保存到: {index_path}")
    
    # 5. 创建ID映射
    print("4. 创建ID映射...")
    id_mapping = {}
    for idx, item in enumerate(qa_data):
        # 使用字符串作为键，与JSON格式保持一致
        id_mapping[str(idx)] = {
            'original_id': item['id'],
            'question': item['question'],
            'answer': item['answer'],
            'link': item['link'],
            'tags': item['tags']
        }
    
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(id_mapping, f, ensure_ascii=False, indent=2)
    
    print(f"ID映射已保存到: {mapping_path}")
    print("=== 索引构建完成! ===")


def main():
    """主函数 - 演示检索器使用"""
    # 文件路径
    data_path = "../ai_sample/qa_dataset_cleaned.json"
    vectors_path = "../ai_sample/qa_tensors.pt"
    index_path = "../ai_sample/qa_faiss_index.index"
    mapping_path = "../ai_sample/id_map.json"
    
    # 检查是否需要构建索引
    if not all(os.path.exists(p) for p in [index_path, mapping_path]):
        print("检测到缺少索引文件，开始构建...")
        build_retriever_index(data_path, vectors_path, index_path, mapping_path)
    
    # 初始化检索器
    retriever = QARetriever()
    retriever.initialize(index_path, mapping_path)
    
    # 测试查询
    test_queries = [
        "如何使用公共交通",
        "机场到市区怎么走",
        "学生票有优惠吗",
        "停车规则",
        "租车需要什么"
    ]
    
    print("\n=== 测试检索功能 ===")
    for query in test_queries:
        print(f"\n查询: '{query}'")
        print("-" * 50)
        
        results = retriever.search(query, k=3)
        
        for result in results:
            print(f"排名 {result['rank']}: 相似度 {result['similarity_score']:.4f}")
            print(f"问题: {result['question']}")
            print(f"答案: {result['answer']}")
            if result['tags']:
                print(f"标签: {', '.join(result['tags'])}")
            print()


if __name__ == "__main__":
    main()
