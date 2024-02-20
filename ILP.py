import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus

# 步骤1：导入文件
file_path = r'D:\Synergence\TaskWeaver\TaskWeaver\project\sample_data\test2.xlsx'  # 更换为实际文件路径
data = pd.read_excel(file_path)

# 步骤2：根据基础条件筛选
filtered_data = data[
    (data['粉丝量'] > 500000) &
    (data['等级'].isin(['A', 'S'])) &
    (data['星图指数'] > 60) &
    (data['性价比指数'] > 60) &
    (data['总分'] > 7)
]

# 函数：构建并求解模型
def solve_ilp(exclude_indices=[]):
    model = LpProblem(name="daren-selection", sense=LpMaximize)
    selection_vars = LpVariable.dicts("Select", range(len(filtered_data)), cat="Binary")
    model += lpSum(selection_vars[i] * filtered_data.iloc[i]['预期播放量'] for i in range(len(filtered_data)))
    model += lpSum(selection_vars[i] * filtered_data.iloc[i]['60s以上视频报价'] for i in range(len(filtered_data))) <= 1000000
    model += lpSum(selection_vars[i] for i in range(len(filtered_data))) == 15
    car_indices = [i for i in range(len(filtered_data)) if filtered_data.iloc[i]['内容垂类'] == '汽车']
    model += lpSum(selection_vars[i] for i in car_indices) >= 0.6 * lpSum(selection_vars[i] for i in range(len(filtered_data)))
    if exclude_indices:
        model += lpSum(selection_vars[i] for i in exclude_indices) <= len(exclude_indices) - 1
    status = model.solve()
    return status, selection_vars

# 步骤3：求解第一最优解
status, selection_vars = solve_ilp()
if LpStatus[status] == 'Optimal':
    selected_indices = [i for i in range(len(filtered_data)) if selection_vars[i].value() == 1]
    selected_daren = filtered_data.iloc[selected_indices]
    print("第一最优解的达人:")
    print(selected_daren[['昵称', '内容垂类']])
    print(f"总报价: {sum(selected_daren['60s以上视频报价'])}元")
    print(f"总预期播放量: {sum(selected_daren['预期播放量'])}")
else:
    print("没有找到第一最优解。")

# 步骤4：尝试找到一个备用方案
status, selection_vars = solve_ilp(selected_indices)
if LpStatus[status] == 'Optimal':
    selected_indices_alternative = [i for i in range(len(filtered_data)) if selection_vars[i].value() == 1]
    selected_daren_alternative = filtered_data.iloc[selected_indices_alternative]
    print("\n备用方案的达人:")
    print(selected_daren_alternative[['昵称', '内容垂类']])
    print(f"总报价: {sum(selected_daren_alternative['60s以上视频报价'])}元")
    print(f"总预期播放量: {sum(selected_daren_alternative['预期播放量'])}")
else:
    print("没有找到备用方案的最优解。")
