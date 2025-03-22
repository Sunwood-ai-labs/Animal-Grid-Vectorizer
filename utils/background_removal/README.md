# 🧹 Background Removal - 背景除去モジュール

## 📋 概要
画像から背景を効率的に除去し、前景オブジェクトを抽出するためのモジュールです。
複数の処理モードと最適化オプションを提供します。

## 🎯 主な機能

### シンプルモード
- 閾値ベースの高速な背景除去
- メモリ効率の良い処理
- バッチ処理に最適

```python
from utils.background_removal import SimpleBackgroundRemover

remover = SimpleBackgroundRemover()
result = remover.process(
    image,
    threshold=128,
    iterations=2
)
```

### 高度モード
- GrabCutアルゴリズムによる高精度な背景除去
- 前景/背景の自動推定
- エッジ保持処理

```python
from utils.background_removal import AdvancedBackgroundRemover

remover = AdvancedBackgroundRemover()
result = remover.process(
    image,
    rect=None,  # 自動検出
    iterations=5
)
```

## ⚙️ パラメータ設定

### シンプルモード
| パラメータ | 型 | 範囲 | デフォルト | 説明 |
|------------|-----|------|------------|------|
| threshold | int | 0-255 | 128 | 2値化の閾値 |
| iterations | int | 1-10 | 2 | モーフォロジー処理の反復回数 |
| kernel_size | tuple | (3,3)-(9,9) | (3,3) | カーネルサイズ |

### 高度モード
| パラメータ | 型 | 範囲 | デフォルト | 説明 |
|------------|-----|------|------------|------|
| rect | tuple | None/座標 | None | 前景領域の指定（自動/手動） |
| iterations | int | 1-10 | 5 | GrabCut反復回数 |
| margin | int | 0-50 | 10 | 前景領域のマージン |

## 🔧 最適化オプション

### メモリ最適化
```python
remover.enable_memory_optimization(
    chunk_size=1000,
    max_workers=4
)
```

### 処理速度最適化
```python
remover.enable_gpu_acceleration()  # GPU利用可能時
remover.enable_parallel_processing()  # マルチコア処理
```

## 🎨 後処理オプション

### エッジスムージング
```python
result = remover.smooth_edges(
    result,
    radius=2,
    threshold=0.5
)
```

### ノイズ除去
```python
result = remover.remove_noise(
    result,
    min_size=100,
    connectivity=8
)
```

### アルファチャンネル最適化
```python
result = remover.optimize_alpha(
    result,
    quality=0.95
)
```

## 📊 性能指標

### シンプルモード
- 処理速度: 〜0.1秒/画像
- メモリ使用量: 〜100MB
- 精度: 80-90%（単純な背景）

### 高度モード
- 処理速度: 〜1.0秒/画像
- メモリ使用量: 〜500MB
- 精度: 90-95%（複雑な背景）

## 🚀 使用例

### 基本的な使用方法
```python
from utils.background_removal import BackgroundRemover

# リムーバーの初期化
remover = BackgroundRemover(mode='simple')

# 画像の読み込みと処理
image = cv2.imread('input.png')
result = remover.process(image)

# 結果の保存
cv2.imwrite('output.png', result)
```

### バッチ処理
```python
from utils.background_removal import BatchBackgroundRemover

# バッチリムーバーの初期化
batch_remover = BatchBackgroundRemover(
    mode='advanced',
    max_workers=4
)

# 画像リストの処理
results = batch_remover.process_batch(image_list)
```

## 🧪 品質管理

### 自動テスト
```bash
python -m pytest tests/background_removal/
```

### 性能プロファイリング
```python
from utils.profiler import profile_removal

profile_removal(remover, test_image)
```

## 📝 注意事項
1. メモリ使用量に注意（特に高度モード）
2. GPU加速は環境依存
3. 大量の画像処理時はバッチモードを推奨
