<div align="center">

# 🐾 Animal Grid Vectorizer

![Animal Grid Vectorizer Banner](https://github.com/user-attachments/assets/dd7dca6e-7c62-4767-b8fc-7269bf8f2bc5)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0%2B-orange)](https://www.gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Beta-yellow.svg)](https://github.com/Sunwood-ai-labs/Animal-Grid-Vectorizer)

</div>

グリッド状に配置された動物イラストを個別に分割し、SVGベクター形式に変換するAIパワードツールです。

## ✨ 主な機能

- 🔲 **グリッド分割**: 
  - 行数・列数を指定して画像を個別に分割
  - 自動的な余白の除去と最適化
  - 分割結果のプレビュー表示

- 🧹 **背景除去**: 
  - シンプルモード: 閾値ベースの高速な背景除去
  - 高度モード: GrabCutアルゴリズムを使用した高品質な背景除去
  - SVGの大きな背景要素を自動検出・削除

- 💬 **AI画像キャプション**:
  - Google Geminiを使用した高精度な画像認識
  - 自動ファイル名生成
  - カスタマイズ可能なプロンプト

- 🖋️ **SVGベクター変換**:
  - カラー/白黒モードの選択
  - 階層モード(積み重ね/切り抜き)
  - トレースモードの最適化
  - パス精度とノイズフィルタの調整

## 🚀 インストール方法

1. リポジトリのクローン:
```bash
git clone https://github.com/Sunwood-ai-labs/Animal-Grid-Vectorizer.git
cd animal_grid_vectorizer
```

2. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

3. Gemini API設定 (オプション):
- [Google AI Studio](https://aistudio.google.com/)でAPIキーを取得
- `.env`ファイルに設定を追加:
```env
XAI_API_KEY=your-api-key-here
XAI_MODEL=xai/grok-2-vision-1212
```

## 💻 使用方法

1. アプリケーションの起動:
```bash
python run.py
```

2. Webインターフェースにアクセス:
- デフォルトで`http://localhost:7860`が開きます

3. 基本的な処理手順:
   1. グリッド画像をアップロード
   2. グリッドサイズ(行数×列数)を設定
   3. 必要に応じて背景除去を設定
   4. Geminiキャプションの使用を選択（オプション）
   5. SVG変換パラメータを調整
   6. 「処理開始」をクリック
   7. 結果をダウンロード

## 📁 プロジェクト構造

```
animal_grid_vectorizer/
├── app/                    # Gradioアプリケーション
│   ├── handlers/          # 処理ハンドラ
│   └── ui/               # UIコンポーネント
├── utils/                  # ユーティリティモジュール
│   ├── background_removal/ # 背景除去機能
│   ├── grid_splitter/     # グリッド分割機能
│   ├── svg_vectorizer/    # SVG変換機能
│   └── image_captioner.py # 画像キャプション生成
├── static/                 # 静的ファイル
└── test_files/            # テストデータ
```

各モジュールの詳細については、それぞれのディレクトリのREADMEを参照してください:
- [アプリケーション (app/)](app/README.md)
- [ユーティリティ (utils/)](utils/README.md)

## ⚙️ SVG変換パラメータ

| パラメータ | 範囲 | 説明 |
|-----------|------|------|
| カラーモード | color/binary | カラーまたは白黒での出力 |
| 階層モード | stacked/cutout | パスの重なり方の制御 |
| トレースモード | spline/polygon/none | パスの生成方法 |
| ノイズフィルタ | 0-128 | 小さなノイズの除去 |
| 色精度 | 1-8 | 色の量子化レベル |
| 角度閾値 | 0-180 | 角の検出感度 |

## 🔄 処理フロー

1. 入力画像の前処理
   - 画像の読み込みと検証
   - グリッドサイズの計算

2. グリッド分割
   - 均等な分割処理
   - 余白の自動検出と除去

3. 背景除去 (オプション)
   - シンプルモード: 閾値ベース処理
   - 高度モード: GrabCutアルゴリズム

4. キャプション生成 (オプション)
   - Gemini APIによる画像分析
   - キャプションに基づくファイル名生成

5. SVGベクター変換
   - パラメータに基づく変換処理
   - 背景要素の最適化
   - サイズの自動調整

6. 結果の出力
   - プレビュー生成
   - ZIPアーカイブ作成

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 新しいブランチを作成: `git checkout -b feature/amazing-feature`
3. 変更をコミット: `git commit -m 'Add amazing feature'`
4. ブランチをプッシュ: `git push origin feature/amazing-feature`
5. プルリクエストを作成

## 📝 ライセンス

[MIT License](LICENSE)で提供されています。

## 🙏 謝辞

- [Gradio](https://www.gradio.app/) - 直感的なWebインターフェース構築
- [vtracer](https://github.com/visioncortex/vtracer) - 高品質なSVG変換
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI画像分析
