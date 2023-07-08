from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import re
import os
import sys

# Start the WebDriver
driver = webdriver.Chrome()  # Or use Chrome: webdriver.Chrome()


while True:
    # Ask the user to enter the URL to scrape from
    url = input('Enter the URL to scrape from (or type "quit" to stop): ')
    
    if url.lower() == "quit":
        break

    # Verify the URL
    if not url.startswith("https://bestcoastpairings.com/event/") or not url.endswith("?active_tab=placings"):
        print("Invalid URL. Please ensure it starts with 'https://bestcoastpairings.com/event/' and ends with '?active_tab=placings'.")
        continue

    # Get the page
    driver.get(url)

    # Wait for the JavaScript to load the content (adjust time as necessary)
    import time
    time.sleep(5)  # wait 5 seconds

    # Get the HTML of the page
    html = driver.page_source

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h3', class_='MuiTypography-root MuiTypography-h3 css-1yuegcu').get_text()

    # Clean up the title to be suitable for a filename
    clean_title = re.sub('[^a-zA-Z0-9\n]', '_', title)

    # Get the directory of the executable
    script_dir = os.path.dirname(sys.executable)

    # Create 'bestcoastoutput' directory if not exists
    os.makedirs(os.path.join(script_dir, 'bestcoastoutput'), exist_ok=True)

    # Open or create a CSV file to save the data
    with open(os.path.join(script_dir, 'bestcoastoutput', f'{clean_title}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Player Name", "Faction", "Wins", "Losses", "Points Scored"])
        full_path = os.path.join(script_dir, 'bestcoastoutput', f'{clean_title}.csv')


        # Find each player's div
        players = soup.find_all('div', class_="MuiGrid-root MuiGrid-item css-koo75d")

        for player in players:
            # Extract player's name
            name = player.find('p', class_="MuiTypography-root MuiTypography-body1 MuiTypography-gutterBottom css-1tqv6h6").get_text()
            # Extract player's faction
            faction = player.find('p', class_="MuiTypography-root MuiTypography-body2 MuiTypography-gutterBottom css-1b8y91").get_text()

            # Extract player's points
            points_html = player.find('p', class_="MuiTypography-root MuiTypography-caption MuiTypography-paragraph css-1rkqsb8")
            points_spans = points_html.find_all('span')

            win_points = []
            loss_points = []
            for span in points_spans:
                # Check if 'style' attribute exists
                if 'style' in span.attrs:
                    if 'rgb(102, 187, 106)' in span['style']:  # If green, it's a win
                        win_points.append(int(span.get_text()))
                    elif 'rgb(244, 67, 54)' in span['style']:  # If red, it's a loss
                        loss_points.append(int(span.get_text()))

            wins = len(win_points)
            losses = len(loss_points)
            points_scored = sum(win_points + loss_points)  # total points

            # The data to write
            row = [name, faction, wins, losses, points_scored]

            # Write data to the CSV and output to terminal
            writer.writerow(row)
            print(f"Wrote to file {full_path}: {row}")
            
# Don't forget to close the driver
driver.quit()
