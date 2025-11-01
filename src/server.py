#!/usr/bin/env python3
"""AKShare股票财务数据MCP服务器"""
import sys
import os
import asyncio

# 添加项目根目录到Python路径，以便可以导入src包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src.tools import (
    get_stock_financial_indicators,
    get_stock_balance_sheet,
    get_stock_income_statement,
    get_stock_cash_flow,
    get_stock_main_indicators,
    get_batch_stock_indicators,
    export_data_to_file,
    search_stock,
    get_all_stocks
)

# 创建MCP服务器实例
server = Server("akshare-stock-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="get_stock_financial_indicators",
            description="获取股票的财务指标数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码（6位数字，如 000001 或 600519）"
                    },
                    "indicator_type": {
                        "type": "string",
                        "enum": ["basic", "profit", "growth", "debt", "operation", "all"],
                        "description": "指标类型：basic(基本财务指标)、profit(盈利能力)、growth(成长能力)、debt(偿债能力)、operation(运营能力)、all(所有指标，默认)",
                        "default": "all"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_stock_balance_sheet",
            description="获取股票的资产负债表",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码（6位数字）"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["quarter", "annual"],
                        "description": "报告期类型：quarter(季度报告)、annual(年度报告，默认)",
                        "default": "annual"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_stock_income_statement",
            description="获取股票的利润表",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码（6位数字）"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["quarter", "annual"],
                        "description": "报告期类型：quarter(季度报告)、annual(年度报告，默认)",
                        "default": "annual"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_stock_cash_flow",
            description="获取股票的现金流量表",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码（6位数字）"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["quarter", "annual"],
                        "description": "报告期类型：quarter(季度报告)、annual(年度报告，默认)",
                        "default": "annual"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_stock_main_indicators",
            description="获取股票的主要财务指标（包括市盈率、市净率、ROE、营收、净利润等关键指标）",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码（6位数字）"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_batch_stock_indicators",
            description="批量获取多个股票的财务指标（最多20个股票）",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "股票代码列表（如 [\"000001\", \"600000\", \"600519\"]），最多20个"
                    },
                    "indicator_type": {
                        "type": "string",
                        "enum": ["basic", "profit", "growth", "debt", "operation", "all"],
                        "description": "指标类型",
                        "default": "all"
                    },
                    "save_to_file": {
                        "type": "boolean",
                        "description": "是否保存到文件",
                        "default": False
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出文件路径（可选）"
                    },
                    "file_format": {
                        "type": "string",
                        "enum": ["csv", "excel", "json"],
                        "description": "文件格式",
                        "default": "csv"
                    }
                },
                "required": ["symbols"]
            }
        ),
        Tool(
            name="export_data_to_file",
            description="导出查询结果到文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_type": {
                        "type": "string",
                        "enum": ["indicators", "balance_sheet", "income", "cash_flow"],
                        "description": "数据类型：indicators(财务指标)、balance_sheet(资产负债表)、income(利润表)、cash_flow(现金流量表)"
                    },
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出文件路径"
                    },
                    "file_format": {
                        "type": "string",
                        "enum": ["csv", "excel", "json"],
                        "description": "文件格式",
                        "default": "csv"
                    }
                },
                "required": ["data_type", "symbol", "output_path"]
            }
        ),
        Tool(
            name="search_stock",
            description="搜索股票（通过股票代码或名称）",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词（股票代码或名称）"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_all_stocks",
            description="获取所有A股股票列表",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""
    try:
        result = None
        
        if name == "get_stock_financial_indicators":
            result = get_stock_financial_indicators(
                symbol=arguments["symbol"],
                indicator_type=arguments.get("indicator_type", "all")
            )
        
        elif name == "get_stock_balance_sheet":
            result = get_stock_balance_sheet(
                symbol=arguments["symbol"],
                period=arguments.get("period", "annual")
            )
        
        elif name == "get_stock_income_statement":
            result = get_stock_income_statement(
                symbol=arguments["symbol"],
                period=arguments.get("period", "annual")
            )
        
        elif name == "get_stock_cash_flow":
            result = get_stock_cash_flow(
                symbol=arguments["symbol"],
                period=arguments.get("period", "annual")
            )
        
        elif name == "get_stock_main_indicators":
            result = get_stock_main_indicators(
                symbol=arguments["symbol"]
            )
        
        elif name == "get_batch_stock_indicators":
            result = await get_batch_stock_indicators(
                symbols=arguments["symbols"],
                indicator_type=arguments.get("indicator_type", "all"),
                save_to_file=arguments.get("save_to_file", False),
                output_path=arguments.get("output_path"),
                file_format=arguments.get("file_format", "csv")
            )
        
        elif name == "export_data_to_file":
            result = export_data_to_file(
                data_type=arguments["data_type"],
                symbol=arguments["symbol"],
                output_path=arguments["output_path"],
                file_format=arguments.get("file_format", "csv")
            )
        
        elif name == "search_stock":
            result = search_stock(
                query=arguments["query"]
            )
        
        elif name == "get_all_stocks":
            result = get_all_stocks()
        
        else:
            result = f"未知工具: {name}"
        
        return [TextContent(type="text", text=result)]
    
    except Exception as e:
        import traceback
        error_msg = f"工具执行失败: {str(e)}\n{traceback.format_exc()}"
        return [TextContent(type="text", text=error_msg)]


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)