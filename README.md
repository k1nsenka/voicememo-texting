# voicememo-transcribe

Mac ボイスメモ（.m4a）をオフラインで文字起こしし、テキストおよび PDF を生成する CLI ツールです。

## 特徴

- **オフライン動作**: OpenAI Whisper をローカルで実行（インターネット接続不要）
- **日本語対応**: 日本語の文字起こしに最適化
- **複数出力形式**: テキスト (.txt) と PDF (.pdf) を同時生成
- **柔軟なモデル選択**: 精度と速度のバランスを選択可能

## 前提条件

- macOS
- Python 3.10 以上
- [ffmpeg](https://ffmpeg.org/) がインストールされていること

```bash
# Homebrew で ffmpeg をインストール
brew install ffmpeg
```

## インストール

```bash
# uv を使用（推奨）
uv pip install -e .

# または pip を使用
pip install -e .
```

## 使い方

### 基本的な使い方

```bash
uv run voicememo-transcribe /path/to/voice-memo.m4a
```

これにより、同じディレクトリに以下のファイルが生成されます：
- `voice-memo.txt` - 文字起こしテキスト
- `voice-memo.pdf` - PDF 形式の文字起こし

### オプション

```bash
# 出力先ディレクトリを指定
voicememo-transcribe input.m4a -o /path/to/output/

# より高精度なモデルを使用（処理時間が長くなります）
voicememo-transcribe input.m4a -m medium

# テキストファイルのみ出力
voicememo-transcribe input.m4a --text-only

# PDF のみ出力
voicememo-transcribe input.m4a --pdf-only

# 英語の音声を文字起こし
voicememo-transcribe input.m4a -l en

# 詳細なログを表示
voicememo-transcribe input.m4a --verbose
```

### Whisper モデル

| モデル | 精度 | 速度 | VRAM 使用量 |
|--------|------|------|-------------|
| tiny   | 低   | 最速 | ~1GB        |
| base   | 中   | 速い | ~1GB        |
| small  | 高   | 普通 | ~2GB        |
| medium | 高   | 遅い | ~5GB        |
| large  | 最高 | 最遅 | ~10GB       |

※ 初回実行時にモデルがダウンロードされます（`~/.cache/whisper` に保存）

## Mac ボイスメモの保存場所

Mac のボイスメモは以下の場所に保存されています：

```
~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/
```

## 開発

```bash
# 依存関係のインストール
uv pip install -e .

# テスト実行
uv run pytest
```

## ライセンス

MIT License
