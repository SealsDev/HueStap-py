"""RGB colors and text gradients for the terminal."""

import math
import os
import sys
from collections.abc import Mapping
from typing import Union

__version__ = "1.0.0"
__all__ = [
    "HueStep", "HueStepInstance", "rgb", "gradient", "autorgb", "configure",
    "reset", "createHueStep", "create_huestep", "phase", "step", "color",
]

_TAU = math.pi * 2
_UNSET = object()
_Number = Union[int, float]


def _number(value: _Number, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a finite number.")
    try:
        result = float(value)
    except OverflowError:
        raise TypeError(f"{name} must be a finite number.") from None
    if not math.isfinite(result):
        raise TypeError(f"{name} must be a finite number.")
    return result


def _text(text: str) -> None:
    if not isinstance(text, str):
        raise TypeError("Expected a string.")


def _wrap(value: float) -> float:
    # Keep phase normalization consistent with the Node.js version.
    return math.fmod(math.fmod(value, _TAU) + _TAU, _TAU)


def _has_color(mode: str) -> bool:
    if mode != "auto":
        return mode == "always"
    if os.environ.get("NO_COLOR"):
        return False
    if "FORCE_COLOR" in os.environ:
        return os.environ["FORCE_COLOR"] != "0"
    if os.environ.get("TERM") == "dumb":
        return False
    isatty = getattr(sys.stdout, "isatty", None)
    return bool(isatty and isatty())


def _paint(text: str, r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"


class HueStepInstance:
    """A color sequence with its own settings and phase."""

    __slots__ = ("_step", "_phase", "_color")

    def __init__(self, options=_UNSET, **kwargs):
        self._step = 0.16
        self._phase = 0.0
        self._color = "auto"
        self.configure(options, **kwargs)

    @property
    def phase(self) -> float:
        return self._phase

    @property
    def step(self) -> float:
        return self._step

    @property
    def color(self) -> str:
        return self._color

    def configure(self, options=_UNSET, **kwargs) -> "HueStepInstance":
        if options is _UNSET:
            options = {}
        if not isinstance(options, Mapping):
            raise TypeError("Expected an options object.")
        options = {**options, **kwargs}
        for key in options:
            if key not in ("step", "phase", "color"):
                raise TypeError(f"Unknown option: {key}")
        step = _number(options.get("step", self._step), "step")
        phase = _number(options.get("phase", self._phase), "phase")
        color = options.get("color", self._color)
        if color not in ("auto", "always", "never"):
            raise TypeError('color must be "auto", "always" or "never".')
        self._step = step
        self._phase = _wrap(phase)
        self._color = color
        return self

    def rgb(self, text: str, r: _Number, g: _Number, b: _Number) -> str:
        _text(text)
        for channel in (r, g, b):
            if (
                isinstance(channel, bool)
                or not isinstance(channel, (int, float))
                or not 0 <= channel <= 255
                or int(channel) != channel
            ):
                raise ValueError("RGB channels must be integers from 0 to 255.")
        if not text or not _has_color(self._color):
            return text
        return _paint(text, int(r), int(g), int(b))

    def gradient(self, text: str, phase: _Number = 0) -> str:
        _text(text)
        phase = _number(phase, "phase")
        if not text or not _has_color(self._color):
            return text
        length = sum(char not in "\n\r" for char in text)
        span = max(length - 1, 1)
        offset = _wrap(phase)
        index = 0
        result = []
        for char in text:
            if char in "\n\r":
                result.append(char)
                continue
            angle = index / span * math.pi * 1.5 + offset
            # Match Math.round rather than Python's ties-to-even rounding.
            r = math.floor(150 + 105 * math.sin(angle) + 0.5)
            g = math.floor(150 + 105 * math.sin(angle + 2.1) + 0.5)
            b = math.floor(150 + 105 * math.sin(angle + 4.2) + 0.5)
            result.append(_paint(char, r, g, b))
            index += 1
        return "".join(result)

    def autorgb(self, text: str) -> str:
        result = self.gradient(text, self._phase)
        self._phase = _wrap(self._phase + math.fmod(self._step, _TAU))
        return result

    def reset(self, phase: _Number = 0) -> "HueStepInstance":
        self._phase = _wrap(_number(phase, "phase"))
        return self

    @staticmethod
    def createHueStep(options=_UNSET, **kwargs) -> "HueStepInstance":
        return HueStepInstance(options, **kwargs)

    create_huestep = createHueStep


# Direct imports and HueStep share the same phase counter.
HueStep = HueStepInstance()
rgb = HueStep.rgb
gradient = HueStep.gradient
autorgb = HueStep.autorgb
configure = HueStep.configure
reset = HueStep.reset
createHueStep = HueStep.createHueStep
create_huestep = createHueStep


def __getattr__(name: str):
    if name in ("phase", "step", "color"):
        return getattr(HueStep, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
