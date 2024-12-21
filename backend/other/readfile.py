import pyarrow
import fastparquet
import pandas as pd

# 读取 .parquet 文件并输出条目数和字段信息
def inspect_parquet(file_path):
    # 读取文件
    df = pd.read_parquet(file_path)
    # 输出条目数（行数）和字段信息（列名）
    print(f"文件 {file_path} 包含 {df.shape[0]} 条数据")
    print(f"数据字段为: {df.columns.tolist()}")

    df = pd.read_parquet(file_path)

    # 打印前100条数据
    print(df.head(100))

    # 将前100行数据保存为 CSV 文件
    csv_file_path = r'C:\Users\Ye\Desktop\数据库课设项目\data\archive\fundamentals_processed_first_100_rows.csv'  # 替换为你希望保存的路径
    df.head(100).to_csv(csv_file_path, index=False)

# 调用方法，将路径改为待读取的文件路径
inspect_parquet(r"C:\Users\Ye\Desktop\数据库课设项目\data\archive\fundamentals_processed.parquet")

