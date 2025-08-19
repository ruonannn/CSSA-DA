"""
测试Retriever模块的脚本

作者：ruonan
创建时间：2025-08-18
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_environment():
    """测试环境依赖"""
    print("🔧 测试环境依赖...")
    
    required_packages = [
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('pandas', 'pandas'),
    ]
    
    missing_packages = []
    
    for package_name, install_name in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            print(f"❌ {package_name} - 缺失")
            missing_packages.append(install_name)
    
    if missing_packages:
        print(f"\n需要安装的包：{missing_packages}")
        print("请运行：pip install " + " ".join(missing_packages))
        return False
    
    print("✅ 所有依赖包检查通过")
    return True

def test_data_loading():
    """测试数据加载"""
    print("\n📊 测试数据加载...")
    
    import json
    
    data_path = "data/qa_clean_data.json"
    
    if not os.path.exists(data_path):
        print(f"❌ 数据文件不存在: {data_path}")
        return False
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ 成功加载 {len(data)} 条数据")
        
        # 显示数据样例
        if data:
            print("\n📝 数据样例:")
            sample = data[0]
            print(f"   ID: {sample.get('id', 'N/A')}")
            print(f"   问题: {sample.get('question', 'N/A')}")
            print(f"   答案: {sample.get('answer', 'N/A')[:50]}...")
            print(f"   标签: {sample.get('tags', [])}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return False

def test_basic_retriever():
    """测试基础检索器"""
    print("\n🔍 测试基础检索器...")
    
    try:
        # 使用最基础的方法实现检索
        import json
        import re
        from collections import Counter
        
        # 加载数据
        with open("data/qa_clean_data.json", 'r', encoding='utf-8') as f:
            qa_data = json.load(f)
        
        def simple_search(query, data, k=5):
            """简单的关键词匹配搜索"""
            # 清理查询
            query_words = set(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', query.lower()))
            
            results = []
            for item in data:
                question = item.get('question', '')
                question_words = set(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', question.lower()))
                
                # 计算重叠词数
                overlap = len(query_words.intersection(question_words))
                if overlap > 0:
                    score = overlap / len(query_words.union(question_words))
                    results.append((item, score))
            
            # 按分数排序
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:k]
        
        # 测试查询
        test_queries = [
            "墨尔本公交车",
            "Myki卡",
            "学生优惠",
            "交通工具"
        ]
        
        for query in test_queries:
            print(f"\n🔍 查询: {query}")
            results = simple_search(query, qa_data, k=3)
            
            if results:
                for i, (item, score) in enumerate(results, 1):
                    print(f"   {i}. [{score:.3f}] {item.get('question', '')}")
            else:
                print("   没有找到相关结果")
        
        print("\n✅ 基础检索器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 基础检索器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 Retriever模块测试开始")
    print("=" * 50)
    
    # 切换到项目根目录
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(f"📁 当前工作目录: {os.getcwd()}")
    
    # 测试步骤
    tests = [
        ("环境依赖", test_environment),
        ("数据加载", test_data_loading),
        ("基础检索", test_basic_retriever),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} 测试失败")
        except Exception as e:
            print(f"\n❌ {test_name} 测试出错: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试总结: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！可以开始实现完整的Retriever模块")
        print("\n📋 下一步建议:")
        print("1. 安装jieba分词库: pip install jieba")
        print("2. 运行simple_retriever.py进行TF-IDF检索测试")
        print("3. 如果需要更高精度，可安装sentence-transformers使用BERT模型")
    else:
        print("⚠️  部分测试失败，请检查环境和数据")

if __name__ == "__main__":
    main()
