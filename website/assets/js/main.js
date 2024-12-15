'use strict';

// Radio selection
const radioButtons = document.querySelectorAll('.filter-radios input[type="radio"]');

radioButtons.forEach(radioButton => {
  radioButton.addEventListener('click', () => {
    const checkedRadioButton = document.querySelector('.filter-radios input[type="radio"]:checked');
    const checkedValue = checkedRadioButton.id;

    // Perform actions based on the checked value
    if (checkedValue === 'featured') {
      // Do something for featured
      displayMovies(`http://127.0.0.1:5010/api/upcoming`, "movie-container");
    } else if (checkedValue === 'popular') {
      // Do something for popular
      displayMovies(`http://127.0.0.1:5010/api/top_rated`, "movie-container");

    } else if (checkedValue === 'newest') {
      // Do something for newest
      displayMovies(`http://127.0.0.1:5010/api/popular`, "movie-container");
    }
  });
});

// Data parsing 
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

// Fetch genre data
async function fetchGenreData() {
  try {
    const genreResponse = await fetch(`http://127.0.0.1:5001/api/categories`);
    if (!genreResponse.ok) {
      throw new Error(`HTTP error! status: ${genreResponse.status}`);
    }
    const genreData = await genreResponse.json();
    return new Map(genreData.categories.map(genre => [genre.api_id, genre.name]));
  } catch (error) {
    console.error("Error fetching genre data:", error);
    return new Map();
  }
}

// Display movie data with genre mapping (generic)
async function displayMovies(moviesUrl, containerId) {
  const movies = await fetchMovieData(moviesUrl);
  const genreMap = await fetchGenreData();

  const movieCardsHTML = movies.map(movie => {
    const genreNames = movie.genre_ids.map(id => genreMap.get(id) || "Unknown Genre");
    // Limit genreString to 2 entries
    const genreString = genreNames.slice(0, 2).join("/");
    const year = movie.release_date.substring(0, 4);
    return `
      <div class="movie-card">
          <div class="card-head">
            <img src="${movie.poster_path}" alt="${movie.title}" class="card-img">
            <div class="card-overlay">
              <div class="bookmark">
                <ion-icon name="bookmark-outline"></ion-icon>
              </div>
              <div class="rating">
                <ion-icon name="star-outline"></ion-icon>
                <span>7.4</span> </div> <div class="play">
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
  }).join('');

  document.getElementById(containerId).innerHTML = movieCardsHTML;
}

displayMovies(`http://127.0.0.1:5010/api/top_rated`, "movie-container");