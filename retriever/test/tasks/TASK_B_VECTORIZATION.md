# 🎯 成员B：文本向量化工程师 - 详细任务说明

## 👋 欢迎成员B！

你好！你是我们团队的**文本向量化工程师**，你的工作就像"翻译官"，负责把人类语言翻译成计算机能理解的数字向量。

## 🎯 你的任务目标

把中文问题："墨尔本怎么坐公交车？" 
变成数字向量：`[0.1, 0.8, 0.2, 0.0, 0.5, ...]`

## 📋 具体要做什么

### 任务1：中文分词模块 (1天)

创建文件：`retriever/text_processor.py`

```python
"""
中文文本处理模块
作者：成员B
"""

import jieba
import re
from typing import List

class ChineseTextProcessor:
    """中文文本处理器 - 你的核心工具"""
    
    def __init__(self):
        # 初始化jieba分词器
        self.setup_jieba()
    
    def setup_jieba(self):
        """
        设置jieba分词器
        
        TODO: 你需要实现这个函数
        1. 添加自定义词典（墨尔本、Myki等专业词汇）
        2. 设置分词模式
        """
        # 添加专业词汇，避免被错误分词
        custom_words = ['墨尔本', 'Myki', 'PTV', '电车', '公交车']
        for word in custom_words:
            jieba.add_word(word)
    
    def segment_text(self, text: str) -> List[str]:
        """
        对文本进行分词
        
        TODO: 你需要实现这个函数
        1. 使用jieba分词
        2. 过滤掉停用词
        3. 过滤掉长度<2的词
        
        示例：
        输入："墨尔本怎么坐公交车？"
        输出：["墨尔本", "怎么", "公交车"]
        """
        pass
    
    def preprocess_for_vectorization(self, text: str) -> str:
        """
        为向量化预处理文本
        
        TODO: 你需要实现这个函数
        1. 分词
        2. 去除停用词
        3. 连接成空格分隔的字符串
        4. 统一格式
        """
        pass

# 测试代码
if __name__ == "__main__":
    processor = ChineseTextProcessor()
    test_text = "墨尔本怎么坐公交车？"
    segments = processor.segment_text(test_text)
    print(f"原文：{test_text}")
    print(f"分词结果：{segments}")
```

### 任务2：TF-IDF向量化模块 (2天)

创建文件：`retriever/vectorizer.py`

```python
"""
TF-IDF向量化模块
作者：成员B
"""

import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple
from text_processor import ChineseTextProcessor

class QuestionVectorizer:
    """问题向量化器 - 把文字变成数字"""
    
    def __init__(self):
        self.text_processor = ChineseTextProcessor()
        self.vectorizer = None
        self.question_vectors = None
        
    def create_tfidf_vectorizer(self) -> TfidfVectorizer:
        """
        创建TF-IDF向量化器
        
        TODO: 你需要实现这个函数
        1. 设置合适的参数
        2. max_features: 最大特征数（建议1000-5000）
        3. ngram_range: n-gram范围（建议(1,2)）
        4. min_df, max_df: 文档频率范围
        """
        pass
    
    def fit_transform_questions(self, questions: List[str]) -> np.ndarray:
        """
        训练向量化器并转换问题
        
        TODO: 你需要实现这个函数
        1. 预处理所有问题文本
        2. 使用TF-IDF拟合并转换
        3. 返回向量矩阵
        
        输入：["墨尔本公交车", "学生优惠", ...]
        输出：numpy数组，形状为(问题数, 特征数)
        """
        pass
    
    def transform_single_question(self, question: str) -> np.ndarray:
        """
        转换单个问题为向量
        
        TODO: 你需要实现这个函数
        1. 预处理问题文本
        2. 使用已训练的向量化器转换
        3. 返回向量
        """
        pass
    
    def get_feature_names(self) -> List[str]:
        """
        获取特征词汇表
        
        TODO: 你需要实现这个函数
        1. 返回TF-IDF的特征词汇
        2. 用于调试和分析
        """
        pass
    
    def save_vectorizer(self, save_path: str):
        """
        保存向量化器
        
        TODO: 你需要实现这个函数
        1. 使用pickle保存vectorizer
        2. 保存到指定路径
        """
        pass
    
    def load_vectorizer(self, load_path: str):
        """
        加载向量化器
        
        TODO: 你需要实现这个函数
        1. 使用pickle加载vectorizer
        2. 从指定路径加载
        """
        pass

# 测试代码
if __name__ == "__main__":
    vectorizer = QuestionVectorizer()
    
    # 测试数据
    test_questions = [
        "墨尔本怎么坐公交车？",
        "如何使用Myki卡？",
        "学生乘车有优惠吗？"
    ]
    
    # 训练和转换
    vectors = vectorizer.fit_transform_questions(test_questions)
    print(f"向量形状：{vectors.shape}")
    print(f"特征数量：{len(vectorizer.get_feature_names())}")
```

### 任务3：向量质量优化模块 (1天)

创建文件：`retriever/vector_optimizer.py`

```python
"""
向量质量优化模块
作者：成员B
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Tuple

class VectorOptimizer:
    """向量优化器 - 让向量表示更准确"""
    
    def analyze_vocabulary(self, vectorizer: TfidfVectorizer) -> Dict:
        """
        分析词汇表质量
        
        TODO: 你需要实现这个函数
        1. 统计词汇数量
        2. 分析词汇分布
        3. 找出可能的无意义词汇
        """
        pass
    
    def optimize_parameters(self, questions: List[str]) -> Dict:
        """
        优化TF-IDF参数
        
        TODO: 你需要实现这个函数
        1. 尝试不同的max_features值
        2. 尝试不同的ngram_range
        3. 评估向量质量
        4. 返回最佳参数
        """
        pass
    
    def evaluate_vector_quality(self, vectors: np.ndarray, questions: List[str]) -> Dict:
        """
        评估向量质量
        
        TODO: 你需要实现这个函数
        1. 计算向量密度（非零元素比例）
        2. 计算向量相似度分布
        3. 分析是否有异常向量
        """
        pass
    
    def recommend_improvements(self, analysis_result: Dict) -> List[str]:
        """
        推荐改进建议
        
        TODO: 你需要实现这个函数
        1. 基于分析结果
        2. 给出具体的改进建议
        """
        pass

# 测试代码
if __name__ == "__main__":
    optimizer = VectorOptimizer()
    # 这里可以测试优化功能
```

## 🛠️ 开发工具和技巧

### 需要的Python库
```bash
# 安装命令
pip install jieba scikit-learn numpy

# 导入语句
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
```

### 重要概念解释

#### 什么是TF-IDF？
```
TF-IDF = Term Frequency × Inverse Document Frequency

简单理解：
- TF：词在这个文档中出现多少次（越多越重要）
- IDF：词在所有文档中出现多少次（越少越特殊）
- 结果：既常见又特殊的词权重最高

例子：
"墨尔本公交车" vs "的在是"
"墨尔本公交车"更有意义，TF-IDF值更高
```

#### 什么是n-gram？
```
1-gram: ["墨尔本", "公交车"]
2-gram: ["墨尔本 公交车"]

组合使用可以捕获更多语义信息
```

### 常用代码片段

#### jieba分词
```python
import jieba

# 添加自定义词汇
jieba.add_word("墨尔本")

# 分词
words = jieba.cut("墨尔本公交车")
word_list = list(words)
```

#### TF-IDF向量化
```python
from sklearn.feature_extraction.text import TfidfVectorizer

# 创建向量化器
vectorizer = TfidfVectorizer(
    max_features=1000,    # 最大特征数
    ngram_range=(1, 2),   # 1-gram和2-gram
    min_df=1,             # 最小文档频率
    max_df=0.8            # 最大文档频率
)

# 训练和转换
vectors = vectorizer.fit_transform(texts)
```

#### 保存和加载模型
```python
import pickle

# 保存
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# 加载
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
```

## 📅 时间计划

### 第1天：中文分词
- 上午：学习jieba库用法
- 下午：实现分词功能
- 晚上：测试分词效果

### 第2天：TF-IDF基础
- 上午：学习TF-IDF原理
- 下午：实现基础向量化
- 晚上：测试向量化功能

### 第3天：参数优化
- 上午：实现参数调优
- 下午：测试不同参数效果
- 晚上：选择最佳配置

### 第4天：质量优化
- 上午：实现质量评估
- 下午：优化向量质量
- 晚上：完善保存加载功能

## ✅ 验收标准

### 功能要求
- ✅ 中文分词准确率>90%
- ✅ 向量维度在1000-5000之间
- ✅ 向量化速度<5秒（221个问题）
- ✅ 能保存和加载模型

### 质量要求
- ✅ 相似问题的向量相似度>0.5
- ✅ 不相关问题的向量相似度<0.3
- ✅ 向量稠密度适中（不要太稀疏）

## 🆘 遇到问题怎么办

### 常见问题及解决方案

#### 问题1：jieba分词不准确
```python
# 解决方案：添加专业词汇
domain_words = ['墨尔本', 'Myki', 'PTV', '公交车', '电车']
for word in domain_words:
    jieba.add_word(word)
```

#### 问题2：向量维度太高或太低
```python
# 调整max_features参数
vectorizer = TfidfVectorizer(
    max_features=2000,  # 从1000调整到2000
    ngram_range=(1, 2)
)
```

#### 问题3：向量太稀疏
```python
# 调整min_df和max_df
vectorizer = TfidfVectorizer(
    min_df=2,    # 增加最小文档频率
    max_df=0.7   # 降低最大文档频率
)
```

#### 问题4：内存不足
```python
# 使用稀疏矩阵
from scipy.sparse import csr_matrix
vectors = vectorizer.fit_transform(texts)  # 已经是稀疏矩阵
```

### 调试技巧
1. **查看词汇表**：`vectorizer.get_feature_names_out()`
2. **检查向量形状**：`vectors.shape`
3. **查看向量密度**：`vectors.nnz / (vectors.shape[0] * vectors.shape[1])`

## 🎉 完成后的成就

当你完成这个模块后，你将：
- ✨ 掌握中文自然语言处理
- ✨ 理解TF-IDF算法原理
- ✨ 学会特征工程技巧
- ✨ 为检索系统提供核心向量表示

**加油！你是团队的"翻译官"，让计算机理解人类语言！** 🚀
