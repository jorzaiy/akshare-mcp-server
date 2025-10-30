# AKShare 股票财务数据 MCP 服务器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

基于 [AKShare](https://github.com/akfamily/akshare) 的 A 股股票财务数据查询 MCP (Model Context Protocol) 服务器，支持批量查询和多格式数据导出。

## ✨ 功能特性

- 🔍 **单个股票财务指标查询** - 获取详细的财务分析指标
- 📊 **三大财务报表** - 资产负债表、利润表、现金流量表
- 🚀 **批量查询** - 一次查询最多 20 个股票
- 💾 **多格式导出** - 支持 CSV、Excel、JSON 格式
- 🔎 **股票搜索** - 通过代码或名称快速搜索
- 🆓 **无需 API 密钥** - 使用公开数据源

## 📦 安装

### 方式一：使用 UVX（推荐）⭐

UVX 是最简单的安装方式，自动管理依赖和虚拟环境。

#### 1. 安装 UV

```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. 配置 MCP 服务器

在 MCP 客户端配置中添加：

```json
{
  "mcpServers": {
    "akshare-stock": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jorzaiy/akshare-mcp-server.git",
        "akshare-mcp-server"
      ]
    }
  }
}
```

#### 3. 本地开发配置

如果你克隆了仓库进行本地开发：

```json
{
  "mcpServers": {
    "akshare-stock": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\akshare-mcp-server",
        "run",
        "akshare-mcp-server"
      ]
    }
  }
}
```

### 方式二：传统 Python 方式

#### 1. 克隆仓库

```bash
git clone https://github.com/jorzaiy/akshare-mcp-server.git
cd akshare-stock-server
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置 MCP 服务器

在 Kilo Code 或其他支持 MCP 的客户端中添加服务器配置：

```json
{
  "mcpServers": {
    "akshare-stock": {
      "command": "python",
      "args": [
        "/path/to/akshare-stock-server/src/server.py"
      ],
      "env": {},
      "disabled": false
    }
  }
}
```

**Windows 示例路径**:
```json
"C:\\Users\\YourName\\akshare-stock-server\\src\\server.py"
```

**macOS/Linux 示例路径**:
```json
"/home/username/akshare-stock-server/src/server.py"
```

## 🛠️ 可用工具

### 1. `get_stock_financial_indicators`
获取股票的详细财务指标

**参数**:
- `symbol` (必需): 股票代码，如 "600519"
- `indicator_type` (可选): 指标类型
  - `basic` - 基本财务指标
  - `profit` - 盈利能力指标
  - `growth` - 成长能力指标
  - `debt` - 偿债能力指标
  - `operation` - 运营能力指标
  - `all` - 所有指标（默认）

### 2. `get_stock_balance_sheet`
获取资产负债表

**参数**:
- `symbol` (必需): 股票代码
- `period` (可选): 报告期类型
  - `quarter` - 季度报告
  - `annual` - 年度报告（默认）

### 3. `get_stock_income_statement`
获取利润表

**参数**:
- `symbol` (必需): 股票代码
- `period` (可选): `quarter` 或 `annual`（默认）

### 4. `get_stock_cash_flow`
获取现金流量表

**参数**:
- `symbol` (必需): 股票代码
- `period` (可选): `quarter` 或 `annual`（默认）

### 5. `get_stock_main_indicators`
获取股票主要财务指标（市盈率、市净率、ROE等）

**参数**:
- `symbol` (必需): 股票代码

### 6. `get_batch_stock_indicators`
批量获取多个股票的财务指标（最多20个）

**参数**:
- `symbols` (必需): 股票代码列表，如 `["000001", "600519"]`
- `indicator_type` (可选): 指标类型（同上）
- `save_to_file` (可选): 是否保存到文件，默认 `false`
- `output_path` (可选): 输出文件路径
- `file_format` (可选): 文件格式 - `csv`、`excel` 或 `json`（默认 `csv`）

### 7. `export_data_to_file`
将查询结果导出到文件

**参数**:
- `data_type` (必需): 数据类型
  - `indicators` - 财务指标
  - `balance_sheet` - 资产负债表
  - `income` - 利润表
  - `cash_flow` - 现金流量表
- `symbol` (必需): 股票代码
- `output_path` (必需): 输出文件路径
- `file_format` (可选): 文件格式（默认 `csv`）

### 8. `search_stock`
搜索股票

**参数**:
- `query` (必需): 搜索关键词（股票代码或名称）

## 📝 使用示例

配置完成后，可以通过 AI 助手使用自然语言查询：

```
获取贵州茅台(600519)的主要财务指标
```

```
批量查询平安银行(000001)、招商银行(600036)、贵州茅台(600519)的财务数据，并保存为CSV
```

```
搜索名称包含"银行"的股票
```

```
导出工商银行(601398)的资产负债表为Excel格式
```

## 📂 项目结构

```
akshare-stock-server/
├── src/
│   ├── server.py              # MCP 服务器主入口
│   ├── tools/                 # 工具模块
│   │   ├── financial_data.py  # 财务数据查询
│   │   ├── batch_data.py      # 批量数据查询
│   │   ├── export_data.py     # 数据导出
│   │   └── stock_info.py      # 股票信息和搜索
│   └── utils/                 # 工具函数
│       ├── validators.py      # 参数验证
│       ├── data_formatter.py  # 数据格式化
│       └── file_manager.py    # 文件管理
├── data/                      # 数据存储目录
│   ├── exports/              # 用户导出的文件
│   ├── batch/                # 批量查询结果
│   └── cache/                # 临时缓存（7天自动清理）
├── requirements.txt          # Python 依赖
├── README.md                 # 项目说明
└── LICENSE                   # MIT 许可证
```

## 🔧 故障排查

### MCP 连接错误

如果遇到 "Connection closed -32000" 错误：

1. **检查依赖安装**:
```bash
pip install -r requirements.txt
```

2. **验证服务器启动**:
```bash
python src/server.py
```
应该看到服务器成功启动（无错误输出）

3. **检查路径配置**: 确保 MCP 配置中的路径正确且绝对路径

## 📊 数据存储

- **导出文件**: `data/exports/` - 用户手动导出的数据
- **批量查询**: `data/batch/` - 批量查询结果
- **缓存数据**: `data/cache/` - 临时缓存（7天自动清理）

## ⚠️ 注意事项

- AKShare 数据源为公开数据，使用时请遵守相关使用条款
- 某些财务数据可能存在更新延迟
- 建议在非交易时段进行大量数据查询，避免对数据源造成压力
- 批量查询限制为每次最多 20 个股票

## 🛠️ 技术栈

- **Python 3.8+** - 编程语言
- **MCP SDK** - Model Context Protocol 实现
- **AKShare** - A 股数据获取库
- **Pandas** - 数据处理
- **asyncio** - 异步处理

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🙏 致谢

- [AKShare](https://github.com/akfamily/akshare) - 提供数据源
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol

## 📮 联系方式

如有问题或建议，请提交 [Issue](https://github.com/your-username/akshare-stock-server/issues)。

---

**版本**: v1.0.0
