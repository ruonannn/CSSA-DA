模块二：Retriever
模块目标：给定一个query提取k个可能的回答
模块步骤：
1. 调用hugging face模型将json的问题encode成vector
2. 构建FAISS数据库
3. 使用FAISS内置功能retrieve k 个最相近的问题
4. 找到对应的json并返还
注意事项：
1. 现阶段使用100条手动收集的数据进行该模块
