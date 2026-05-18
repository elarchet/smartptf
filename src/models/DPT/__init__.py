# ruff: noqa: F401
import warnings

try:
    from .DptCls import DPT, OptimizedPortfolio
    from .gymEnv import DPTEnv
    from .TensorboardCallBack import TensorboardCallBack
except ImportError as e:
    warnings.warn(
        "Could not load AI components due to missing dependencies. "
        "Please install the 'ai' optional dependencies (e.g., pip install \".[ai]\"). "
        f"Original error: {e}",
        ImportWarning,
        stacklevel=2
    )

