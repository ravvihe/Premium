"""Premium custom-emoji icons for Telegram inline buttons.

Telegram only allows these button icons when the bot is eligible to use
custom emoji (for example, when its owner has Telegram Premium). Set
PREMIUM_BUTTON_ICONS=0 to keep the original Unicode emoji labels.
"""

import os

from telegram import InlineKeyboardButton as _TelegramInlineKeyboardButton


def _enabled() -> bool:
    return os.getenv("PREMIUM_BUTTON_ICONS", "1").strip().lower() not in {
        "0", "false", "no", "off",
    }


# Telegram custom emoji IDs from public emoji packs. These are icon-only
# button decorations; callback data and the bot's underlying actions are
# unchanged. Keys include both emoji presentation forms where needed.
_PREMIUM_ICON_IDS = {
    "➕": "5775937998948404844",
    "✅": "5805532930662996322",
    "🚀": "5361930420361378687",
    "🎯": "5310278924616356636",
    "📅": "5364233403300330811",
    "📊": "5231200819986047254",
    "⚡": "5219804923130038865",
    "⚙️": "5877260593903177342",
    "⚙": "5877260593903177342",
    "👤": "5879770735999717115",
    "👥": "5942877472163892475",
    "👁": "5960714428394507968",
    "👑": "5348306023889254367",
    "👨‍💻": "4985930888572306287",
    "📖": "5877597667231534929",
    "💬": "5884510167986343350",
    "📌": "5397782960512444700",
    "🔙": "5967355281057779430",
    "🔍": "5874960879434338403",
    "🗑": "5879896690210639947",
    "🏷": "5985433648810171091",
    "🔐": "5296369303661067030",
    "🔑": "5296369303661067030",
    "📱": "5411604122321302582",
    "🗳": "5884179047482659474",
    "🔗": "5877465816030515018",
    "📋": "5877597667231534929",
    "💾": "5462956611033117422",
    "🔔": "5458603043203327669",
    "🔕": "5458603043203327669",
    "📢": "5424818078833715060",
    "📩": "5253742260054409879",
    "📦": "5345987742276797245",
    "📎": "5305265301917549162",
    "💡": "5422439311196834318",
    "🔄": "5375338737028841420",
    "🔁": "5375338737028841420",
    "⏭": "5875506366050734240",
    "⏱": "5350438526691326210",
    "⏹": "5210952531676504517",
    "▶️": "5453921696354419743",
    "◀️": "5877536313623711363",
    "⬅️": "5877536313623711363",
    "✏️": "5879841310902324730",
    "✖": "5210952531676504517",
    "➖": "5877413297170419326",
    "❌": "5210952531676504517",
    "⚠️": "5447644880824181073",
    "🚫": "5260293700088511294",
    "🟢": "5429501538806548545",
    "🔴": "5210952531676504517",
    "🟠": "5447644880824181073",
    "❤️": "5429277624981538430",
    "❤": "5429277624981538430",
    "❤️‍🔥": "5429223499803672937",
    "🔥": "5424972470023104089",
    "👍": "5992199545151295755",
    "👎": "5994368422031397063",
    "⭐": "5438496463044752972",
    "🌟": "5429351167706547656",
    "💎": "5429153655045507054",
    "⏸": "5359543311897998264",
    "🕐": "5330157467781312171",
    "🌍": "5224450179368767019",
    "🌐": "5224450179368767019",
    "🏥": "5463081281048818043",
    "🐇": "5877613700344450910",
    "🐢": "5877613700344450910",
    "🚶": "5877613700344450910",
    "📣": "5424818078833715060",
    "📥": "5875008416132370818",
    "🔓": "5296369303661067030",
    "🔢": "5877485980901971030",
    "🔬": "5348158075150808878",
    "🚪": "5967355281057779430",
    "🇩🇪": "5460710948727693721",
    "🇪🇸": "5467702459700880680",
    "🇬🇧": "5467887736000093669",
    "🇷🇺": "5461155860094921420",
}

_ICON_PREFIXES = sorted(_PREMIUM_ICON_IDS, key=len, reverse=True)


def _premium_label(text: str) -> tuple[str, str | None]:
    """Return visible label and optional premium icon ID for a button."""
    label = str(text)
    icon_id = None

    # Move leading emoji out of the text and into Telegram's custom-icon
    # field. If a label starts with multiple mapped icons, use the first as
    # the premium icon and remove the remaining mapped decorations too.
    while True:
        match = next((emoji for emoji in _ICON_PREFIXES if label.startswith(emoji)), None)
        if match is None:
            break
        if icon_id is None:
            icon_id = _PREMIUM_ICON_IDS[match]
        label = label[len(match):].lstrip()

    # Reaction-picker buttons can consist of only one emoji. Keep a tiny
    # non-breaking space as the required text while the premium icon shows.
    return (label or "\u00a0"), icon_id


def premium_button(text: str, *args, **kwargs) -> _TelegramInlineKeyboardButton:
    """Build an inline button, replacing known leading emoji with premium icons."""
    if _enabled() and not kwargs.get("icon_custom_emoji_id"):
        label, icon_id = _premium_label(text)
        if icon_id:
            kwargs["icon_custom_emoji_id"] = icon_id
            text = label
    return _TelegramInlineKeyboardButton(text, *args, **kwargs)
