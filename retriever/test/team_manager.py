"""
Retriever团队项目管理工具
组长专用 - 跟踪团队进度和任务完成情况

作者：组长
创建时间：2025-08-19
"""

import json
import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict
import os

@dataclass
class TaskItem:
    """单个任务项"""
    task_id: str
    description: str
    assigned_to: str
    status: str  # "未开始", "进行中", "已完成", "需要帮助"
    priority: str  # "高", "中", "低"
    estimated_hours: int
    start_date: str
    due_date: str
    completion_date: str = ""
    notes: str = ""

@dataclass
class TeamMember:
    """团队成员信息"""
    name: str
    role: str
    skills: List[str]
    current_tasks: List[str]
    completed_tasks: List[str]
    total_hours: int = 0
    last_update: str = ""

class RetrieeverTeamManager:
    """Retriever团队管理器"""
    
    def __init__(self, data_file: str = "retriever/team_progress.json"):
        self.data_file = data_file
        self.tasks = {}
        self.members = {}
        self.daily_reports = []
        self.load_data()
        self.initialize_team()
    
    def initialize_team(self):
        """初始化团队成员和任务"""
        if not self.members:
            # 初始化团队成员
            self.members = {
                "成员A": TeamMember(
                    name="成员A",
                    role="数据处理工程师",
                    skills=["Python", "数据清洗", "JSON处理"],
                    current_tasks=[],
                    completed_tasks=[]
                ),
                "成员B": TeamMember(
                    name="成员B", 
                    role="文本向量化工程师",
                    skills=["NLP", "TF-IDF", "jieba分词"],
                    current_tasks=[],
                    completed_tasks=[]
                ),
                "成员C": TeamMember(
                    name="成员C",
                    role="相似度计算工程师", 
                    skills=["算法", "numpy", "相似度计算"],
                    current_tasks=[],
                    completed_tasks=[]
                ),
                "成员D": TeamMember(
                    name="成员D",
                    role="存储管理工程师",
                    skills=["文件IO", "序列化", "缓存"],
                    current_tasks=[],
                    completed_tasks=[]
                ),
                "成员E": TeamMember(
                    name="成员E",
                    role="测试验证工程师",
                    skills=["测试", "文档", "质量保证"],
                    current_tasks=[],
                    completed_tasks=[]
                )
            }
        
        if not self.tasks:
            # 初始化任务列表
            today = datetime.date.today().strftime("%Y-%m-%d")
            
            tasks_data = [
                # 成员A的任务
                ("A001", "实现数据加载模块", "成员A", "高", 8, 3),
                ("A002", "实现文本清洗模块", "成员A", "高", 8, 2),
                ("A003", "实现数据验证模块", "成员A", "中", 6, 2),
                
                # 成员B的任务  
                ("B001", "实现中文分词处理", "成员B", "高", 8, 2),
                ("B002", "实现TF-IDF向量化", "成员B", "高", 12, 3),
                ("B003", "优化向量化参数", "成员B", "中", 8, 2),
                ("B004", "实现模型保存加载", "成员B", "高", 6, 1),
                
                # 成员C的任务
                ("C001", "实现余弦相似度计算", "成员C", "高", 8, 2),
                ("C002", "实现结果排序筛选", "成员C", "高", 6, 2),
                ("C003", "性能优化", "成员C", "中", 8, 2),
                
                # 成员D的任务
                ("D001", "实现向量持久化存储", "成员D", "高", 6, 2),
                ("D002", "实现快速加载机制", "成员D", "高", 8, 2),
                ("D003", "实现查询缓存", "成员D", "中", 6, 2),
                
                # 成员E的任务
                ("E001", "编写基础测试用例", "成员E", "高", 8, 1),
                ("E002", "实现性能基准测试", "成员E", "中", 10, 2),
                ("E003", "编写使用文档", "成员E", "中", 8, 2),
                ("E004", "生成最终测试报告", "成员E", "高", 6, 1),
            ]
            
            for task_id, desc, assignee, priority, hours, days_offset in tasks_data:
                due_date = (datetime.date.today() + datetime.timedelta(days=days_offset)).strftime("%Y-%m-%d")
                
                self.tasks[task_id] = TaskItem(
                    task_id=task_id,
                    description=desc,
                    assigned_to=assignee,
                    status="未开始",
                    priority=priority,
                    estimated_hours=hours,
                    start_date=today,
                    due_date=due_date
                )
                
                # 更新成员任务列表
                if assignee in self.members:
                    self.members[assignee].current_tasks.append(task_id)
    
    def update_task_status(self, task_id: str, status: str, notes: str = ""):
        """更新任务状态"""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.tasks[task_id].notes = notes
            
            if status == "已完成":
                self.tasks[task_id].completion_date = datetime.date.today().strftime("%Y-%m-%d")
                
                # 移动到已完成任务
                assignee = self.tasks[task_id].assigned_to
                if assignee in self.members:
                    if task_id in self.members[assignee].current_tasks:
                        self.members[assignee].current_tasks.remove(task_id)
                    self.members[assignee].completed_tasks.append(task_id)
            
            self.save_data()
            print(f"✅ 任务 {task_id} 状态更新为: {status}")
        else:
            print(f"❌ 任务 {task_id} 不存在")
    
    def add_daily_report(self, member: str, completed: str, planned: str, issues: str = ""):
        """添加每日报告"""
        report = {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "member": member,
            "completed": completed,
            "planned": planned,
            "issues": issues,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.daily_reports.append(report)
        self.members[member].last_update = report["timestamp"]
        self.save_data()
        print(f"📝 {member} 的日报已添加")
    
    def get_team_progress(self) -> Dict:
        """获取团队整体进度"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == "已完成"])
        in_progress_tasks = len([t for t in self.tasks.values() if t.status == "进行中"])
        not_started_tasks = len([t for t in self.tasks.values() if t.status == "未开始"])
        blocked_tasks = len([t for t in self.tasks.values() if t.status == "需要帮助"])
        
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "总任务数": total_tasks,
            "已完成": completed_tasks,
            "进行中": in_progress_tasks,
            "未开始": not_started_tasks,
            "需要帮助": blocked_tasks,
            "完成百分比": f"{progress_percentage:.1f}%"
        }
    
    def get_member_status(self, member: str) -> Dict:
        """获取成员状态"""
        if member not in self.members:
            return {"错误": "成员不存在"}
        
        member_info = self.members[member]
        current_task_details = []
        
        for task_id in member_info.current_tasks:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                current_task_details.append({
                    "任务ID": task.task_id,
                    "描述": task.description,
                    "状态": task.status,
                    "优先级": task.priority,
                    "截止日期": task.due_date
                })
        
        return {
            "姓名": member_info.name,
            "角色": member_info.role,
            "技能": member_info.skills,
            "当前任务": current_task_details,
            "已完成任务数": len(member_info.completed_tasks),
            "最后更新": member_info.last_update
        }
    
    def get_overdue_tasks(self) -> List[Dict]:
        """获取逾期任务"""
        today = datetime.date.today().strftime("%Y-%m-%d")
        overdue_tasks = []
        
        for task in self.tasks.values():
            if task.status != "已完成" and task.due_date < today:
                overdue_tasks.append({
                    "任务ID": task.task_id,
                    "描述": task.description,
                    "负责人": task.assigned_to,
                    "截止日期": task.due_date,
                    "逾期天数": (datetime.date.today() - datetime.datetime.strptime(task.due_date, "%Y-%m-%d").date()).days
                })
        
        return overdue_tasks
    
    def generate_daily_standup(self) -> str:
        """生成每日站会报告"""
        today = datetime.date.today().strftime("%Y-%m-%d")
        
        report = f"""
🚀 Retriever团队每日站会 - {today}

📊 整体进度：
{self._dict_to_string(self.get_team_progress())}

👥 成员状态：
"""
        
        for member_name in self.members:
            status = self.get_member_status(member_name)
            current_tasks = status.get("当前任务", [])
            
            report += f"""
🔹 {member_name} ({status['角色']})
   当前任务: {len(current_tasks)}个
   已完成: {status['已完成任务数']}个
   最后更新: {status['最后更新'] or '暂无'}
"""
            
            if current_tasks:
                for task in current_tasks[:2]:  # 只显示前2个任务
                    report += f"   - {task['描述']} ({task['状态']})\n"
        
        # 逾期任务警告
        overdue = self.get_overdue_tasks()
        if overdue:
            report += f"\n⚠️  逾期任务警告:\n"
            for task in overdue:
                report += f"   - {task['描述']} (负责人: {task['负责人']}, 逾期{task['逾期天数']}天)\n"
        
        return report
    
    def _dict_to_string(self, d: Dict) -> str:
        """将字典转为字符串"""
        return "\n".join([f"   {k}: {v}" for k, v in d.items()])
    
    def save_data(self):
        """保存数据到文件"""
        data = {
            "tasks": {k: asdict(v) for k, v in self.tasks.items()},
            "members": {k: asdict(v) for k, v in self.members.items()},
            "daily_reports": self.daily_reports,
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.tasks = {k: TaskItem(**v) for k, v in data.get("tasks", {}).items()}
                self.members = {k: TeamMember(**v) for k, v in data.get("members", {}).items()}
                self.daily_reports = data.get("daily_reports", [])
                
            except Exception as e:
                print(f"加载数据失败: {e}")

def main():
    """命令行工具主函数"""
    manager = RetrieeverTeamManager()
    
    while True:
        print(f"\n{'='*50}")
        print("🎯 Retriever团队管理工具")
        print("="*50)
        print("1. 查看团队进度")
        print("2. 查看成员状态") 
        print("3. 更新任务状态")
        print("4. 添加每日报告")
        print("5. 查看逾期任务")
        print("6. 生成站会报告")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-6): ").strip()
        
        if choice == "1":
            print("\n📊 团队整体进度:")
            progress = manager.get_team_progress()
            for k, v in progress.items():
                print(f"   {k}: {v}")
                
        elif choice == "2":
            member = input("请输入成员姓名 (成员A-E): ").strip()
            status = manager.get_member_status(member)
            print(f"\n👤 {member} 状态:")
            print(json.dumps(status, ensure_ascii=False, indent=2))
            
        elif choice == "3":
            task_id = input("请输入任务ID: ").strip()
            print("状态选项: 未开始, 进行中, 已完成, 需要帮助")
            status = input("请输入新状态: ").strip()
            notes = input("备注 (可选): ").strip()
            manager.update_task_status(task_id, status, notes)
            
        elif choice == "4":
            member = input("成员姓名: ").strip()
            completed = input("昨天完成的工作: ").strip()
            planned = input("今天计划的工作: ").strip()
            issues = input("遇到的问题 (可选): ").strip()
            manager.add_daily_report(member, completed, planned, issues)
            
        elif choice == "5":
            overdue = manager.get_overdue_tasks()
            if overdue:
                print("\n⚠️  逾期任务:")
                for task in overdue:
                    print(f"   - {task['描述']} (负责人: {task['负责人']}, 逾期{task['逾期天数']}天)")
            else:
                print("\n✅ 没有逾期任务!")
                
        elif choice == "6":
            report = manager.generate_daily_standup()
            print(report)
            
        elif choice == "0":
            print("👋 再见!")
            break
            
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
