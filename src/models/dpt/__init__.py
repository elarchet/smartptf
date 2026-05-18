# ruff: noqa: F401
import warnings

try:
    from .dpt_cls import DPT, OptimizedPortfolio
    from .gym_env import DPTEnv
    from .tensorboard_callback import TensorboardCallBack
except ImportError as e:
    warnings.warn(
        "Could not load AI components due to missing dependencies. "
        "Please install the 'ai' optional dependencies (e.g., pip install \".[ai]\"). "
        f"Original error: {e}",
        ImportWarning,
        stacklevel=2
    )

