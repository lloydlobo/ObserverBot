import io

import discord
import matplotlib.pyplot as plt
from discord.ext import commands

from CREDENTIALS import *
from DATA import *
from db import DBHelper
from plot import *

###############################################################################

db = DBHelper()
db.setup()

###############################################################################

description = """
Hello! I am observerbot, your no-nonsense executive function trainer bot.

Trained for Discord, I am here to keep you in line with your executive functions and
respond to your commands and generate text based on your inputs.
Feel free to use the '?help' command to see the list of available commands and
how to use them.

Here are some of the things I can do:
"""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/",
                   description=description, intents=intents)

###############################################################################


@bot.event
async def on_ready():
    """Log the terminal when the bot is ready and connected to Discord."""
    print(f"Logged in as {bot.user}.")


@bot.command()
async def reflect(ctx):
    """Review and generate progress report of executive function"""
    answers = []
    for question in QUESTIONS:
        # Send question.
        question_text = question[1]
        await ctx.send(question_text)

        while True:
            # Await answer.
            answer = await bot.wait_for(
                "message", check=lambda message: message.author == ctx.author
            )

            # Handle the recorded answers.
            if (answer.content).lower() in ["yes", "y", "no", "n"]:
                answers.append(answer)
                break  # If valid response, exit the innermost `while` loop.
            elif (answer.content).lower() in ["quit", "q"]:
                await ctx.send(f"Quitting... Goodbye!")
                return
            else:
                await ctx.send(
                    f"```Invalid response.\nAvailable responses are [yes, y, no, n, quit, q].```"
                    f"{question_text}"
                )
        pass

    # Calculate score
    num_answers = len(QUESTIONS)
    num_yes = sum(
        1 for answer in answers if answer.content.lower() in ["yes", "y"])
    percentage = (num_yes / num_answers) * 100

    await ctx.send(f"Your progress score for this week is {percentage:.2f}%.")
    db.add_reflect(
        user_id=ctx.author.id,
        score=percentage,
    )
    await ctx.send("Data saved!")


@bot.command()
async def observe(ctx):
    """Observe and save current task and focus level"""
    await ctx.send("What task are you currently working on?")
    task = await bot.wait_for(
        "message", check=lambda message: message.author == ctx.author
    )

    await ctx.send(
        "On a scale of 1-10, how focused and concentrated are you on this task?"
    )
    focus = await bot.wait_for(
        "message", check=lambda message: message.author == ctx.author
    )
    db.add_observe(
        user_id=ctx.author.id,
        task=task.content,
        focus=focus.content,
    )
    await ctx.send("Data saved!")


###############################################################################


@bot.command(name="view-all")
async def view_all(ctx):
    """Display all observation and reflection data"""
    user_id = ctx.author.id
    get_observe = db.get_observe(user_id=user_id)
    get_reflect = db.get_reflect(user_id=user_id)
    await ctx.send(f"""@observe```{get_observe}```@reflect```{get_reflect}```""")


# When using matplotlib with Discord, the generated charts are usually displayed in a separate window on the machine running the bot, rather than directly in the Discord chat. This is because matplotlib is designed for generating static charts, rather than interactive charts that can be directly interacted with by users.
# However, you can still use matplotlib to generate charts in your bot and then send the resulting image file to the user in Discord. You can use the discord.py library's File class to create a file object from the generated image, and then send the file object using the await ctx.send() function.
# The file is then sent to the user in Discord using await ctx.send() and the discord.py File class.
# Although the chart is not directly interactive in Discord, the user can still view the chart and interact with it in their own way by zooming in, panning, or taking a screenshot. However, if you need to provide more advanced interactive features, you may need to look into other charting libraries that are designed specifically for interactive charts, such as Plotly or Bokeh.
#
# Date::Performance
@bot.command()
async def chart(ctx):
    """
    Generate and fetch `/reflect` chart using matplotlib and then converts it to a PNG image file.
    """
    # Retrieve the user's performance data from the database.
    c = db.create_connection()
    data = c.execute(
        """SELECT * FROM db_reflect WHERE user_id=?""", (ctx.author.id,)
    ).fetchall()
    if len(data) == 0:
        await ctx.send("No performance data found")
        return

    # Plot the performance data using matplotlib.
    x = [row[2] for row in data]  # date.
    y = [row[1] for row in data]  # score %.
    plt.plot(x, y)
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.title("Your weekly reflection score chart")

    # Convert the chart to an image file.
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    await ctx.send("Here's your weekly reflection score chart")
    # Send the chart image to the user in Discord
    await ctx.send(file=discord.File(buf, "reflectchart.png"))
    # plt.show()  # Display all open figures.
    pass


###############################################################################


def main():
    pass


if __name__ == "__main__":
    main()

bot.run(TOKEN)

###############################################################################
###############################################################################

# Create a database to store user data
# def connect_db():
#     c = conn.cursor()
#     c.execute(
#         """
#         CREATE TABLE IF NOT EXISTS db_observe (
#             user_id INTEGER,
#             task TEXT,
#             focus INTEGER,
#             date TEXT
#         )
#         """
#     )
#     c.execute(
#         """
#         CREATE TABLE IF NOT EXISTS db_reflect (
#             user_id INTEGER,
#             score REAL,
#             date TEXT
#         )
#         """
#     )
#     conn.commit()
#     return c

# db.setup()
# last_update_id = None
# while True: updates = get_updates(last_update_id)
#     if len(updates["result"]) > 0:
#         last_update_id = get_last_update_id(updates) + 1
#         handle_updates(updates)
#     time.sleep(0.5)
# send_message( "Welcome to the Executive Function Bot. I'm here to help you get things done. For now, I operate as a traditional To Do list. Tell me things that you want to do and use /done to mark them complete", chat,)

# def train_chatbot():
#     trainer = ListTrainer(chatbot)
#     trainer.train(CONVERSATION)
#     pass
# def get_response_chatbot():
#     response = chatbot.get_response("Good morning!")
#     print(response)
#     pass
###############################################################################
# def get_url(url):
#     response = requests.get(url)
#     content = response.content.decode("utf8")
#     return content
# def send_message(text, chat_id, reply_markup=None):
#     # text = urllib.quote_plus(text)
#     # url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format( text, chat_id)
#     # if reply_markup: url += "&reply_markup={}".format(reply_markup)
#     # get_url(url)
#     pass
