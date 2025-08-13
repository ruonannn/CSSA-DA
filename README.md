### 环境安装
1. 使用anaconda作为环境管理方式
2. 打开terminal（打开 anaconda prompt 如果你是Windows用户）
3. Navigate到CSSA-DA文件夹
3. 运行conda env create -f environment.yml
4. 运行conda activate cssa-ai来激活当前环境（或者直接在vscode中选择）
5. 后续更新环境运行conda env update -f environment.yaml --prune


### 项目注意：
1. 使用github作为代码传输方式，进行修改前先创建一个以自己名字命名的branch，创建新的file后进行修改，尽量不要修改已经在main里的文件，会导致conflict。完成当前任务后通过commit -> push -> pull request来合并入main。
2. 保持代码 clean 和 readable，不强制要求oop。
