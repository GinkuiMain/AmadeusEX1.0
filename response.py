def handlingMessages(message) -> str:  # Yes, I'm aware this isn't very... Well, "clean" or "good manners" but, this is just something that I'll be keeping FOR NOW.
    userMessage = message.lower()

    if "@1150388543559045212" in userMessage:
        return "The Amadeus system is a very advanced AI programme (No, I'm not) that uses the data of a person's memories and personality as base. Now, feel free to use me for music stuff! El Psy Congroo."

    if "🖕" in userMessage:
        return "Givin' me a middle finger? Well... I'll give you one back, then!! 🖕 🖕"

    if "Amadeus?" in userMessage:
        return ("Yes! That's me! Amadeus, your local AI assistant! Worth mentioning, I'm not really an AI... Yet... "
                "Although, I hope I'll turn into one, in the future!")

    if "version" in userMessage:
        return "The AmadeusEX 1.0, running on the main computer! Ask Zuzu for more information about me, if needed!"

    if "watch user" in userMessage:
        return "Watching them for 1 hour. Sending logs to DM!!"

    if "@186537028513431555" in userMessage:
        return "Zuzu is tired/eepy, please be nice to them."

    if "morgan" in userMessage:
        return "MORGAN FREEMAN! IN THE FLEEEEESH."

    if "Explode his balls" in userMessage:
        return "Explode!!!!"

    if "@286161980006465536" in userMessage:
        return ""