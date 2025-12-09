"""CLI エントリポイント"""

import argparse
import logging
import sys
from pathlib import Path

from voicememo_transcribe import __version__
from voicememo_transcribe.transcriber import transcribe_audio
from voicememo_transcribe.pdf_generator import generate_pdf

# ロガー設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(
        prog="voicememo-transcribe",
        description="Macボイスメモ（.m4a）をオフラインで文字起こしし、テキストおよびPDFを生成します。",
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="入力音声ファイル（.m4a など）",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="出力先ディレクトリ（デフォルト: 入力ファイルと同じディレクトリ）",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper モデル（デフォルト: base）",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="ja",
        help="言語コード（デフォルト: ja）",
    )
    parser.add_argument(
        "--text-only",
        action="store_true",
        help="テキストのみ出力（PDFを生成しない）",
    )
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="PDFのみ出力（テキストファイルを生成しない）",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="詳細なログを出力",
    )
    return parser.parse_args()


def main() -> int:
    """メインエントリポイント"""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    input_file: Path = args.input_file

    # 入力ファイルの存在確認
    if not input_file.exists():
        logger.error(f"入力ファイルが見つかりません: {input_file}")
        return 1

    # 出力ディレクトリの決定
    output_dir: Path = args.output_dir if args.output_dir else input_file.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 出力ファイル名（拡張子なし）
    base_name = input_file.stem
    text_output = output_dir / f"{base_name}.txt"
    pdf_output = output_dir / f"{base_name}.pdf"

    logger.info(f"入力ファイル: {input_file}")
    logger.info(f"使用モデル: {args.model}")
    logger.info(f"言語: {args.language}")

    # 文字起こし実行
    try:
        logger.info("文字起こしを開始します...")
        transcription = transcribe_audio(
            audio_path=input_file,
            model_name=args.model,
            language=args.language,
        )
        logger.info("文字起こしが完了しました。")
    except Exception as e:
        logger.error(f"文字起こし中にエラーが発生しました: {e}")
        return 1

    # テキスト出力
    if not args.pdf_only:
        try:
            text_output.write_text(transcription, encoding="utf-8")
            logger.info(f"テキストファイルを出力しました: {text_output}")
        except Exception as e:
            logger.error(f"テキストファイルの出力中にエラーが発生しました: {e}")
            return 1

    # PDF出力
    if not args.text_only:
        try:
            generate_pdf(
                text=transcription,
                output_path=pdf_output,
                title=base_name,
            )
            logger.info(f"PDFファイルを出力しました: {pdf_output}")
        except Exception as e:
            logger.error(f"PDFファイルの出力中にエラーが発生しました: {e}")
            return 1

    logger.info("処理が完了しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
