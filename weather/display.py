from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import WeatherData

console = Console()

_ICONS: dict[str, tuple[str, str]] = {
    "thunderstorm": (
        "    .--.\n"
        " .-(    ).\n"
        "(___.__)__)\n"
        "    ⚡ ⚡\n"
        "     ⚡  ",
        "yellow",
    ),
    "drizzle": (
        "    .--.\n"
        " .-(    ).\n"
        "(___.__)__)\n"
        "  , , , ,\n"
        " , , , , ",
        "cyan",
    ),
    "rain": (
        "    .--.\n"
        " .-(    ).\n"
        "(___.__)__)\n"
        "  ' ' ' '\n"
        " ' ' ' ' ",
        "blue",
    ),
    "snow": (
        "    .--.\n"
        " .-(    ).\n"
        "(___.__)__)\n"
        "  *  *  *\n"
        "   *  *  ",
        "white",
    ),
    "atmosphere": (
        " ≡ ≡ ≡ ≡ ≡\n"
        "   ≡ ≡ ≡\n"
        " ≡ ≡ ≡ ≡ ≡\n"
        "   ≡ ≡ ≡\n"
        " ≡ ≡ ≡ ≡ ≡",
        "bright_black",
    ),
    "clear": (
        "   \\  |  /\n"
        "    \\ | /\n"
        "  ---( )---\n"
        "    / | \\\n"
        "   /  |  \\",
        "yellow",
    ),
    "few_clouds": (
        "   \\ | /\n"
        "  --( )--\n"
        "   .(--).\n"
        ".-(      ).\n"
        "(___.__)__)",
        "yellow",
    ),
    "clouds": (
        "    .--.\n"
        " .-(    ).\n"
        "(___.__)__)\n"
        "           \n"
        "           ",
        "bright_white",
    ),
}


def _resolve_icon(condition_id: int) -> tuple[str, str]:
    if 200 <= condition_id <= 232:
        return _ICONS["thunderstorm"]
    if 300 <= condition_id <= 321:
        return _ICONS["drizzle"]
    if 500 <= condition_id <= 531:
        return _ICONS["rain"]
    if 600 <= condition_id <= 622:
        return _ICONS["snow"]
    if 700 <= condition_id <= 781:
        return _ICONS["atmosphere"]
    if condition_id == 800:
        return _ICONS["clear"]
    if condition_id == 801:
        return _ICONS["few_clouds"]
    return _ICONS["clouds"]  # 802–804


def _temp_style(temp: float) -> str:
    if temp < 0:
        return "bold blue"
    if temp < 10:
        return "cyan"
    if temp < 20:
        return "green"
    if temp < 30:
        return "yellow"
    if temp < 38:
        return "orange3"
    return "bold red"


def render(data: WeatherData) -> None:
    art, art_color = _resolve_icon(data.condition_id)
    temp_style = _temp_style(data.temperature)

    grid = Table.grid(padding=(0, 3))
    grid.add_column(width=13)
    grid.add_column()

    icon = Text(art, style=art_color)

    info = Text()
    info.append(f"{data.description.capitalize()}\n\n", style="bold white")
    info.append("Temperature  ", style="dim")
    info.append(f"{data.temperature}°C", style=f"{temp_style} bold")
    info.append(f"  (feels like {data.feels_like}°C)\n", style="dim")
    info.append("Humidity     ", style="dim")
    info.append(f"{data.humidity}%\n", style="cyan")
    info.append("Wind         ", style="dim")
    info.append(f"{data.wind_speed} m/s", style="blue")

    if data.is_stale:
        info.append("\n\ncached — live data unavailable", style="dim italic yellow")

    grid.add_row(icon, info)

    title = Text()
    title.append(f" {data.city}", style="bold white")
    title.append(f", {data.country} ", style="dim white")

    console.print(Panel(grid, title=title, border_style="steel_blue1", padding=(1, 2)))
