###############################################################################
# Discord Bot auth.
#
# TOKEN=
# # To instantly authorize and call the bot to your server:
# # # https://discord.com/oauth2/authorize?client_id=1077105831046299710&scope=bot
#
###############################################################################

CHOICES_YN = ["Yes", "No"]
QUESTIONS = [
    (
        "set_goals",
        "Did you set clear goals for yourself this week?",
        CHOICES_YN,
    ),
    (
        "break_down",
        "Did you break down your goals into smaller, more manageable task?",
        CHOICES_YN,
    ),
    (
        "prioritize",
        "Did you prioritize your task based on their importance and urgency?",
        CHOICES_YN,
    ),
    (
        "avoid_distractions",
        "Did you avoid getting distracted by non-work related tasks?",
        CHOICES_YN,
    ),
    (
        "take_breaks",
        "Did you take regular breaks to recharge and prevent burnout?",
        CHOICES_YN,
    ),
    (
        "productivity_tools",
        "Did you use any productivity tools or techniques to help you stay focused and motivated?",
        CHOICES_YN,
    ),
    (
        "mindfulness",
        "Did you practice mindfulness or other relaxation techniques to reduce stress and improve your mental clarity?",
        CHOICES_YN,
    ),
    (
        "sleep_exercises",
        "Did you get enough sleep and exercises this week?",
        CHOICES_YN,
    ),
    (
        "reflect_adjust",
        "Did you take time to reflect on your progress and make adjustments as needed?",
        CHOICES_YN,
    ),
    (
        "notes",
        "Something on your mind? Is there anything else you would like to add or note about your performace this week? (Optional)",
        CHOICES_YN,
    ),
]

###############################################################################

CONVERSATION = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear.",
    "Thank you.",
    "You're welcome.",
]
