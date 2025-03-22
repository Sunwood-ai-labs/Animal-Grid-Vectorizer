# 🔲 Grid Splitter - グリッド分割モジュール

## 📋 概要
画像をグリッド状に分割し、個別の画像として保存するモジュールです。
自動的な余白検出と最適化機能を備えています。

## 🎯 主な機能

### 基本分割機能
- 行数×列数指定による均等分割
- 余白の自動検出と除去
- アスペクト比の保持
- バッチ処理対応

```python
from utils.grid_splitter import GridSplitter

splitter = GridSplitter()
images = splitter.split(
    image,
    rows=3,
    cols=4
)
```

### 自動余白検出
```python
from utils.grid_splitter import AutoPaddingDetector

detector = AutoPaddingDetector()
padding = detector.detect(image)
```

## ⚙️ パラメータ設定

### 基本パラメータ
| パラメータ | 型 | 範囲 | デフォルト | 説明 |
|------------|-----|------|------------|------|
| rows | int | 1以上 | 必須 | グリッドの行数 |
| cols | int | 1以上 | 必須 | グリッドの列数 |
| padding | int | 0以上 | 0 | グリッド間の余白 |
| keep_aspect | bool | - | True | アスペクト比維持 |

### 余白検出パラメータ
| パラメータ | 型 | 範囲 | デフォルト | 説明 |
|------------|-----|------|------------|------|
| threshold | float | 0-1.0 | 0.95 | 余白判定閾値 |
| min_padding | int | 0以上 | 1 | 最小余白サイズ |
| detect_edges | bool | - | True | エッジ検出使用 |

## 🔧 最適化オプション

### メモリ最適化
```python
splitter.enable_memory_optimization(
    chunk_size=1000,
    max_workers=4
)
```

### 処理速度最適化
```python
splitter.enable_parallel_processing()  # マルチコア処理
```

## 🎨 画像処理オプション

### 余白トリミング
```python
images = splitter.trim_padding(
    images,
    threshold=0.95
)
```

### サイズ正規化
```python
images = splitter.normalize_size(
    images,
    target_size=(256, 256)
)
```

### 画質最適化
```python
images = splitter.optimize_quality(
    images,
    compression=90
)
```

## 📊 性能指標

### 処理速度
- 基本分割: 〜0.1秒/グリッド
- 余白検出: 〜0.2秒/画像
- バッチ処理: 〜0.05秒/グリッド

### メモリ使用量
- 標準処理: 〜画像サイズ×2
- 最適化モード: 〜画像サイズ×1.2

## 🚀 使用例

### 基本的な使用方法
```python
from utils.grid_splitter import GridSplitter

# スプリッターの初期化
splitter = GridSplitter()

# 画像の読み込みと分割
image = cv2.imread('grid_image.png')
images = splitter.split(
    image,
    rows=3,
    cols=4
)

# 分割画像の保存
for i, img in enumerate(images):
    cv2.imwrite(f'split_{i}.png', img)
```

### 自動余白検出付き分割
```python
from utils.grid_splitter import AutoGridSplitter

# 自動スプリッターの初期化
auto_splitter = AutoGridSplitter()

# 余白を自動検出して分割
images = auto_splitter.split(
    image,
    rows=3,
    cols=4
)
```

### バッチ処理
```python
from utils.grid_splitter import BatchGridSplitter

# バッチスプリッターの初期化
batch_splitter = BatchGridSplitter(
    rows=3,
    cols=4,
    max_workers=4
)

# 画像リストの処理
results = batch_splitter.process_batch(image_list)
```

## 🎯 最適化テクニック

### メモリ効率
1. ストリーミング処理の使用
2. 必要な部分のみ読み込み
3. 処理済み画像の即時解放

### 処理速度
1. マルチスレッド処理
2. NumPy演算の活用
3. キャッシュの利用

## 🧪 品質管理

### 自動テスト
```bash
python -m pytest tests/grid_splitter/
```

### 性能プロファイリング
```python
from utils.profiler import profile_splitting

profile_splitting(splitter, test_image)
```

## 📝 注意事項
1. 大きな画像の分割時はメモリ使用量に注意
2. グリッドサイズの整合性を確認
3. 余白検出は画像の特性に依存
4. バッチ処理時は進捗監視を推奨
