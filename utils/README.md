# 🛠️ Animal Grid Vectorizer - ユーティリティ

## 📋 概要
Animal Grid Vectorizerの主要な処理機能を提供するユーティリティモジュール群です。
画像処理、ベクター変換、AI機能などの中核となる機能を実装しています。

## 🏗️ ディレクトリ構造
```
utils/
├── background_removal/  # 背景除去機能
├── grid_splitter/      # グリッド分割機能
├── svg_vectorizer/     # SVG変換機能
└── image_captioner.py  # 画像キャプション生成
```

## 💻 モジュール説明

### 🧹 background_removal/
画像から背景を除去する機能を提供します。
- [詳細説明](background_removal/README.md)

主な機能：
- シンプルモード（閾値ベース）
- 高度モード（GrabCutアルゴリズム）
- 透明部分の最適化
- バッチ処理対応

### 🔲 grid_splitter/
グリッド画像を個別の画像に分割する機能を提供します。
- [詳細説明](grid_splitter/README.md)

主な機能：
- グリッドサイズ指定による分割
- 余白の自動検出と除去
- アスペクト比の保持
- バッチ処理対応

### 🖋️ svg_vectorizer/
画像をSVGベクター形式に変換する機能を提供します。
- [詳細説明](svg_vectorizer/README.md)

主な機能：
- カラー/白黒変換
- 階層モード選択
- パス最適化
- サイズ自動調整

### 💬 image_captioner.py
Google Geminiを使用した画像キャプション生成機能を提供します。

主な機能：
- 画像の内容分析
- キャプション生成
- ファイル名生成
- カスタムプロンプト対応

## 🔧 共通ユーティリティ

### エラー処理
```python
from utils.exceptions import (
    GridSplitError,
    BackgroundRemovalError,
    VectorizeError,
    CaptionError
)
```

### ログ機能
```python
from utils.logging import get_logger

logger = get_logger(__name__)
logger.info("処理開始")
```

### 設定管理
```python
from utils.config import (
    load_config,
    save_config,
    update_config
)
```

## 📊 性能最適化

### メモリ使用量
- 大きな画像の分割処理時のメモリ管理
- バッチ処理時のメモリプール
- 一時ファイルの自動クリーンアップ

### 処理速度
- マルチスレッド処理対応
- GPU支援処理（利用可能な場合）
- キャッシュ機能

## 🔍 デバッグ機能

### デバッグモード
```python
from utils.debug import enable_debug

enable_debug()  # デバッグ情報の出力を有効化
```

### プロファイリング
```python
from utils.profiler import profile

@profile
def process_image():
    # 処理内容
    pass
```

## 🧪 テスト

### ユニットテスト
```bash
python -m pytest tests/utils/
```

### 統合テスト
```bash
python -m pytest tests/integration/
```

## 📝 コード規約
- PEP 8に準拠
- Type hintingの使用
- Docstringの記述（Google形式）
- モジュールごとのREADME.mdの整備
