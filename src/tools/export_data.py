"""数据导出工具"""
import akshare as ak
import pandas as pd
import os
from src.utils import (
    validate_stock_symbol,
    validate_file_format,
    format_error,
    format_file_info,
    FileManager
)


def export_data_to_file(
    data_type: str,
    symbol: str,
    output_path: str,
    file_format: str = "csv"
) -> str:
    """
    导出查询结果到文件
    
    Args:
        data_type: 数据类型 (indicators/balance_sheet/income/cash_flow)
        symbol: 股票代码
        output_path: 输出文件路径
        file_format: 文件格式 (csv/excel/json)
    
    Returns:
        JSON格式的导出结果
    """
    try:
        # 验证参数
        if not validate_stock_symbol(symbol):
            return format_error(f"股票代码格式不正确: {symbol}")
        
        if not validate_file_format(file_format):
            return format_error(f"文件格式不正确: {file_format}")
        
        valid_types = ["indicators", "balance_sheet", "income", "cash_flow"]
        if data_type not in valid_types:
            return format_error(f"数据类型不正确: {data_type}，有效值: {', '.join(valid_types)}")
        
        # 根据数据类型获取数据
        df = None
        if data_type == "indicators":
            df = ak.stock_financial_analysis_indicator(symbol=symbol)
        elif data_type == "balance_sheet":
            df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        elif data_type == "income":
            df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        elif data_type == "cash_flow":
            df = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        
        if df is None or df.empty:
            return format_error(f"未找到股票 {symbol} 的 {data_type} 数据")
        
        # 获取文件管理器
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_manager = FileManager(base_path)
        
        # 保存文件
        file_path = file_manager.save_dataframe(
            df=df,
            file_type="export",
            symbols=[symbol],
            format=file_format,
            output_path=output_path
        )
        
        # 返回文件信息
        return format_file_info(file_path, len(df))
        
    except Exception as e:
        return format_error(f"导出数据失败: {str(e)}", symbol)