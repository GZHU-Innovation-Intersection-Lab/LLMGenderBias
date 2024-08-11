import pandas as pd
from scipy.stats import kruskal

# 从Excel文件读取数据
file_path = "E:\Desktop\性别偏见\数据分析\工作簿2.xlsx"
df = pd.read_excel(file_path, header=None)

# 提取方法、语言和维度信息
methods = df.iloc[0, :].values
languages = df.iloc[1, :].values
dimensions = df.iloc[2, :].values

# 提取得分数据
scores = df.iloc[3:, :].values

# 创建一个长格式的数据框架
data = {
    '方法': [],
    '语言': [],
    '维度': [],
    '得分': []
}

for col in range(df.shape[1]):
    method = methods[col]
    language = languages[col]
    dimension = dimensions[col]
    for score in scores[:, col]:
        data['方法'].append(method)
        data['语言'].append(language)
        data['维度'].append(dimension)
        data['得分'].append(score)

df_long = pd.DataFrame(data)

# 对每个维度分别进行Kruskal-Wallis H检验
for dimension in ['偏男性', '偏女性', '中性']:
    subset = df_long[df_long['维度'] == dimension]
    scores = [subset[subset['方法'] == method]['得分'].values for method in subset['方法'].unique()]
    
    # 进行Kruskal-Wallis H检验
    stat, p = kruskal(*scores)
    print(f"维度: {dimension}, Kruskal-Wallis H统计量: {stat}, p值: {p}")

    if p < 0.05:
        print(f"在维度 {dimension} 上，不同方法的数据分布显著不同（p < 0.05）。")
    else:
        print(f"在维度 {dimension} 上，不同方法的数据分布没有显著差异（p >= 0.05）。")
