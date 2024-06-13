from base64 import b64encode
from io import BytesIO

from matplotlib.figure import Figure


def fig_to_base64(fig: Figure) -> str:
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
    return b64encode(buf.getvalue()).decode()
