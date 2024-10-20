import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def extract_and_plot_characters(url):
    """
    Extracts tabular data from a public Google Docs URL and plots the characters 
    based on their x and y coordinates, filling unspecified positions with spaces.

    Args:
        url (str): The URL of the Google Document with tabular data.
    """
    # Step 1: Fetch the page content
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to access URL. Status code: {response.status_code}")
    
    # Step 2: Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 3: Locate and extract the table
    tables = soup.find_all('table')
    
    if len(tables) == 0:
        raise Exception("No tables found in the document.")
    
    # Extract the first table
    table = tables[0]
    rows = table.find_all('tr')

    # Step 4: Parse the table rows into a dictionary 
    data = {}
    for row in rows[1:]:  # Skip the first row because  it's a header
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]  # Get text and strip whitespace
        
        # Ensure the row has the expected number of columns (3: x-coordinate, character, y-coordinate)
        if len(cols) == 3:
            x = int(cols[0])
            y = int(cols[2])
            character = cols[1]
            data[(x, y)] = character

    # Step 5: Determine the grid size
    
    max_x = max(x for x, y in data.keys())
    max_y = max(y for x, y in data.keys())

    # Step 6: Plot characters on a blank white grid
    plt.figure(figsize=(10, 10))

    # Loop over all possible positions in the grid and fill with either the specified character or a space
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            character = data.get((x, y), '░')  # Get character if specified, otherwise use a space
            
            # Plot the character at the specified x and y coordinates
            plt.text(x, y, character)
    
    
        

    # Set limits and aspect ratio
    plt.xlim(-1, max_x + 1)
    plt.ylim(-1, max_y + 1)
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Remove axes and grid
    plt.axis('off')  # Hides the axes
    plt.show()
    
#call function
url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
extract_and_plot_characters(url)
