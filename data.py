import pandas as pd

# 读取 Excel 文件
file_path = r"D:\Synergence\Disi\data\merged_modified_files.xlsx"
influencer_data = pd.read_excel(file_path)

# 删除等级列中的汉字，保留字母
influencer_data['等级'] = influencer_data['等级'].str.replace('[^\x00-\x7F]+', '', regex=True)

# 保存修改后的数据到新的 Excel 文件
modified_file_path = r"D:\Synergence\Disi\data\test2.xlsx"
influencer_data.to_excel(modified_file_path, index=False)

modified_file_path
