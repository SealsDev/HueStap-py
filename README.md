# HueStep

RGB colors and smooth text gradients for Python terminals. No runtime dependencies.
Requires Python 3.9+ and a terminal with true-color ANSI support.

## Install

```sh
pip install huestep
```

To install from source, run `python -m pip install .` in the project directory.

## Usage

```python
from huestep import HueStep

print(HueStep.rgb("Purple", 170, 85, 255))
print(HueStep.gradient("A smooth color gradient"))
print(HueStep.autorgb("Connecting..."))
print(HueStep.autorgb("Ready."))
```

`autorgb()` shifts the gradient on each call. It does not animate existing output.
All color methods return strings.

## Configuration

```python
HueStep.configure(step=0.16, phase=0, color="auto")
logger = HueStep.createHueStep(step=0.5)
print(logger.autorgb("Independent color sequence"))
```

- `step`: phase increment in radians; negative values reverse the direction.
- `phase`: starting phase, wrapped at `2π`. Use `reset()` to return to zero.
- `color`: `"auto"`, `"always"`, or `"never"`.

Automatic detection respects `NO_COLOR`, then `FORCE_COLOR`, then TTY status and
`TERM=dumb`. Instance settings are read-only; use `configure()` to update them.
`configure()` also accepts a dictionary. `create_huestep()` is an alias for
`createHueStep()`.

## License

[MIT](LICENSE)
