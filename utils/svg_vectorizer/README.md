# 🖋️ SVG Vectorizer - SVGベクター変換モジュール

## 📋 概要
画像をSVGベクター形式に変換し、最適化するモジュールです。
カラー/白黒変換、階層モード、パス最適化など、多彩な変換オプションを提供します。

## 🎯 主な機能

### 基本変換機能
- カラー/白黒モード選択
- 階層モード（積み重ね/切り抜き）
- パス最適化
- サイズ自動調整

```python
from utils.svg_vectorizer import SVGVectorizer

vectorizer = SVGVectorizer()
svg = vectorizer.convert(
    image,
    color_mode='color',
    layer_mode='stacked'
)
```

## ⚙️ 変換パラメータ

### 基本パラメータ
| パラメータ | 型 | 範囲 | デフォルト | 説明 |
|------------|-----|------|------------|------|
| color_mode | str | color/binary | color | カラーモード |
| layer_mode | str | stacked/cutout | stacked | レイヤー処理方式 |
| trace_mode | str | spline/polygon/none | spline | パス生成方式 |
| noise_filter | int | 0-128 | 32 | ノイズ除去レベル |
| color_precision | int | 1-8 | 3 | 色の精度 |
| angle_threshold | float | 0-180 | 15 | 角度閾値 |

### 最適化パラメータ
| パラメータ | 型 | 範囲 | デフォルト | 説明 |
|------------|-----|------|------------|------|
| simplify_paths | bool | - | True | パス単純化 |
| merge_paths | bool | - | True | パス結合 |
| remove_background | bool | - | True | 背景除去 |
| auto_size | bool | - | True | サイズ自動調整 |

## 🔧 変換モード

### カラーモード
```python
# フルカラー変換
svg = vectorizer.convert(
    image,
    color_mode='color',
    color_precision=3
)

# 白黒変換
svg = vectorizer.convert(
    image,
    color_mode='binary',
    threshold=128
)
```

### レイヤーモード
```python
# 積み重ねモード
svg = vectorizer.convert(
    image,
    layer_mode='stacked',
    merge_overlapping=True
)

# 切り抜きモード
svg = vectorizer.convert(
    image,
    layer_mode='cutout',
    preserve_holes=True
)
```

### トレースモード
```python
# スプライントレース
svg = vectorizer.convert(
    image,
    trace_mode='spline',
    smooth_factor=0.5
)

# ポリゴントレース
svg = vectorizer.convert(
    image,
    trace_mode='polygon',
    corner_threshold=60
)
```

## 🎨 最適化オプション

### パス最適化
```python
svg = vectorizer.optimize_paths(
    svg,
    simplify=True,
    smooth=True,
    precision=2
)
```

### サイズ最適化
```python
svg = vectorizer.optimize_size(
    svg,
    max_size=1000,
    preserve_aspect=True
)
```

### ファイルサイズ最適化
```python
svg = vectorizer.optimize_filesize(
    svg,
    level='aggressive',
    preserve_quality=True
)
```

## 📊 性能指標

### 変換速度
- シンプルな画像: 〜0.5秒
- 複雑な画像: 〜2.0秒
- バッチ処理: 〜0.3秒/画像

### ファイルサイズ
| 入力サイズ | 出力サイズ（最適化前） | 出力サイズ（最適化後） |
|------------|------------------------|------------------------|
| 100KB PNG | 〜50KB SVG | 〜30KB SVG |
| 500KB PNG | 〜200KB SVG | 〜120KB SVG |
| 1MB PNG | 〜400KB SVG | 〜250KB SVG |

## 🚀 使用例

### 基本的な使用方法
```python
from utils.svg_vectorizer import SVGVectorizer

# ベクタライザーの初期化
vectorizer = SVGVectorizer()

# 画像の読み込みと変換
image = cv2.imread('input.png')
svg = vectorizer.convert(image)

# SVGの保存
with open('output.svg', 'w') as f:
    f.write(svg)
```

### バッチ処理
```python
from utils.svg_vectorizer import BatchSVGVectorizer

# バッチベクタライザーの初期化
batch_vectorizer = BatchSVGVectorizer(
    max_workers=4,
    optimize=True
)

# 画像リストの処理
results = batch_vectorizer.process_batch(image_list)
```

### カスタム最適化
```python
from utils.svg_vectorizer import SVGOptimizer

# 最適化の実行
optimizer = SVGOptimizer()
optimized_svg = optimizer.optimize(
    svg,
    remove_background=True,
    simplify_paths=True,
    merge_similar=True
)
```

## 🎯 最適化テクニック

### 変換品質
1. ノイズフィルタの適切な設定
2. パス単純化の調整
3. 色精度の最適化

### 処理速度
1. マルチスレッド処理の活用
2. キャッシュの利用
3. バッチ処理の活用

## 🧪 品質管理

### 自動テスト
```bash
python -m pytest tests/svg_vectorizer/
```

### 性能プロファイリング
```python
from utils.profiler import profile_vectorization

profile_vectorization(vectorizer, test_image)
```

## 📝 注意事項
1. 複雑な画像は処理時間が増加
2. メモリ使用量に注意
3. 最適化レベルとファイルサイズのバランス
4. SVG互換性の確認推奨
