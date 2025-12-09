"""PDF 生成モジュール（fpdf2 を使用）"""

import logging
from pathlib import Path

from fpdf import FPDF

logger = logging.getLogger(__name__)

# 日本語フォントのパス（macOS システムフォント）
JAPANESE_FONT_PATHS = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]


class JapanesePDF(FPDF):
    """日本語対応の PDF クラス"""

    def __init__(self) -> None:
        super().__init__()
        self._font_loaded = False
        self._load_japanese_font()

    def _load_japanese_font(self) -> None:
        """日本語フォントをロード"""
        for font_path in JAPANESE_FONT_PATHS:
            if Path(font_path).exists():
                try:
                    self.add_font("JapaneseFont", "", font_path, uni=True)
                    self._font_loaded = True
                    logger.debug(f"フォントをロードしました: {font_path}")
                    return
                except Exception as e:
                    logger.debug(f"フォントのロードに失敗: {font_path} - {e}")
                    continue

        # フォールバック: システムのデフォルトフォントを試す
        logger.warning(
            "日本語フォントが見つかりませんでした。デフォルトフォントを使用します。"
        )

    def set_japanese_font(self, size: int = 12) -> None:
        """日本語フォントを設定"""
        if self._font_loaded:
            self.set_font("JapaneseFont", size=size)
        else:
            # フォールバック（日本語が正しく表示されない可能性あり）
            self.set_font("Helvetica", size=size)


def generate_pdf(
    text: str,
    output_path: Path,
    title: str = "文字起こし結果",
    font_size: int = 12,
) -> None:
    """
    テキストから PDF を生成する。

    Args:
        text: PDF に書き込むテキスト
        output_path: 出力 PDF ファイルのパス
        title: PDF のタイトル（ヘッダーに表示）
        font_size: フォントサイズ
    """
    pdf = JapanesePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # タイトル
    pdf.set_japanese_font(size=16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)

    # 本文
    pdf.set_japanese_font(size=font_size)

    # テキストを段落ごとに処理
    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        if paragraph.strip():
            pdf.multi_cell(0, 8, paragraph.strip())
            pdf.ln(2)
        else:
            pdf.ln(5)

    # PDF を保存
    pdf.output(str(output_path))
    logger.debug(f"PDF を保存しました: {output_path}")
