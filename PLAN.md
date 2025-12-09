# PLAN.md - voicememo-texting

## 2025-12-09 Mac ボイスメモ文字起こし CLI（ブランチ: feature/voicememo-transcribe-cli）

### 目的

- ユーザ指示: "Mac ボイスメモ（.m4a）をオフラインで文字起こしし、テキストおよび PDF を生成する CLI ツールを作ってください。"
- これを「.m4a ファイルをローカルの音声認識モデルで文字起こしし、テキスト・PDF を出力する CLI」として具現化する。

### 前提・制約

- Python + uv を利用（標準運用ルールに準拠）
- オフライン動作: OpenAI Whisper（ローカル推論）を使用
- PDF 生成: `reportlab` または `fpdf2` を利用（日本語対応のため）
- macOS 環境を想定（ボイスメモが .m4a 形式で保存されるため）

### 技術選定

| 機能               | ライブラリ                       | 理由                                  |
| ------------------ | -------------------------------- | ------------------------------------- |
| 音声文字起こし     | `openai-whisper` (ローカル実行)  | オフライン・高精度・日本語対応        |
| 音声読み込み       | `ffmpeg` (外部依存)              | Whisper が内部で利用                  |
| PDF 生成           | `fpdf2`                          | 軽量・日本語対応が比較的容易          |
| CLI フレームワーク | `argparse` (標準ライブラリ)      | 依存を増やさない                      |

### TODO

- [x] PLAN.md のタスク分解を書く
- [ ] ブランチ `feature/voicememo-transcribe-cli` を作成
- [ ] `.gitignore` を整備
- [ ] `uv init` でプロジェクト初期化
- [ ] 必要な依存を `uv add` で追加
- [ ] CLI エントリポイント (`cli.py`) を作成
- [ ] Whisper を用いた文字起こし機能を実装
- [ ] PDF 生成機能を実装
- [ ] 簡易テスト or 手動確認
- [ ] README.md を作成
- [ ] PR を作成

### 出力仕様

```
$ voicememo-transcribe input.m4a
→ input.txt  (文字起こしテキスト)
→ input.pdf  (PDF 形式)
```

オプション:
- `--output-dir` : 出力先ディレクトリ指定
- `--model` : Whisper モデル選択 (tiny/base/small/medium/large)
- `--language` : 言語指定 (デフォルト: ja)
