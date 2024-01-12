"""
file: movies.py
language: python 3
author: Aakash Jaideva
purpose: Scrapes HTML data from IMDb websites for movie ratings, year of release and votes
"""

import requests
from bs4 import BeautifulSoup


def scrape(movie_name_input):
    """
    Scrapes IMDb's top 1000 movies page for details of a specific movie.

    Parameters:
    - movie_name_input (str): The name of the movie to search for.

    Prints the details of the matching movie if found, otherwise prints a message indicating that the movie was not found.
    """
    # IMDb URL for the top 1000 movies sorted by user rating
    url = 'https://www.imdb.com/search/title/?sort=user_rating,desc&groups=top_1000'

    # Set the User-Agent header to mimic a browser request
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Send a GET request to the IMDb URL with the specified headers
    response = requests.get(url, headers=headers)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all list items with the specified class containing movie data
    movie_data = soup.findAll('li', attrs={'class': 'ipc-metadata-list-summary-item'})

    # Loop through each movie in the list
    for store in movie_data:
        # Extract the movie name from the heading
        name = store.h3.text

        # Check if the input movie name is present in the current movie's name
        if movie_name_input.lower() in name.lower():
            # Use find method with the specified class for year_of_release
            year_of_release_element = store.find('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')

            # Check if the element is found before accessing its text attribute
            if year_of_release_element:
                year_of_release = year_of_release_element.text
            else:
                year_of_release = "Year of release not available"

            # Extract the rating and votes using the 'aria-label' attribute
            the_rating = store.find('span', {'aria-label': True}).text
            i = the_rating.split()
            rating = i[0]
            votes = i[1]

            # Print the details of the matching movie
            print(f"Movie: {name}")
            print(f"Year of Release: {year_of_release}")
            print(f"Rating: {rating}")
            print(f"Votes: {votes}")

            # Return after printing the details of the first matching movie
            return

    # If the input movie name is not found in the top 1000 list
    print(f"Movie '{movie_name_input}' not found in the top 1000 list.")


if __name__ == "__main__":
    # Get user input for the movie name
    movie_name_input = input("Enter the name of the movie: ")

    # Call the scrape function with the user-input movie name
    scrape(movie_name_input)
