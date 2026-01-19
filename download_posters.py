import os
import requests

# Target directory
output_dir = r"c:\Users\calys\OneDrive\Изображения\Пленка\Рабочий стол\myproject\django-project\static\films"
os.makedirs(output_dir, exist_ok=True)

# Films to download
# (view_key_base, possible_urls)
films = [
    ("interstellar", [
        "http://www.impawards.com/2014/posters/interstellar.jpg",
        "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg"
    ]),
    ("dark-knight", [
        "http://www.impawards.com/2008/posters/dark_knight.jpg",
        "https://upload.wikimedia.org/wikipedia/en/8/8a/Dark_Knight.jpg"
    ]),
    ("inception", [
        "http://www.impawards.com/2010/posters/inception.jpg",
        "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg"
    ]),
    ("spirited-away", [
        "http://www.impawards.com/2002/posters/spirited_away.jpg", # 2002 US release
        "http://www.impawards.com/2001/posters/spirited_away.jpg",
        "https://upload.wikimedia.org/wikipedia/en/d/db/Spirited_Away_Japanese_poster.png" 
    ]),
    ("matrix", [
        "http://www.impawards.com/1999/posters/matrix.jpg",
        "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg"
    ]),
    ("parasite", [
        "http://www.impawards.com/2019/posters/parasite.jpg",
        "https://upload.wikimedia.org/wikipedia/en/5/53/Parasite_%282019_film%29_poster.jpg"
    ])
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

downloaded_files = []

for key, urls in films:
    success = False
    filename = f"{key}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    for url in urls:
        try:
            print(f"Trying to download {filename} from {url}...")
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Successfully downloaded {filename}")
                downloaded_files.append(filename)
                success = True
                break
            else:
                print(f"Failed to download from {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"Error downloading from {url}: {e}")
            
    if not success:
        print(f"Could not download poster for {key}")

print(f"Created files: {downloaded_files}")
