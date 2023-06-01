# Written by Dylan Tuminelli using ChatGPT
# Version 1.0 - 5/31/2023
import requests
import os
import re
import html

def search_show(show_title):
    show_name = show_title.replace(" ", "-")  # Replace spaces with dashes

    # Perform a search to get the show's details
    search_url = f"https://www.episodate.com/api/search?q={show_name}"
    response = requests.get(search_url)
    data = response.json()

    # Check if any shows are found
    if "tv_shows" not in data or len(data["tv_shows"]) == 0:
        print("No shows found.")
        return None

    shows = data["tv_shows"]

    # Display the list of shows for the user to select from
    print("Multiple shows found. Please select one:")
    for i, show in enumerate(shows):
        print(f"{i+1}. {show['name']}")

    # Prompt the user to select a show
    show_number = int(input("Enter the number of the desired show: "))
    selected_show = shows[show_number - 1]
    print(f"Selected show: {selected_show['name']}")

    return selected_show

def rename_files(show_title, folder_path):
    renamed_count = 0

    # Calculate the total file count
    file_count = sum(len(files) for _, _, files in os.walk(folder_path))

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if os.path.isfile(os.path.join(root, filename)):
                season_episode = extract_season_episode(filename)
                if season_episode:
                    season, episode = season_episode
                    episode_name = get_episode_name(show_title, season, episode)
                    new_filename = f"{show_title} -S{season:02d}E{episode:02d}- {episode_name}{filename[-4:]}"
                    os.rename(
                        os.path.join(root, filename),
                        os.path.join(root, new_filename)
                    )
                    renamed_count += 1

                # Update and display the tracking indicator
                print(f"Renaming files: {renamed_count}/{file_count}", end="\r")

    print("\nDone.")

def extract_season_episode(filename):
    season_episode = None
    filename = os.path.splitext(filename)[0]
    patterns = [
        r"\.S(\d+)E(\d+)\.",
        r"-(?:S|s)(\d+)(?:E|e)(\d+)-",
        r"-(?:S|s)(\d+)-(?:E|e)(\d+)-",
        r"\.S(\d+)\.E(\d+)\.",
        r"_(?:S|s)(\d+)(?:E|e)(\d+)_",
        r"_(?:S|s)(\d+)_(?:E|e)(\d+)_",
        r"S(\d+)E(\d+)",
        r"S(\d+) - E(\d+)",
        r"\.s(\d+)e(\d+)\.",
        r"s(\d+)e(\d+)",
        r"\D(\d+)x(\d+)\D",
    ]
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            season_episode = [int(match.group(1)), int(match.group(2))]
            break
    return season_episode

def get_episode_name(show_title, season, episode):
    show_id = get_show_id(show_title)
    if show_id is None:
        return ""

    show_details_url = f"https://www.episodate.com/api/show-details?q={show_id}"
    response = requests.get(show_details_url)
    show_data = response.json()

    if "tvShow" in show_data:
        show = show_data["tvShow"]
        if "episodes" in show:
            episodes = show["episodes"]
            for ep in episodes:
                if ep["season"] == season and ep["episode"] == episode:
                    episode_name = ep["name"]
                    
                    # Remove or replace invalid characters in the episode name
                    episode_name = re.sub(r'[\\/:*?"<>|]', '', episode_name)
                    
                    # Unescape HTML entities, such as &amp;
                    episode_name = html.unescape(episode_name)
                    
                    return episode_name

    return ""

def get_show_id(show_title):
    search_url = f"https://www.episodate.com/api/search?q={show_title}"
    response = requests.get(search_url)
    data = response.json()

    if "tv_shows" in data and len(data["tv_shows"]) > 0:
        return data["tv_shows"][0]["id"]

    return None

def main():
    folder_path = input("Enter your show's folder path: ")
    show_title = input("Enter the name of the show: ")
    
    selected_show = search_show(show_title)
    if selected_show is not None:
        rename_files(show_title, folder_path)

if __name__ == "__main__":
    main()
