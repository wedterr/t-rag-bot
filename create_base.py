import json
import os
import re
from pathlib import Path
from inflect import engine

p = engine()

def replace_words_in_file(file_path, substitutions):
    text = Path(file_path).read_text(encoding='utf-8')

    def replace_match(match):
        word = match.group(0)
        lower_word = word.lower()

        for key, replacement in substitutions.items():
            key_singular = key.lower()
            key_plural = p.plural(key_singular)

            # Проверяем совпадение с ключом в единственном или множественном числе
            if lower_word == key_singular:
                new_word = replacement
            elif lower_word == key_plural:
                new_word = p.plural(replacement)
            else:
                continue

            # Восстановим регистр исходного слова
            if word.isupper():
                new_word = new_word.upper()
            elif word[0].isupper():
                new_word = new_word.capitalize()
            else:
                new_word = new_word.lower()

            return new_word
        return word

    # Формируем паттерн для поиска всех ключей и их форм
    words_pattern = "|".join(re.escape(k) for k in substitutions.keys())
    # Регулярное выражение для слов в тексте (с учётом слов в единственном или множественном числе)
    pattern = re.compile(r'\b(' + words_pattern + r')s?\b', re.IGNORECASE)

    result_text = pattern.sub(replace_match, text)

    # Запишем изменения обратно в файл (или можно вернуть строку)
    Path(file_path).write_text(result_text, encoding='utf-8')
    os.rename(file_path, pattern.sub(replace_match, file_path))

def process_directory(root_dir, terms_map):
    
    for dirpath, _, filenames in os.walk(root_dir):
        # Обрабатываем содержимое файлов
        for filename in filenames:
            if not filename.lower().endswith('.txt'):
                continue
                
            filepath = os.path.join(dirpath, filename)
            replace_words_in_file(filepath, terms_map)
    return

def main():
    root_dir = "knowledge_base"
    terms_path = "terms_map.json"
    
    with open(terms_path, 'r', encoding='utf-8') as f:
        substitutions = json.load(f)  
          
    process_directory(root_dir, substitutions)
    
    print("Done!")

if __name__ == "__main__":
    main()