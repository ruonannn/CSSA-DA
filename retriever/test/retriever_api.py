"""
模块二：Retriever API接口
提供标准化的检索服务接口

作者：ruonan (xrn zmy syl sly团队)
创建时间：2025-08-18
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import logging

# 导入我们的检索器
try:
    from simple_retriever import SimpleRetriever, RetrievalResult
except ImportError:
    # 如果在其他目录运行，尝试相对导入
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from simple_retriever import SimpleRetriever, RetrievalResult

logger = logging.getLogger(__name__)

class RetrieverAPI:
    """
    Retriever模块的标准API接口
    
    提供标准化的检索服务，符合项目规范要求：
    - 给定一个query提取k个可能的回答
    - 返回标准格式的结果
    """
    
    def __init__(self, data_path: str = "data/qa_clean_data.json"):
        """
        初始化Retriever API
        
        Args:
            data_path: 问答数据文件路径
        """
        self.retriever = SimpleRetriever(data_path=data_path)
        self.is_built = False
        self._build_retriever()
    
    def _build_retriever(self):
        """构建检索器"""
        try:
            self.retriever.build()
            self.is_built = True
            logger.info("Retriever API 初始化完成")
        except Exception as e:
            logger.error(f"Retriever构建失败: {e}")
            self.is_built = False
            raise e
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        执行语义检索 - 主要API接口
        
        Args:
            query: 用户查询问题
            k: 返回结果数量，默认5个
            
        Returns:
            List[Dict]: 检索结果列表，每个结果包含：
                - question_id: 问题ID
                - question: 问题文本
                - answer: 答案文本
                - source: 来源
                - link: 链接
                - tags: 标签列表
                - similarity_score: 相似度分数
        """
        if not self.is_built:
            raise Exception("Retriever未正确初始化")
        
        if not query or not query.strip():
            return []
        
        # 调用检索器
        results = self.retriever.search(query.strip(), k)
        
        # 转换为字典格式
        return [asdict(result) for result in results]
    
    def get_stats(self) -> Dict:
        """
        获取检索器统计信息
        
        Returns:
            Dict: 统计信息
        """
        if not self.is_built:
            return {"status": "not_built"}
        
        return {
            "status": "ready",
            "total_questions": len(self.retriever.qa_data),
            "model_type": "TF-IDF + 余弦相似度",
            "vector_dimension": getattr(self.retriever.question_vectors, 'shape', [0, 0])[1] if hasattr(self.retriever, 'question_vectors') else 0,
            "index_built": self.is_built
        }
    
    def search_by_category(self, query: str, category: str, k: int = 5) -> List[Dict]:
        """
        按分类检索
        
        Args:
            query: 查询问题
            category: 分类标签
            k: 返回结果数量
            
        Returns:
            List[Dict]: 过滤后的检索结果
        """
        results = self.search(query, k * 2)  # 先获取更多结果
        
        # 过滤指定分类
        filtered_results = [
            result for result in results 
            if category in result.get('tags', [])
        ]
        
        return filtered_results[:k]
    
    def get_question_by_id(self, question_id: str) -> Optional[Dict]:
        """
        根据ID获取问答对
        
        Args:
            question_id: 问题ID
            
        Returns:
            Dict: 问答对信息，如果不存在返回None
        """
        for item in self.retriever.qa_data:
            if item.get('id') == question_id:
                return item
        return None
    
    def get_all_categories(self) -> List[str]:
        """
        获取所有分类标签
        
        Returns:
            List[str]: 分类标签列表
        """
        categories = set()
        for item in self.retriever.qa_data:
            categories.update(item.get('tags', []))
        return sorted(list(categories))

def demo():
    """演示Retriever API的使用"""
    print("🚀 Retriever API 演示")
    print("=" * 50)
    
    try:
        # 初始化API
        api = RetrieverAPI()
        
        # 显示统计信息
        stats = api.get_stats()
        print(f"📊 系统状态: {stats}")
        print(f"📚 数据量: {stats['total_questions']} 条问答")
        print(f"🔧 模型类型: {stats['model_type']}")
        print(f"📐 向量维度: {stats['vector_dimension']}")
        
        print(f"\n🏷️  可用分类: {api.get_all_categories()}")
        
        # 测试查询
        test_queries = [
            ("墨尔本公共交通", 3),
            ("学生优惠", 2),
            ("Myki卡使用", 3),
            ("租房信息", 2)
        ]
        
        print(f"\n🔍 开始测试查询...")
        print("-" * 50)
        
        for query, k in test_queries:
            print(f"\n🔍 查询: '{query}' (Top-{k})")
            results = api.search(query, k)
            
            if not results:
                print("   ❌ 没有找到相关结果")
                continue
                
            for i, result in enumerate(results, 1):
                print(f"   {i}. 📊 {result['similarity_score']:.3f} | {result['question']}")
                print(f"      💡 {result['answer'][:50]}...")
                print(f"      🏷️  {result['tags']}")
        
        # 测试分类检索
        print(f"\n🎯 测试分类检索 - '交通'类问题...")
        transport_results = api.search_by_category("公交车", "交通", 3)
        for i, result in enumerate(transport_results, 1):
            print(f"   {i}. {result['question']}")
        
        # 测试ID查询
        print(f"\n🔍 测试ID查询...")
        question_info = api.get_question_by_id("00001")
        if question_info:
            print(f"   ID 00001: {question_info['question']}")
        
        print(f"\n✅ API测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

# 命令行接口
def main():
    """命令行交互式检索"""
    print("🎯 Retriever 交互式检索")
    print("输入 'quit' 退出程序")
    print("-" * 30)
    
    try:
        api = RetrieverAPI()
        
        while True:
            query = input("\n🔍 请输入查询: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            if not query:
                continue
                
            results = api.search(query, 5)
            
            if not results:
                print("❌ 没有找到相关结果")
                continue
                
            print(f"\n📋 找到 {len(results)} 个结果:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. 📊 相似度: {result['similarity_score']:.3f}")
                print(f"   ❓ 问题: {result['question']}")
                print(f"   ✅ 答案: {result['answer']}")
                print(f"   🏷️  标签: {result['tags']}")
                
    except KeyboardInterrupt:
        print(f"\n👋 再见!")
    except Exception as e:
        print(f"❌ 程序错误: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        main()
