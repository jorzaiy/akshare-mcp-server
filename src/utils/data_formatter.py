"""数据格式化工具"""
import pandas as pd
import json
from typing import Dict, Any, List
from datetime import datetime


def format_dataframe_to_json(df: pd.DataFrame) -> str:
    """
    将DataFrame转换为JSON字符串
    
    Args:
        df: pandas DataFrame
    
    Returns:
        格式化的JSON字符串
    """
    if df is None or df.empty:
        return json.dumps({"data": [], "message": "无数据"}, ensure_ascii=False, indent=2)
    
    # 处理NaN值
    df = df.fillna("")
    
    # 转换为字典列表
    data = df.to_dict(orient='records')
    
    result = {
        "data": data,
        "count": len(data),
        "columns": list(df.columns),
        "timestamp": datetime.now().isoformat()
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)


def format_dict_to_json(data: Dict[str, Any]) -> str:
    """
    将字典转换为JSON字符串
    
    Args:
        data: 字典数据
    
    Returns:
        格式化的JSON字符串
    """
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_batch_results(results: List[Dict[str, Any]]) -> str:
    """
    格式化批量查询结果
    
    Args:
        results: 查询结果列表
    
    Returns:
        格式化的JSON字符串
    """
    success_count = sum(1 for r in results if 'error' not in r)
    failed_count = len(results) - success_count
    
    formatted = {
        "total": len(results),
        "success": success_count,
        "failed": failed_count,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }
    
    return json.dumps(formatted, ensure_ascii=False, indent=2)


def format_error(error_message: str, symbol: str = None) -> str:
    """
    格式化错误消息
    
    Args:
        error_message: 错误消息
        symbol: 股票代码（可选）
    
    Returns:
        格式化的错误JSON字符串
    """
    error_data = {
        "error": True,
        "message": error_message,
        "timestamp": datetime.now().isoformat()
    }
    
    if symbol:
        error_data["symbol"] = symbol
    
    return json.dumps(error_data, ensure_ascii=False, indent=2)


def simplify_financial_data(df: pd.DataFrame, indicator_type: str = "all") -> pd.DataFrame:
    """
    根据指标类型简化财务数据
    
    Args:
        df: 原始数据
        indicator_type: 指标类型
    
    Returns:
        简化后的DataFrame
    """
    if df is None or df.empty:
        return df
    
    # 根据不同类型选择关键列
    key_columns = {
        "basic": ["股票代码", "股票名称", "市盈率", "市净率", "市销率", "总市值"],
        "profit": ["股票代码", "股票名称", "净利润", "净利润同比", "营业收入", "营业收入同比", "毛利率", "净利率"],
        "growth": ["股票代码", "股票名称", "营业收入同比", "净利润同比", "营业收入环比", "净利润环比"],
        "debt": ["股票代码", "股票名称", "资产负债率", "流动比率", "速动比率"],
        "operation": ["股票代码", "股票名称", "总资产周转率", "存货周转率", "应收账款周转率"]
    }
    
    if indicator_type != "all" and indicator_type in key_columns:
        # 选择存在的列
        available_columns = [col for col in key_columns[indicator_type] if col in df.columns]
        if available_columns:
            return df[available_columns]
    
    return df


def format_file_info(file_path: str, record_count: int, file_size: int = None) -> str:
    """
    格式化文件信息
    
    Args:
        file_path: 文件路径
        record_count: 记录数
        file_size: 文件大小（字节）
    
    Returns:
        格式化的JSON字符串
    """
    import os
    
    if file_size is None and os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
    
    info = {
        "file_path": file_path,
        "record_count": record_count,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2) if file_size else None,
        "timestamp": datetime.now().isoformat()
    }
    
    return json.dumps(info, ensure_ascii=False, indent=2)