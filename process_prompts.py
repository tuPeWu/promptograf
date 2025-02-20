import os
import datetime

def generate_unique_filename(output_dir):
    """Generuje unikalną nazwę pliku na podstawie liczby plików w katalogu outputs."""
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    existing_files = [f for f in os.listdir(output_dir) if f.endswith(".txt")]
    file_count = len(existing_files) + 1
    return f"{date_str}_p-graf_{file_count:04d}.txt"

def process_prompt_file(input_file, output_dir, repo_url, commit_id):
    """Przetwarza plik promptu i zapisuje go w katalogu outputs."""
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        print(f"Plik {input_file} nie zawiera wystarczających danych.")
        return
    
    model_name = lines[0].strip()
    prompt_content = "".join(lines[1:]).strip()
    short_title = " ".join(prompt_content.split()[:5])
    date_str = datetime.datetime.now().strftime("%d.%m.%Y")
    github_record_link = f"{repo_url}/commit/{commit_id}"
    
    output_filename = generate_unique_filename(output_dir)
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Autor promptu: Paweł Wolski\n")
        f.write(f"Krótki tytuł: {short_title}\n")
        f.write(f"Użyty model AI: {model_name}\n")
        f.write(f"Data: {date_str}\n")
        f.write(f"Treść promptu:\n{prompt_content}\n")
        f.write("\nWygenerowano w: Promptograf 1.0 - Twój Pomocnik Promptograficzny!\n")
        f.write(f"{github_record_link}\n")
    
    print(f"Przetworzono: {input_file} -> {output_filename}")

def main():
    input_dir = "prompts_in"
    output_dir = "prompts_out"
    repo_url = f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}"
    commit_id = os.getenv("GITHUB_SHA", "unknown_commit")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            process_prompt_file(input_path, output_dir, repo_url, commit_id)
    
    # Commit changes to GitHub
    os.system("git config --global user.email 'github-actions@github.com'")
    os.system("git config --global user.name 'GitHub Actions'")
    os.system("git add prompts_out/*.txt")
    os.system("git commit -m 'Automatycznie dodano przetworzone pliki promptów' || echo 'Brak zmian do zatwierdzenia'")
    os.system("git push")

if __name__ == "__main__":
    main()
