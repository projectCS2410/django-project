import os
import urllib.request
import urllib.error

# Target directory
output_dir = r"c:\Users\calys\OneDrive\Изображения\Пленка\Рабочий стол\myproject\django-project\static\films"
os.makedirs(output_dir, exist_ok=True)

# Films to download
# (view_key_base, possible_urls)
films = [
    ("interstellar", [
        "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
        "http://www.impawards.com/2014/posters/interstellar.jpg"
    ]),
    ("dark-knight", [
        "https://upload.wikimedia.org/wikipedia/en/8/8a/Dark_Knight.jpg",
        "http://www.impawards.com/2008/posters/dark_knight.jpg"
    ]),
    ("inception", [
        "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg",
        "http://www.impawards.com/2010/posters/inception.jpg"
    ]),
    ("spirited-away", [
        "https://upload.wikimedia.org/wikipedia/en/d/db/Spirited_Away_Japanese_poster.png",
        "http://www.impawards.com/2002/posters/spirited_away.jpg",
        "http://www.impawards.com/2001/posters/spirited_away.jpg"
    ]),
    ("matrix", [
        "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
        "http://www.impawards.com/1999/posters/matrix.jpg"
    ]),
    ("parasite", [
        "https://upload.wikimedia.org/wikipedia/en/5/53/Parasite_%282019_film%29_poster.jpg",
        "http://www.impawards.com/2019/posters/parasite.jpg"
    ])
]

# Set a user user agent to avoid being blocked by Wikipedia/IMP
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')]
urllib.request.install_opener(opener)

downloaded_files = []

for key, urls in films:
    success = False
    filename = f"{key}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    for url in urls:
        try:
            print(f"Trying to download {filename} from {url}...")
            # Use urlretrieve
            urllib.request.urlretrieve(url, filepath)
            print(f"Successfully downloaded {filename}")
            downloaded_files.append(filename)
            success = True
            break
        except Exception as e:
            print(f"Failed to download from {url}: {e}")
            
    if not success:
        print(f"Could not download poster for {key}")

print(f"Created files: {downloaded_files}")
