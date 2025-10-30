"""参数验证工具"""
import re
from typing import List, Optional


def validate_stock_symbol(symbol: str) -> bool:
    """
    验证股票代码格式
    A股代码：6位数字
    """
    if not symbol:
        return False
    
    # 移除可能的空格
    symbol = symbol.strip()
    
    # 检查是否为6位数字
    pattern = r'^\d{6}$'
    return bool(re.match(pattern, symbol))


def validate_stock_symbols(symbols: List[str], max_count: int = 20) -> tuple[bool, Optional[str]]:
    """
    验证股票代码列表
    
    Args:
        symbols: 股票代码列表
        max_count: 最大数量限制
    
    Returns:
        (is_valid, error_message)
    """
    if not symbols:
        return False, "股票代码列表不能为空"
    
    if len(symbols) > max_count:
        return False, f"股票代码数量超过限制（最多{max_count}个）"
    
    invalid_symbols = []
    for symbol in symbols:
        if not validate_stock_symbol(symbol):
            invalid_symbols.append(symbol)
    
    if invalid_symbols:
        return False, f"以下股票代码格式不正确: {', '.join(invalid_symbols)}"
    
    return True, None


def validate_period(period: str) -> bool:
    """验证报告期类型"""
    valid_periods = ["quarter", "annual"]
    return period in valid_periods


def validate_indicator_type(indicator_type: str) -> bool:
    """验证指标类型"""
    valid_types = ["basic", "profit", "growth", "debt", "operation", "all"]
    return indicator_type in valid_types


def validate_file_format(file_format: str) -> bool:
    """验证文件格式"""
    valid_formats = ["csv", "excel", "json"]
    return file_format in valid_formats


def normalize_symbol(symbol: str) -> str:
    """标准化股票代码（移除空格等）"""
    return symbol.strip()


def normalize_symbols(symbols: List[str]) -> List[str]:
    """标准化股票代码列表"""
    return [normalize_symbol(s) for s in symbols]