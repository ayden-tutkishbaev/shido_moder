import configs
import re
import datetime


def triggers(text):
    cleaned_text = re.sub(r'\s+', '', text.lower())
    for word in configs.BANNED_WORDS:
        if re.search(rf"{word}", cleaned_text):
            return True
    return False


def time_converter(time_text) -> datetime:
    if not time_text:
        return None

    match_ = re.match(r"(d+)[a-z]", time_text.lower().strip())

    current_time = datetime.datetime.utcnow()

    if match_:
        value, unit = int(match_.group(1)), match_.group(2)

        if unit == "m":
            time = datetime.timedelta(minutes=value)
        if unit == "h":
            time = datetime.timedelta(hours=value)
        elif unit == "d":
            time = datetime.timedelta(days=value)
        elif unit == "w":
            time = datetime.timedelta(weeks=value)
        else:
            return None

        # match unit:
        #     case "h": time = datetime.timedelta(hours=value)
        #     case "d": time = datetime.timedelta(days=value)
        #     case "w": time = datetime.timedelta(weeks=value)
        #     case _: return None

    else:
        return None

    new_datetime = current_time + time
    return new_datetime
