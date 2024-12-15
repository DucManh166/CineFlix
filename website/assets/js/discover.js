// Query panel
const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const optionsList = document.querySelectorAll(".option");
const dropdownList = document.getElementById('dropdownListMovies');
const recommendButton = document.querySelector('.recommend-button')

selected.onfocus = () => {
  optionsContainer.classList.add("active");
};

selected.onblur = () => {
  selected.style.backgroundColor = "initial";
  optionsContainer.classList.remove("active");
};

selected.addEventListener('keyup', () => {
  const filterValue = selected.value.toLowerCase();
  const options = dropdownList.querySelectorAll('.option');

  options.forEach(option => {
    const optionText = option.textContent.toLowerCase();
    if (optionText.includes(filterValue)) {
      option.style.display = 'block';
    } else {
      option.style.display = 'none'; 1 
    }
  });

  // Show or hide the dropdown list based on input value
  if (filterValue.trim() === '') {
    dropdownList.classList.remove('active');
  } else {
    dropdownList.classList.add('active');
  }
});

recommendButton.addEventListener('click', async () => {
    const searchTerm = document.getElementById('searchInput').value;
    if (searchTerm.trim() === "") {
        alert("Please enter a search term.");
        return;
    }
    await fetchRecommendData(`${encodeURIComponent(searchTerm)}/tags`, "movie-container-tags")
    await fetchRecommendData(`${encodeURIComponent(searchTerm)}/genres`, "movie-container-genres")
    await fetchRecommendData(`${encodeURIComponent(searchTerm)}/keywords`, "movie-container-keywords")
    await fetchRecommendData(`${encodeURIComponent(searchTerm)}/cast`, "movie-container-casts")
    await fetchRecommendData(`${encodeURIComponent(searchTerm)}/production_companies`, "movie-container-production-company")
    
});

async function fetchRecommendData(url, containerId) {
    try {
        const response = await fetch(`http://127.0.0.1:5011/api/movie/recommend/${(url)}`); 

        if (!response.ok) {
            const errorData = await response.json(); // Attempt to parse error details
            const errorMessage = errorData.message || `HTTP error! status: ${response.status}`;
            throw new Error(errorMessage);
        }

        const recommendations = await response.json();
        displayMovies(recommendations, containerId); 

    } catch (error) {
        console.error("Error fetching recommendations:", error);
        alert(`Error fetching recommendations: ${error.message}`); 
    }
}
// Data retrieve from API
async function fetchMovieData(url) {
    try {
      const movieResponse = await fetch(url);
      if (!movieResponse.ok) {
        throw new Error(`HTTP error! status: ${movieResponse.status}`);
      }
      const movieData = await movieResponse.json();
      return movieData;
    } catch (error) {
      console.error("Error fetching movie data:", error);
      return [];
    }
}

async function addToList() {
    try {
      const movieData = await fetchMovieData("http://127.0.0.1:5011/api/movie/list");
  
      const movieList = document.getElementById("dropdownListMovies");
  
      movieData.forEach(movie => {
        const listItem = document.createElement("li");
        listItem.classList.add("option");
        listItem.textContent = movie; 
        movieList.appendChild(listItem);
      });
    } catch (error) {
      console.error("Error adding movies to list:", error);
    }
}
addToList();

async function displayMovies(movies, containerId) {
    const movieContainer = document.getElementById(containerId); // Assumes you have a div with this ID

    if (!movieContainer) {
        console.error("Error: Element not found:", containerId);
        return;
    }

    movieContainer.innerHTML = ''; // Clear previous content

    movies.forEach(movie => {
        const genreString = movie.genres.slice(0, 2).join('/');
        const year = new Date(movie.release_date).getFullYear();

        const movieCardHTML = `
            <div class="movie-card">
                <div class="card-head">
                    <img src="${movie.poster_path}" alt="${movie.title}" class="card-img">
                    <div class="card-overlay">
                        <div class="bookmark">
                            <ion-icon name="bookmark-outline"></ion-icon>
                        </div>
                        <div class="rating">
                            <ion-icon name="star-outline"></ion-icon>
                            <span>7.4</span> </div>
                        <div class="play">
                            <ion-icon name="play-circle-outline"></ion-icon>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <h3 class="card-title">${movie.title}</h3>
                    <div class="card-info">
                        <span class="genre">${genreString}</span>
                        <span class="year">${year}</span>
                    </div>
                </div>
            </div>
        `;
        movieContainer.innerHTML += movieCardHTML;
    });
}

//For now, use the mock data.

document.addEventListener('DOMContentLoaded', () => {
    dropdownList.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
          selected.value = event.target.textContent;
        }
      });      
});