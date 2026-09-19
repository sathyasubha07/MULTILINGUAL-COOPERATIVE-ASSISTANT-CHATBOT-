"""
Text-to-Speech engine — Piper (offline) + gTTS (online fallback).

Public API
----------
>>> from ai_engine.language import text_to_speech
>>> result = text_to_speech("नमस्ते, आपकी क्या मदद कर सकता हूँ?", "hi")
>>> result = text_to_speech("Hello!", "en", play_audio=True)
"""

import io
import logging
from pathlib import Path
from typing import Optional, Union

from .interfaces import TTSBackend, TTSResult
from .config import (
    SUPPORTED_LANGUAGES,
    DEFAULT_SAMPLE_RATE,
    is_language_supported,
    get_language_name,
    get_piper_model_path,
)
from . import audio_utils

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Piper TTS Backend  (offline, CPU-optimised ONNX)
# ---------------------------------------------------------------------------

class PiperTTSBackend(TTSBackend):
    """
    Offline Text-to-Speech via **Piper** ONNX voice models.
    """

    def __init__(self):
        self._voices = {}  # lang -> PiperVoice (lazy-loaded)

    @property
    def name(self) -> str:
        return "piper-tts"

    def is_available(self) -> bool:
        try:
            from piper import PiperVoice  # noqa: F401
            return True
        except ImportError:
            return False

    def supports_language(self, language: str) -> bool:
        """True if a Piper voice model is downloaded for *language*."""
        return get_piper_model_path(language) is not None

    def synthesize(self, text: str, language: str) -> TTSResult:
        try:
            return self._do_synthesize(text, language)
        except Exception as exc:
            logger.exception("Piper TTS failed")
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error=str(exc),
            )

    def _do_synthesize(self, text: str, language: str) -> TTSResult:
        if not text or not text.strip():
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error="Empty text — nothing to synthesize.",
            )

        text = text.strip()
        model_path = get_piper_model_path(language)
        if model_path is None:
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error=(
                    f"No Piper voice model installed for '{get_language_name(language)}'. "
                    f"Run: python -m ai_engine.language.download_models"
                ),
            )

        voice = self._load_voice(language, model_path)

        # Synthesize to an in-memory WAV
        import wave as _wave

        buf = io.BytesIO()
        with _wave.open(buf, "wb") as wf:
            voice.synthesize(text, wf)

        wav_bytes = buf.getvalue()
        sr = DEFAULT_SAMPLE_RATE

        # Determine actual sample rate from the WAV header if possible
        if wav_bytes:
            try:
                buf.seek(0)
                with _wave.open(buf, "rb") as wf:
                    sr = wf.getframerate()
            except Exception:
                pass

        return TTSResult(
            audio_bytes=wav_bytes,
            sample_rate=sr,
            language=language,
            engine=self.name,
        )

    def _load_voice(self, language: str, model_path: Path):
        """Lazy-load and cache PiperVoice instances."""
        if language in self._voices:
            return self._voices[language]

        from piper import PiperVoice

        logger.info("Loading Piper voice for '%s' from %s", language, model_path)
        voice = PiperVoice.load(str(model_path))
        self._voices[language] = voice
        return voice


# ---------------------------------------------------------------------------
# gTTS Fallback Backend  (online, Google Translate TTS)
# ---------------------------------------------------------------------------

class GttsFallbackBackend(TTSBackend):
    """
    Online TTS fallback using Google Translate's text-to-speech.
    """

    @property
    def name(self) -> str:
        return "gTTS"

    def is_available(self) -> bool:
        try:
            from gtts import gTTS  # noqa: F401
            return True
        except ImportError:
            return False

    def supports_language(self, language: str) -> bool:
        return is_language_supported(language)

    def synthesize(self, text: str, language: str) -> TTSResult:
        try:
            return self._do_synthesize(text, language)
        except Exception as exc:
            logger.exception("gTTS synthesis failed")
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error=str(exc),
            )

    def _do_synthesize(self, text: str, language: str) -> TTSResult:
        if not text or not text.strip():
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error="Empty text — nothing to synthesize.",
            )

        text = text.strip()
        if not is_language_supported(language):
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error=f"Unsupported language: '{language}'.",
            )

        from gtts import gTTS

        lang_cfg = SUPPORTED_LANGUAGES.get(language, {})
        tld = lang_cfg.get("gtts_tld", "co.in")

        tts = gTTS(text=text, lang=language, tld=tld)

        # gTTS writes MP3 → convert to WAV via pydub if possible
        mp3_buf = io.BytesIO()
        tts.write_to_fp(mp3_buf)
        mp3_bytes = mp3_buf.getvalue()

        try:
            from pydub import AudioSegment

            mp3_buf.seek(0)
            seg = AudioSegment.from_mp3(mp3_buf)
            seg = seg.set_channels(1).set_frame_rate(22050).set_sample_width(2)
            wav_buf = io.BytesIO()
            seg.export(wav_buf, format="wav")
            wav_bytes = wav_buf.getvalue()
            sr = 22050
        except Exception as exc:
            logger.warning(
                "pydub/ffmpeg failed to convert MP3 to WAV (%s) — returning raw MP3 bytes.", exc
            )
            wav_bytes = mp3_bytes
            sr = 22050

        return TTSResult(
            audio_bytes=wav_bytes,
            sample_rate=sr,
            language=language,
            engine=self.name,
        )


# ---------------------------------------------------------------------------
# Module-level singletons & convenience function
# ---------------------------------------------------------------------------

_piper: Optional[PiperTTSBackend] = None
_gtts: Optional[GttsFallbackBackend] = None


def _get_piper() -> PiperTTSBackend:
    global _piper
    if _piper is None:
        _piper = PiperTTSBackend()
    return _piper


def _get_gtts() -> GttsFallbackBackend:
    global _gtts
    if _gtts is None:
        _gtts = GttsFallbackBackend()
    return _gtts


def text_to_speech(
    text: str,
    language: str,
    backend: Optional[TTSBackend] = None,
    play_audio: bool = False,
    save_path: Optional[Union[str, Path]] = None,
) -> TTSResult:
    """
    High-level convenience function — the main entry point for teammates.

    Parameters
    ----------
    text : str
        Text to synthesize.
    language : str
        ISO-639-1 language code (e.g. ``"en"``, ``"hi"``, ``"ta"``).
    backend : TTSBackend, optional
        Force a specific backend.
    play_audio : bool
        If ``True``, play the synthesized audio through speakers.
    save_path : str | Path, optional
        If provided, save the audio to this file path.

    Returns
    -------
    TTSResult
        ``{audio_bytes, sample_rate, language, engine, file_path, error}``
    """
    if not text or not text.strip():
        return TTSResult(
            audio_bytes=b"",
            sample_rate=DEFAULT_SAMPLE_RATE,
            language=language or "unknown",
            engine="none",
            error="Empty text — nothing to synthesize.",
        )

    if not language or not is_language_supported(language):
        return TTSResult(
            audio_bytes=b"",
            sample_rate=DEFAULT_SAMPLE_RATE,
            language=language or "unknown",
            engine="none",
            error=(
                f"Unsupported language '{language}'. "
                f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
            ),
        )

    # --- choose backend (auto mode) ---
    if backend is not None:
        engine = backend
    else:
        piper = _get_piper()
        if piper.is_available() and piper.supports_language(language):
            engine = piper
        else:
            gtts = _get_gtts()
            if gtts.is_available():
                engine = gtts
                if not piper.is_available():
                    logger.info("Piper not installed — using gTTS (online) for '%s'.", language)
                else:
                    logger.info("No Piper voice for '%s' — falling back to gTTS.", language)
            else:
                return TTSResult(
                    audio_bytes=b"",
                    sample_rate=DEFAULT_SAMPLE_RATE,
                    language=language,
                    engine="none",
                    error=(
                        "No TTS backend available. Install piper-tts or gTTS: "
                        "pip install piper-tts gTTS"
                    ),
                )

    # --- synthesize ---
    result = engine.synthesize(text, language)

    # --- optional save ---
    if save_path and result.ok:
        p = audio_utils.save_audio(result.audio_bytes, save_path)
        result.file_path = p
        logger.info("Saved audio to %s", p)

    # --- optional playback ---
    if play_audio and result.ok:
        try:
            audio_utils.play_audio(result.audio_bytes, result.sample_rate)
        except Exception as exc:
            logger.warning("Playback failed: %s", exc)

    return result

