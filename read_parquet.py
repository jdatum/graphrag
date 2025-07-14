#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
フォルダ配下の Parquet ファイル一覧を調べて
  - 列名リスト
  - 総行数
を表示するユーティリティ
"""

from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd

# --- 設定 ------------------------------------------------------------
# 解析したいフォルダのパスを絶対／相対で指定
TARGET_DIR = "voc_test/output"
HEAD_ROWS  = 5   
# ---------------------------------------------------------------------

def inspect_parquet_file(pfile: Path) -> tuple[list[str], int]:
    """
    Parquet ファイル 1 つを調べて (列名リスト, 行数) を返す
    """
    pf = pq.ParquetFile(pfile)
    cols = pf.schema.names               # 列名
    num_rows = pf.metadata.num_rows      # 総行数
    return cols, num_rows

def preview_parquet_file(pfile: Path, n: int = 5) -> pd.DataFrame:
    """DataFrame の先頭 n 行を返す（フルロードせず部分だけ）"""
    # columns=None なら全列、filters=None なら全行だが…
    # pandas 側で head(n) するのでメモリ使用は限定的
    return pd.read_parquet(pfile, engine="pyarrow").head(n)


def main() -> None:
    target = Path(TARGET_DIR).expanduser().resolve()
    if not target.is_dir():
        raise NotADirectoryError(f"指定フォルダが見つかりません: {target}")

    parquet_files = sorted(target.glob("*.parquet"))
    if not parquet_files:
        print("*.parquet ファイルが見つかりませんでした。")
        return

    print(f"=== {len(parquet_files)} 件の Parquet ファイルを解析 ===\n")
    for pfile in parquet_files:
        try:
            cols, nrows = inspect_parquet_file(pfile)
            print(f"■ {pfile.name}")
            print(f"  行数           : {nrows:,}")
            print(f"  列 ({len(cols)} 個) : {cols}\n")

            # # ここで 5 行だけ表示
            # df_head = preview_parquet_file(pfile, HEAD_ROWS)
            # # 列が多くても見切れないようオプション調整
            # with pd.option_context("display.max_columns", None,
            #                        "display.width",        200):
            #     print(f"\n--- 先頭 {HEAD_ROWS} 行 ---")
            #     print(df_head)
            # print()  # 区切り行

            if output := True:
                p = pd.read_parquet(pfile)
                # out = Path(pfile.parent.parent/"tsv"/f"{pfile.name}.tsv")
                # out.parent.mkdir(exist_ok=True, parents=True)
                # p.to_csv(out, sep="\t")
                out_ex = Path(pfile.parent.parent/"excel"/f"{pfile.name}.xlsx")
                out_ex.parent.mkdir(exist_ok=True, parents=True)
                p.to_excel(out_ex)

            

        except Exception as e:
            print(f"  [Error] プレビュー失敗: {e}\n")

if __name__ == "__main__":
    main()
