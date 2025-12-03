#!/usr/bin/env python3
"""
JSONファイルを整形するスクリプト
オブジェクトは展開するが、内部の配列（sides等）は1行に保つ
"""
import json
import sys
from pathlib import Path
import re

def format_json_with_compact_arrays(file_path: str):
    """
    JSONファイルを読み込んで整形し、上書き保存
    オブジェクトは展開、配列は1行形式
    """
    path = Path(file_path)
    
    if not path.exists():
        print(f"❌ ファイルが見つかりません: {file_path}")
        return False
    
    try:
        # JSONファイル読み込み
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # まず通常のインデント付きで整形
        formatted = json.dumps(data, ensure_ascii=False, indent=2)
        
        # 配列部分を1行に圧縮する正規表現
        # [\n      数値,\n      数値\n    ] を [数値, 数値] に変換
        formatted = re.sub(
            r'\[\s*(\d+),\s*(\d+),\s*(\d+)\s*\]',
            r'[\1, \2, \3]',
            formatted
        )
        
        # ファイルに書き込み
        with open(path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        print(f"✅ 整形完了: {file_path}")
        print(f"   オブジェクト: 展開")
        print(f"   配列: 1行に圧縮")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python scripts/format_json.py <jsonファイルパス>")
        print("例: python scripts/format_json.py app/resources/monthly_menu.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = format_json_with_compact_arrays(file_path)
    sys.exit(0 if success else 1)
