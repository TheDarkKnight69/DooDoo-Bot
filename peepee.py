import discord
from discord.ext import commands
import random



popular_words = open("dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("dict-sowpods.txt"))

EMOJI_CODES = {
  "green": {
    "a": "<:green_a:984464800526528512>",
    "b": "<:green_b:984464802262954075>",
    "c": "<:green_c:984464804678881340>",
    "d": "<:green_d:984464807572963368>",
    "e": "<:green_e:984464809619763250>",
    "f": "<:green_f:984464811444297830>",
    "g": "<:green_g:984464813713395753>",
    "h": "<:green_h:984464816003498034>",
    "i": "<:green_i:984464818234863676>",
    "j": "<:green_i:984464818234863676>",
    "k": "<:green_k:984464822789877800>",
    "l": "<:green_l:984464824857657354>",
    "m": "<:green_m:984464827206471720>",
    "n": "<:green_n:984464828997468213>",
    "o": "<:green_o:984464831237222423>",
    "p": "<:green_p:984464834819141692>",
    "q": "<:green_q:984464836899520513>",
    "r": "<:green_r:984464839072182442>",
    "s": "<:green_s:984464841165135922>",
    "t": "<:green_t:984464843128049674>",
    "u": "<:green_u:984464845778874448>",
    "v": "<:green_v:984464847624364063>",
    "w": "<:green_w:984464850057039894>",
    "x": "<:green_x:984464852334575678>",
    "y": "<:green_y:984464854259757131>",
    "z": "<:green_z:984464856281411608>"
  },
  
  "grey": {
    "a": "<:grey_a:984464267963142146> ",
    "b": "<:grey_b:984464270500712518>",
    "c": "<:grey_c:984464272669147146>",
    "d": "<:grey_d:984464275013775400>",
    "e": "<:grey_e:984464277073166407>",
    "f": "<:grey_f:984464279145156669>",
    "g": "<:grey_g:984464281154236456>",
    "h": "<:grey_h:984464283167518801>",
    "i": "<:grey_i:984464285306605568>",
    "j": "<:grey_j:984464287382777876>",
    "k": "<:grey_k:984464288993394759>",
    "l": "<:grey_l:984464291090538528>",
    "m": "<:grey_m:984464293527453706>",
    "n": "<:grey_n:984464295502946364>",
    "o": "<:grey_o:984464297579126784>",
    "p": "<:grey_p:984464299596591237>",
    "q": "<:grey_q:984464301601480756>",
    "r": "<:grey_r:984464303707017257>",
    "s": "<:grey_s:984464305825136650>",
    "t": "<:grey_t:984464307867770890>",
    "u": "<:grey_u:984464309646164041>",
    "v": "<:grey_v:984464312057864242>",
    "w": "<:grey_w:984464314108883074>",
    "x": "<:grey_x:984464316503838790>",
    "y": "<:grey_y:984464318164795437>",
    "z": "<:grey_z:984464320199020545>"
  },

  "yellow": {
    "a": "<:yellow_a:984465343193944075>", 
    "b": "<:yellow_b:984465347518279750>",
    "c": "<:yellow_c:984465349611237457>",
    "d": "<:yellow_d:984465352324948020>",
    "e": "<:yellow_e:984465354703118416>",
    "f": "<:yellow_f:984465357530079292>",
    "g": "<:yellow_g:984465360210251806>",
    "h": "<:yellow_h:984465363288866876>",
    "i": "<:yellow_i:984465365578960906>",
    "j": "<:yellow_j:984465367772565544>",
    "k": "<:yellow_k:984465370234646549>",
    "l": "<:yellow_l:984465372637970492>",
    "m": "<:yellow_m:984465374684790784>",
    "n": "<:yellow_n:984465376635138149>",
    "o": "<:yellow_o:984465379227222116>",
    "p": "<:yellow_p:984465381257252869>",
    "q": "<:yellow_q:984465383887097956>",
    "r": "<:yellow_r:984465386206539846>",
    "s": "<:yellow_s:984465388467286127>",
    "t": "<:yellow_t:984465390660907008>",
    "u": "<:yellow_u:984465393101963274>",
    "v": "<:yellow_v:984465395249451058>",
    "w": "<:yellow_w:984465397556314132>",
    "x": "<:yellow_x:984465399552806912>",
    "y": "<:yellow_y:984465401897422848>",
    "z": "<:yellow_z:984465403847798845>"
  },
}
def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: grey
    Args:
        word (str): The word to be colored
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["grey"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters
    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5

def random_puzzle_id():
  puzzle_id = int(random.randint(0, len(popular_words) - 1))
  return puzzle_id

  
def generate_puzzle_embed(member: discord.Member, puzzle_id: int):
    """
    Generate an embed for a new puzzle given the puzzle id and member
    Args:
        member (discord.member): The member who submitted the puzzle
        puzzle_id (int): The puzzle ID
    Returns:
        discord.Embed: The embed to be sent
    """
    embed = discord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=member.name, icon_url=member.avatar)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command .play!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: discord.Embed, guess: str) -> discord.Embed:
    """
    Updates the embed with the new guesses
    Args:
        embed (discord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the member
    Returns:
        discord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    Validates a word
    Args:
        word (str): The word to validate
    Returns:
        bool: Whether the word is valid
    """
    return word in all_words


def is_game_over(embed: discord.Embed) -> bool:
    """
    Checks if the game is over in the embed
    Args:
        embed (discord.Embed): The embed to check
    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description


