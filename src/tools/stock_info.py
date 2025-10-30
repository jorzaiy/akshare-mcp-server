"""股票信息和搜索工具"""
import akshare as ak
import pandas as pd
from src.utils import format_dataframe_to_json, format_error


def search_stock(query: str) -> str:
    """
    搜索股票
    
    Args:
        query: 搜索关键词（股票代码或名称）
    
    Returns:
        JSON格式的股票列表
    """
    try:
        if not query or len(query.strip()) == 0:
            return format_error("搜索关键词不能为空")
        
        query = query.strip()
        
        # 获取A股股票列表
        df = ak.stock_info_a_code_name()
        
        if df is None or df.empty:
            return format_error("获取股票列表失败")
        
        # 搜索匹配的股票
        # 可以匹配代码或名称
        mask = (
            df['code'].astype(str).str.contains(query, case=False, na=False) |
            df['name'].str.contains(query, case=False, na=False)
        )
        
        result_df = df[mask]
        
        if result_df.empty:
            return format_dataframe_to_json(pd.DataFrame({
                "message": [f"未找到匹配 '{query}' 的股票"]
            }))
        
        # 限制返回数量
        if len(result_df) > 50:
            result_df = result_df.head(50)
            # 添加提示信息
        
        return format_dataframe_to_json(result_df)
        
    except Exception as e:
        return format_error(f"搜索股票失败: {str(e)}")


def get_all_stocks() -> str:
    """
    获取所有A股股票列表
    
    Returns:
        JSON格式的股票列表
    """
    try:
        df = ak.stock_info_a_code_name()
        
        if df is None or df.empty:
            return format_error("获取股票列表失败")
        
        return format_dataframe_to_json(df)
        
    except Exception as e:
        return format_error(f"获取股票列表失败: {str(e)}")