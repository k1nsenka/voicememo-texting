"""音声文字起こしモジュール（Whisper を使用）"""

import logging
from pathlib import Path

import whisper

logger = logging.getLogger(__name__)


def transcribe_audio(
    audio_path: Path,
    model_name: str = "base",
    language: str = "ja",
) -> str:
    """
    音声ファイルを文字起こしする。

    Args:
        audio_path: 入力音声ファイルのパス
        model_name: Whisper モデル名 (tiny/base/small/medium/large)
        language: 言語コード（例: "ja", "en"）

    Returns:
        文字起こしされたテキスト
    """
    logger.debug(f"モデル '{model_name}' をロード中...")
    model = whisper.load_model(model_name)
    logger.debug("モデルのロードが完了しました。")

    logger.debug(f"音声ファイル '{audio_path}' を処理中...")
    result = model.transcribe(
        str(audio_path),
        language=language,
        verbose=False,
    )

    text: str = result["text"]
    logger.debug(f"文字起こし結果: {len(text)} 文字")

    return text.strip()
