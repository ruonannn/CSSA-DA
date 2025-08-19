# 🎯 成员A：数据处理工程师 - 详细任务说明

## 👋 欢迎成员A！

你好！你是我们团队的**数据处理工程师**，你的工作就像"数据清洁工"，负责把原始数据变成AI能理解的干净格式。

## 🎯 你的任务目标

把这个文件：`data/qa_clean_data.json` 变成我们系统能使用的标准格式

## 📋 具体要做什么

### 任务1：数据加载模块 (1天)

创建文件：`retriever/data_loader.py`

```python
"""
数据加载模块
作者：成员A
"""

import json
import pandas as pd
from typing import List, Dict

class DataLoader:
    """数据加载器 - 你的主要工具"""
    
    def __init__(self, data_path: str = "data/qa_clean_data.json"):
        self.data_path = data_path
        self.qa_data = []
    
    def load_json_data(self) -> List[Dict]:
        """
        加载JSON数据
        
        TODO: 你需要实现这个函数
        1. 打开JSON文件
        2. 读取所有问答数据
        3. 返回数据列表
        """
        pass
    
    def validate_data_structure(self, data: List[Dict]) -> bool:
        """
        检查数据结构是否正确
        
        TODO: 你需要实现这个函数
        1. 检查每条数据是否有必要字段
        2. 字段包括：id, question, answer, tags等
        3. 返回True/False
        """
        pass
    
    def get_data_statistics(self) -> Dict:
        """
        获取数据统计信息
        
        TODO: 你需要实现这个函数
        1. 统计总数据量
        2. 统计各个分类的数量
        3. 统计平均问题长度
        """
        pass

# 测试代码 - 你可以用这个测试你的代码
if __name__ == "__main__":
    loader = DataLoader()
    data = loader.load_json_data()
    print(f"加载了 {len(data)} 条数据")
```

### 任务2：文本清洗模块 (1天)

创建文件：`retriever/text_cleaner.py`

```python
"""
文本清洗模块
作者：成员A
"""

import re
from typing import List

class TextCleaner:
    """文本清洗器 - 把脏数据变干净"""
    
    def clean_question(self, question: str) -> str:
        """
        清洗问题文本
        
        TODO: 你需要实现这个函数
        1. 去除多余空格
        2. 去除特殊字符（保留中文、英文、数字、常用标点）
        3. 统一格式
        
        示例：
        输入："  墨尔本怎么坐公交车？？！  "
        输出："墨尔本怎么坐公交车？"
        """
        pass
    
    def clean_answer(self, answer: str) -> str:
        """
        清洗答案文本
        
        TODO: 你需要实现这个函数
        1. 类似clean_question
        2. 但保留更多格式信息
        """
        pass
    
    def validate_text_quality(self, text: str) -> bool:
        """
        检查文本质量
        
        TODO: 你需要实现这个函数
        1. 检查是否为空
        2. 检查长度是否合理
        3. 检查是否包含有意义内容
        """
        pass

# 测试代码
if __name__ == "__main__":
    cleaner = TextCleaner()
    test_text = "  墨尔本怎么坐公交车？？！  "
    clean_text = cleaner.clean_question(test_text)
    print(f"原文：'{test_text}'")
    print(f"清洗后：'{clean_text}'")
```

### 任务3：数据验证模块 (1天)

创建文件：`retriever/data_validator.py`

```python
"""
数据验证模块
作者：成员A
"""

from typing import List, Dict, Tuple

class DataValidator:
    """数据验证器 - 确保数据质量"""
    
    def validate_single_item(self, item: Dict) -> Tuple[bool, str]:
        """
        验证单条数据
        
        TODO: 你需要实现这个函数
        1. 检查必需字段是否存在
        2. 检查字段内容是否有效
        3. 返回 (是否有效, 错误信息)
        """
        pass
    
    def validate_all_data(self, data: List[Dict]) -> Dict:
        """
        验证所有数据
        
        TODO: 你需要实现这个函数
        1. 遍历所有数据项
        2. 统计有效/无效数据
        3. 记录错误信息
        4. 返回验证报告
        """
        pass
    
    def fix_common_issues(self, data: List[Dict]) -> List[Dict]:
        """
        修复常见问题
        
        TODO: 你需要实现这个函数
        1. 修复缺失的ID
        2. 修复格式问题
        3. 删除重复数据
        """
        pass

# 测试代码
if __name__ == "__main__":
    validator = DataValidator()
    test_data = [
        {"id": "001", "question": "测试问题", "answer": "测试答案"},
        {"id": "", "question": "", "answer": "无效数据"}
    ]
    report = validator.validate_all_data(test_data)
    print(f"验证报告：{report}")
```

## 🛠️ 开发工具和技巧

### 推荐的Python库
```bash
# 你需要用到这些库
import json      # 处理JSON文件
import re        # 正则表达式，清洗文本
import pandas    # 数据处理（可选）
```

### 常用代码片段

#### 读取JSON文件
```python
with open('data/qa_clean_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

#### 清洗文本的正则表达式
```python
# 去除特殊字符，保留中文、英文、数字、常用标点
clean_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\.\?\!\,]', '', text)
```

#### 检查字段是否存在
```python
required_fields = ['id', 'question', 'answer']
for field in required_fields:
    if field not in item or not item[field]:
        return False, f"缺少字段: {field}"
```

## 📅 时间计划

### 第1天：数据加载
- 上午：学习JSON操作
- 下午：实现DataLoader类
- 晚上：测试数据加载功能

### 第2天：文本清洗  
- 上午：学习正则表达式
- 下午：实现TextCleaner类
- 晚上：测试清洗效果

### 第3天：数据验证
- 上午：实现DataValidator类
- 下午：测试验证功能
- 晚上：整合所有模块

## ✅ 验收标准

### 功能要求
- ✅ 能成功加载221条问答数据
- ✅ 文本清洗后格式统一
- ✅ 数据验证通过率>95%
- ✅ 提供详细的错误报告

### 代码要求
- ✅ 代码有清楚的注释
- ✅ 函数功能单一明确
- ✅ 有完整的测试用例
- ✅ 错误处理完善

## 🆘 遇到问题怎么办

### 常见问题及解决方案

#### 问题1：JSON文件读取失败
```python
# 解决方案：添加异常处理
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"文件不存在：{file_path}")
except json.JSONDecodeError:
    print("JSON格式错误")
```

#### 问题2：中文字符处理问题
```python
# 解决方案：确保UTF-8编码
text = text.encode('utf-8').decode('utf-8')
```

#### 问题3：正则表达式太复杂
```python
# 解决方案：分步处理
text = re.sub(r'\s+', ' ', text)  # 统一空格
text = re.sub(r'[！？]{2,}', '？', text)  # 统一标点
text = text.strip()  # 去除首尾空格
```

### 求助流程
1. **先自己尝试**：查看错误信息，尝试Google搜索
2. **查看文档**：Python官方文档、库的使用说明
3. **问组长**：提供具体错误信息和你尝试的解决方案
4. **团队讨论**：在团队群里分享问题，可能其他人也遇到过

## 🎉 完成后的成就

当你完成这个模块后，你将：
- ✨ 掌握Python文件操作
- ✨ 学会数据清洗技巧
- ✨ 理解数据质量的重要性
- ✨ 为整个团队提供可靠的数据基础

**加油！你是团队数据处理的专家！有问题随时找我！** 🚀
