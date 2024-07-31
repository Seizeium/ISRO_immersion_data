import wikipediaapi
import pandas as pd

# Function to scrape Wikipedia articles
def scrape_wikipedia():
    # Specify a valid user agent with an email address
    user_agent = "isro_immersion2024/1.0 (atharvagarole678@gmail.com)"
    wiki_wiki = wikipediaapi.Wikipedia('en', headers={'User-Agent': user_agent})

    # List of ISRO-related articles, including more on datasets and missions
    articles = [
        "Indian_Space_Research_Organisation",
        "ISRO_Satellites",
        "List_of_ISRO_missions",
        "PSLV",
        "Gaganyaan",
        "Mangalyaan",
        "Chandrayaan",
        "Cartosat",
        "RISAT",
        "GSAT",
        "NavIC",
        "Earth_Observation_Satellites",
        "INSAT",
        "IRNSS",
        "Space_Data_Sharing",
        "Space_Science_Missions_of_ISRO",
        "GSAT-11",
        "GSAT-29",
        "GSAT-19",
        "GSAT-31",
        "GSAT-6A",
        "GSAT-7A",
        "GSAT-9",
        "RISAT-1A",
        "RISAT-2BR1",
        "RISAT-2B",
        "Cartosat-2F",
        "Cartosat-2E",
        "Cartosat-3"
    ]

    data = []
    for article_name in articles:
        page = wiki_wiki.page(article_name)
        if page.exists():
            title = page.title
            content = page.text
            link = page.fullurl

            # Extract links to more related articles
            links = [link for link in page.links.keys()]

            data.append({"title": title, "content": content, "link": link, "related_links": links})

    return pd.DataFrame(data)

# Scrape and save the data
df = scrape_wikipedia()
df.to_csv("wikipedia_isro_data.csv", index=False)
print(df.head())
