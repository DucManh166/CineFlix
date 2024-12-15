import requests
import json

def test_search_route():
    url = "http://127.0.0.1:5010/api/search"  # Replace with your actual URL
    query = "Inception"

    # Prepare the POST request
    data = {'query': query}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Send the POST request
    response = requests.post(url, data=data, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        print("Search successful!")

        # Write the JSON response to a file
        with open('search_results.json', 'w') as f:
            json.dump(response.json(), f, indent=4)

        print("Results saved to search_results.json")
    else:
        print(f"Search failed with status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_search_route()