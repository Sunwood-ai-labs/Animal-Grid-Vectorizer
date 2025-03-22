# 📱 Animal Grid Vectorizer - アプリケーション

## 📋 概要
Animal Grid Vectorizerのメインアプリケーションモジュールです。Gradioを使用したWebインターフェースを提供し、画像処理の各ステップを管理します。

## 🏗️ ディレクトリ構造
```
app/
├── __init__.py      # モジュール初期化
├── app.py           # メインアプリケーション
├── handlers/        # 処理ハンドラ
└── ui/             # UIコンポーネント
```

## 💻 主要コンポーネント

### app.py
- Gradioアプリケーションのエントリーポイント
- UIコンポーネントの初期化と組み立て
- イベントハンドラの設定
- エラー処理とログ記録

### handlers/
処理ロジックを管理するハンドラモジュール群：
- 画像アップロード処理
- グリッド分割処理
- 背景除去処理
- SVG変換処理
- ファイル出力処理

### ui/
UIコンポーネントを管理するモジュール群：
- 入力フォーム
- プレビュー表示
- 進捗表示
- 結果表示

## 🔧 設定

### 環境変数
- `PORT`: アプリケーションポート（デフォルト: 7860）
- `HOST`: ホストアドレス（デフォルト: 0.0.0.0）
- `DEBUG`: デバッグモード（デフォルト: False）

### Gemini API設定
```env
XAI_API_KEY=your-api-key-here
XAI_MODEL=xai/grok-2-vision-1212
```

## 📥 入力パラメータ

### グリッド設定
- `rows`: 行数 (整数)
- `cols`: 列数 (整数)
- `padding`: 余白サイズ (ピクセル)

### 背景除去設定
- `mode`: 処理モード (simple/advanced)
- `threshold`: 閾値 (0-255)
- `iterations`: 処理反復回数

### SVG変換設定
- `color_mode`: カラーモード (color/binary)
- `layer_mode`: 階層モード (stacked/cutout)
- `trace_mode`: トレースモード (spline/polygon/none)
- `noise_filter`: ノイズフィルタ (0-128)
- `color_precision`: 色精度 (1-8)
- `angle_threshold`: 角度閾値 (0-180)

## 📤 出力形式
- 分割された画像ファイル（PNG形式）
- ベクター化されたSVGファイル
- 処理ログ
- ZIP形式でまとめられた最終出力

## 🚀 使用例

```python
import gradio as gr
from app.app import create_app

# アプリケーションの作成
app = create_app()

# 開発サーバーの起動
if __name__ == "__main__":
    app.launch(debug=True)
