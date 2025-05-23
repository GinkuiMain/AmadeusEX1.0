def handlingMessages(message) -> str:  # Yes, I'm aware this isn't very... Well, "clean" or "good manners" but, this is just something that I'll be keeping FOR NOW.
    userMessage = message.lower()

    if "🖕" in userMessage:
        return "Givin' me a middle finger? Well... I'll give you one back, then!! 🖕 🖕"

    if "watch user" in userMessage:
        return "Watching them for 1 hour. Sending logs to DM!!"

    if "watch server" in userMessage:
        return "Watching the server - Default time: 6 hours || Go sleepy zuzu!! ♥ "

    if "morgan" in userMessage:
        return "GORDON FREEMAN! IN THE FLEEEEESH."

    if "Explode his balls" in userMessage:
        return "Explode!!!!"

    if "@286161980006465536" in userMessage:
        return ""