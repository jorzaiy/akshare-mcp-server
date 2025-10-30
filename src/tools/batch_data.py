"""批量数据查询工具"""
import akshare as ak
import pandas as pd
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor
from src.utils import (
    validate_stock_symbols,
    validate_indicator_type,
    validate_file_format,
    normalize_symbols,
    format_batch_results,
    format_error,
    simplify_financial_data,
    format_file_info,
    FileManager
)
import os


def _fetch_single_stock_data(symbol: str, indicator_type: str = "all") -> dict:
    """
    获取单个股票的财务指标
    
    Args:
        symbol: 股票代码
        indicator_type: 指标类型
    
    Returns:
        包含股票数据或错误信息的字典
    """
    try:
        df = ak.stock_financial_analysis_indicator(symbol=symbol)
        
        if df is None or df.empty:
            return {
                "symbol": symbol,
                "error": "未找到数据",
                "data": None
            }
        
        # 简化数据
        df = simplify_financial_data(df, indicator_type)
        
        # 转换为字典
        data = df.to_dict(orient='records')
        
        return {
            "symbol": symbol,
            "data": data,
            "count": len(data)
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e),
            "data": None
        }


async def get_batch_stock_indicators(
    symbols: List[str],
    indicator_type: str = "all",
    save_to_file: bool = False,
    output_path: str = None,
    file_format: str = "csv"
) -> str:
    """
    批量获取股票财务指标
    
    Args:
        symbols: 股票代码列表
        indicator_type: 指标类型
        save_to_file: 是否保存到文件
        output_path: 输出文件路径
        file_format: 文件格式
    
    Returns:
        JSON格式的批量结果
    """
    try:
        # 标准化股票代码
        symbols = normalize_symbols(symbols)
        
        # 验证参数
        is_valid, error_msg = validate_stock_symbols(symbols, max_count=20)
        if not is_valid:
            return format_error(error_msg)
        
        if not validate_indicator_type(indicator_type):
            return format_error(f"指标类型不正确: {indicator_type}")
        
        if save_to_file and not validate_file_format(file_format):
            return format_error(f"文件格式不正确: {file_format}")
        
        # 使用线程池并发查询（AKShare是同步的）
        with ThreadPoolExecutor(max_workers=5) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    _fetch_single_stock_data,
                    symbol,
                    indicator_type
                )
                for symbol in symbols
            ]
            results = await asyncio.gather(*tasks)
        
        # 如果需要保存到文件
        if save_to_file:
            # 合并所有成功的数据
            all_data = []
            for result in results:
                if result.get("data"):
                    for record in result["data"]:
                        record["股票代码"] = result["symbol"]
                        all_data.append(record)
            
            if all_data:
                df = pd.DataFrame(all_data)
                
                # 获取文件管理器
                base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                file_manager = FileManager(base_path)
                
                # 保存文件
                file_path = file_manager.save_dataframe(
                    df=df,
                    file_type="batch",
                    symbols=symbols,
                    format=file_format,
                    output_path=output_path
                )
                
                # 添加文件信息到结果
                file_info = format_file_info(file_path, len(all_data))
                
                return format_batch_results(results) + f"\n\n文件已保存:\n{file_info}"
        
        return format_batch_results(results)
        
    except Exception as e:
        return format_error(f"批量查询失败: {str(e)}")