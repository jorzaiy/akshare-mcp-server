"""文件管理工具"""
import os
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
import json


class FileManager:
    """文件管理器"""
    
    def __init__(self, base_path: str):
        """
        初始化文件管理器
        
        Args:
            base_path: 基础路径
        """
        self.base_path = Path(base_path)
        self.exports_dir = self.base_path / "data" / "exports"
        self.cache_dir = self.base_path / "data" / "cache"
        self.batch_dir = self.base_path / "data" / "batch"
        self.logs_dir = self.base_path / "logs"
        
        # 确保目录存在
        self.setup_directories()
    
    def setup_directories(self):
        """创建必要的目录"""
        for directory in [self.exports_dir, self.cache_dir, self.batch_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def generate_filename(
        self, 
        file_type: str, 
        symbols: List[str] = None, 
        format: str = "csv"
    ) -> str:
        """
        生成文件名
        
        Args:
            file_type: 文件类型（batch, export, cache等）
            symbols: 股票代码列表
            format: 文件格式
        
        Returns:
            文件名
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if symbols:
            # 限制文件名长度
            if len(symbols) <= 3:
                symbols_str = "_".join(symbols)
            else:
                symbols_str = f"{symbols[0]}_and_{len(symbols)-1}_more"
        else:
            symbols_str = "data"
        
        ext = "xlsx" if format == "excel" else format
        filename = f"{file_type}_{symbols_str}_{timestamp}.{ext}"
        
        return filename
    
    def save_dataframe(
        self,
        df: pd.DataFrame,
        file_type: str,
        symbols: List[str] = None,
        format: str = "csv",
        output_path: str = None
    ) -> str:
        """
        保存DataFrame到文件
        
        Args:
            df: 数据
            file_type: 文件类型
            symbols: 股票代码列表
            format: 文件格式
            output_path: 自定义输出路径
        
        Returns:
            文件路径
        """
        if df is None or df.empty:
            raise ValueError("数据为空，无法保存")
        
        # 确定保存目录
        if output_path:
            file_path = Path(output_path)
        else:
            if file_type == "export":
                save_dir = self.exports_dir
            elif file_type == "batch":
                save_dir = self.batch_dir
            else:
                save_dir = self.cache_dir
            
            filename = self.generate_filename(file_type, symbols, format)
            file_path = save_dir / filename
        
        # 确保父目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        try:
            if format == "csv":
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
            elif format == "excel":
                df.to_excel(file_path, index=False, engine='openpyxl')
            elif format == "json":
                df.to_json(file_path, orient='records', force_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的文件格式: {format}")
            
            return str(file_path)
        except Exception as e:
            raise Exception(f"保存文件失败: {str(e)}")
    
    def save_json(self, data: dict, file_type: str, symbols: List[str] = None, output_path: str = None) -> str:
        """
        保存JSON数据到文件
        
        Args:
            data: 字典数据
            file_type: 文件类型
            symbols: 股票代码列表
            output_path: 自定义输出路径
        
        Returns:
            文件路径
        """
        if output_path:
            file_path = Path(output_path)
        else:
            save_dir = self.cache_dir if file_type == "cache" else self.exports_dir
            filename = self.generate_filename(file_type, symbols, "json")
            file_path = save_dir / filename
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return str(file_path)
        except Exception as e:
            raise Exception(f"保存JSON文件失败: {str(e)}")
    
    def cleanup_old_files(self, max_age_days: int = 7, directory: str = "cache"):
        """
        清理过期文件
        
        Args:
            max_age_days: 最大保留天数
            directory: 目录类型（cache, batch）
        """
        if directory == "cache":
            target_dir = self.cache_dir
        elif directory == "batch":
            target_dir = self.batch_dir
        else:
            return
        
        if not target_dir.exists():
            return
        
        cutoff_time = datetime.now() - timedelta(days=max_age_days)
        deleted_count = 0
        
        try:
            for file_path in target_dir.iterdir():
                if file_path.is_file():
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_mtime < cutoff_time:
                        file_path.unlink()
                        deleted_count += 1
            
            return deleted_count
        except Exception as e:
            print(f"清理文件时出错: {str(e)}")
            return 0
    
    def get_directory_size(self, directory: str = "all") -> int:
        """
        获取目录大小（字节）
        
        Args:
            directory: 目录类型（cache, batch, exports, all）
        
        Returns:
            目录大小（字节）
        """
        if directory == "all":
            dirs = [self.cache_dir, self.batch_dir, self.exports_dir]
        elif directory == "cache":
            dirs = [self.cache_dir]
        elif directory == "batch":
            dirs = [self.batch_dir]
        elif directory == "exports":
            dirs = [self.exports_dir]
        else:
            return 0
        
        total_size = 0
        for dir_path in dirs:
            if dir_path.exists():
                for file_path in dir_path.rglob('*'):
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
        
        return total_size
    
    def list_files(self, directory: str = "exports", limit: int = 10) -> List[dict]:
        """
        列出目录中的文件
        
        Args:
            directory: 目录类型
            limit: 返回数量限制
        
        Returns:
            文件信息列表
        """
        if directory == "exports":
            target_dir = self.exports_dir
        elif directory == "batch":
            target_dir = self.batch_dir
        elif directory == "cache":
            target_dir = self.cache_dir
        else:
            return []
        
        if not target_dir.exists():
            return []
        
        files = []
        for file_path in sorted(target_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size_bytes": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return files