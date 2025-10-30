"""财务数据查询工具"""
import akshare as ak
import pandas as pd
from typing import Optional
from src.utils import (
    validate_stock_symbol,
    validate_period,
    validate_indicator_type,
    format_dataframe_to_json,
    format_error,
    simplify_financial_data
)


def get_stock_financial_indicators(symbol: str, indicator_type: str = "all") -> str:
    """
    获取股票财务指标
    
    Args:
        symbol: 股票代码
        indicator_type: 指标类型
    
    Returns:
        JSON格式的财务指标数据
    """
    try:
        # 验证参数
        if not validate_stock_symbol(symbol):
            return format_error(f"股票代码格式不正确: {symbol}")
        
        if not validate_indicator_type(indicator_type):
            return format_error(f"指标类型不正确: {indicator_type}")
        
        # 调用AKShare接口获取财务指标
        df = ak.stock_financial_analysis_indicator(symbol=symbol)
        
        if df is None or df.empty:
            return format_error(f"未找到股票 {symbol} 的财务指标数据")
        
        # 根据指标类型简化数据
        df = simplify_financial_data(df, indicator_type)
        
        # 转换为JSON
        return format_dataframe_to_json(df)
        
    except Exception as e:
        return format_error(f"获取财务指标失败: {str(e)}", symbol)


def get_stock_balance_sheet(symbol: str, period: str = "annual") -> str:
    """
    获取资产负债表
    
    Args:
        symbol: 股票代码
        period: 报告期类型（quarter/annual）
    
    Returns:
        JSON格式的资产负债表数据
    """
    try:
        if not validate_stock_symbol(symbol):
            return format_error(f"股票代码格式不正确: {symbol}")
        
        if not validate_period(period):
            return format_error(f"报告期类型不正确: {period}")
        
        # 调用AKShare接口
        df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        
        if df is None or df.empty:
            return format_error(f"未找到股票 {symbol} 的资产负债表数据")
        
        # 如果指定季度报告，筛选季度数据
        if period == "quarter" and "报告期" in df.columns:
            # 筛选季度报告（通常包含Q1, Q2, Q3, Q4）
            df = df[df["报告期"].str.contains("Q", na=False)]
        
        return format_dataframe_to_json(df)
        
    except Exception as e:
        return format_error(f"获取资产负债表失败: {str(e)}", symbol)


def get_stock_income_statement(symbol: str, period: str = "annual") -> str:
    """
    获取利润表
    
    Args:
        symbol: 股票代码
        period: 报告期类型（quarter/annual）
    
    Returns:
        JSON格式的利润表数据
    """
    try:
        if not validate_stock_symbol(symbol):
            return format_error(f"股票代码格式不正确: {symbol}")
        
        if not validate_period(period):
            return format_error(f"报告期类型不正确: {period}")
        
        # 调用AKShare接口
        df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        
        if df is None or df.empty:
            return format_error(f"未找到股票 {symbol} 的利润表数据")
        
        # 如果指定季度报告，筛选季度数据
        if period == "quarter" and "报告期" in df.columns:
            df = df[df["报告期"].str.contains("Q", na=False)]
        
        return format_dataframe_to_json(df)
        
    except Exception as e:
        return format_error(f"获取利润表失败: {str(e)}", symbol)


def get_stock_cash_flow(symbol: str, period: str = "annual") -> str:
    """
    获取现金流量表
    
    Args:
        symbol: 股票代码
        period: 报告期类型（quarter/annual）
    
    Returns:
        JSON格式的现金流量表数据
    """
    try:
        if not validate_stock_symbol(symbol):
            return format_error(f"股票代码格式不正确: {symbol}")
        
        if not validate_period(period):
            return format_error(f"报告期类型不正确: {period}")
        
        # 调用AKShare接口
        df = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        
        if df is None or df.empty:
            return format_error(f"未找到股票 {symbol} 的现金流量表数据")
        
        # 如果指定季度报告，筛选季度数据
        if period == "quarter" and "报告期" in df.columns:
            df = df[df["报告期"].str.contains("Q", na=False)]
        
        return format_dataframe_to_json(df)
        
    except Exception as e:
        return format_error(f"获取现金流量表失败: {str(e)}", symbol)


def get_stock_main_indicators(symbol: str) -> str:
    """
    获取股票主要财务指标
    
    Args:
        symbol: 股票代码
    
    Returns:
        JSON格式的主要指标数据
    """
    try:
        if not validate_stock_symbol(symbol):
            return format_error(f"股票代码格式不正确: {symbol}")
        
        # 调用AKShare接口获取个股信息
        df = ak.stock_individual_info_em(symbol=symbol)
        
        if df is None or df.empty:
            return format_error(f"未找到股票 {symbol} 的主要指标数据")
        
        return format_dataframe_to_json(df)
        
    except Exception as e:
        return format_error(f"获取主要指标失败: {str(e)}", symbol)