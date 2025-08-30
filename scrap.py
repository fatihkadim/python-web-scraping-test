import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import os
import csv
from urllib.parse import urljoin

CATEGORIES = {
    "1": ("Travel", "travel_2/index.html"),
    "2": ("Mystery", "mystery_3/index.html"),
    "3": ("Historical Fiction", "historical-fiction_4/index.html"),
    "4": ("Science Fiction", "science-fiction_16/index.html"),
    "5": ("Classics", "classics_6/index.html"),
    "6": ("Philosophy", "philosophy_7/index.html")
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_books_from_category(cat_url_path):
    base_url = "https://books.toscrape.com/catalogue/category/books/"
    main_url = f"{base_url}{cat_url_path}"
    books = []
    while True:
        try:
            response = requests.get(main_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while accessing the URL: {e}")
            return books

        soup = BeautifulSoup(response.text, 'html.parser')
        book_elements = soup.find_all(name='article', class_='product_pod')

        for book in book_elements:
            title = book.h3.a['title']
            max_length = 50
            if len(title) > max_length:
                title = title[:max_length] + "..."
            price = book.find('p', class_='price_color').text
            books.append([title, price])
        next_button = soup.select_one("li.next > a")
        if next_button:
            next_url = urljoin(main_url, next_button['href'])
            main_url = next_url
        else:
            break

    return books

def display_table(books, category_name):
    if not books:
        print(f"No books were found in the '{category_name}' category.")
        return

    table = PrettyTable()
    table.field_names = ["Book Title", "Price"]
    table.align = "l"  # Align left
    for book in books:
        table.add_row(book)

    print(f"\n--- Books in '{category_name}' ---\n")
    print(table)
    print("\n" + "-" * 50)

def save_to_csv(books, category_name):
    if not books:
        print(f"No books to save for '{category_name}'.")
        return

    # Dosya ismi kategorinin adıyla kaydediliyor
    filename = f"{category_name.replace(' ', '_').lower()}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Book Title", "Price"])  # Başlık satırı
        writer.writerows(books)  # Kitapları ekle

    print(f"\nData saved to {filename}\n")

def main_menu():
    while True:
        clear_screen()
        print("--- Book Scraping Menu ---")
        for key, (name, _) in CATEGORIES.items():
            print(f"{key}. {name}")
        print("Press 'q' or 'Q' to quit.")

        choice = input("Please enter a category number: ").strip()

        if choice.lower() == 'q':
            print("Exiting the program...")
            break

        if choice in CATEGORIES:
            category_name, url_path = CATEGORIES[choice]
            print(f"Fetching data for the '{category_name}' category...")

            books_data = get_books_from_category(url_path)
            display_table(books_data, category_name)

            save_choice = input("\nDo you want to save this data to CSV? (y/n): ").strip().lower()
            if save_choice == "y":
                save_to_csv(books_data, category_name)

            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()