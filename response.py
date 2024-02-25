def handlingMessages(message) -> str:
    userMessage = message.lower()

    if "@1150388543559045212" in userMessage:
        return "The Amadeus system is a very advanced AI programme that uses the data of a person's memories and personality as base. Now, feel free to use me for music stuff! El Psy Congroo."

    if "🖕" in userMessage:
        return "Givin' me a middle finger? Well... I'll give you one back, then!! 🖕 🖕"

    if "amadeus?" in userMessage:
        return ("Yes! That's me! Amadeus, your local AI assistant! Worth mentioning, I'm not really an AI... Yet... "
                "Although, I hope I'll turn into one, in the future!")

    if "@286161980006465536" in userMessage:
        return ""