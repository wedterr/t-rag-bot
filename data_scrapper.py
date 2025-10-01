import bs4
from langchain_community.document_loaders import WebBaseLoader

pages = [
    "https://starwars.fandom.com/wiki/Luke_Skywalker",
    "https://starwars.fandom.com/wiki/Han_Solo",
    "https://starwars.fandom.com/wiki/Leia_Skywalker_Organa_Solo",
    "https://starwars.fandom.com/wiki/Anakin_Skywalker",
    "https://starwars.fandom.com/wiki/Chewbacca",
    "https://starwars.fandom.com/wiki/Obi-Wan_Kenobi",
    "https://starwars.fandom.com/wiki/Landonis_Balthazar_Calrissian",
    "https://starwars.fandom.com/wiki/Darth_Sidious",
    "https://starwars.fandom.com/wiki/Yoda"
    "https://starwars.fandom.com/wiki/Qui-Gon_Jinn",
    "https://starwars.fandom.com/wiki/Padm%C3%A9_Amidala",

    "https://starwars.fandom.com/wiki/Tatooine",
    "https://starwars.fandom.com/wiki/Alderaan",
    "https://starwars.fandom.com/wiki/Naboo",
    "https://starwars.fandom.com/wiki/Kashyyyk",
    "https://starwars.fandom.com/wiki/Coruscant",

    "https://starwars.fandom.com/wiki/Mid_Rim_Territories",
    "https://starwars.fandom.com/wiki/Outer_Rim_Territories",
    
    "https://starwars.fandom.com/wiki/Jedi_Order",
    "https://starwars.fandom.com/wiki/Alliance_to_Restore_the_Republic",
    "https://starwars.fandom.com/wiki/Galactic_Republic",
    "https://starwars.fandom.com/wiki/Galactic_Empire",
    "https://starwars.fandom.com/wiki/New_Republic",

    "https://starwars.fandom.com/wiki/Wookiee",
    "https://starwars.fandom.com/wiki/Jedi",
    "https://starwars.fandom.com/wiki/Sith",
    "https://starwars.fandom.com/wiki/The_Force",
    "https://starwars.fandom.com/wiki/Lightsaber",

    "https://starwars.fandom.com/wiki/DS-1_Orbital_Battle_Station",
    "https://starwars.fandom.com/wiki/Battle_of_Yavin",
]

bs4_strainer = bs4.SoupStrainer("p")
loader = WebBaseLoader(
    web_paths=(pages),
    bs_kwargs={"parse_only": bs4_strainer, },
    encoding='utf-8'
)
docs = loader.load()

for doc in docs:
    fname = doc.metadata["source"].rsplit('/', 1)[-1].replace("_", " ")
    index = doc.page_content.find("[Source]")
    with open(f"./knowledge_base/{fname}.txt", "w", encoding='utf-8') as text:
        if index != -1:
            text.write(doc.page_content[index:])
        else:
            text.write(doc.page_content)