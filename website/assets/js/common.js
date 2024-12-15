'use strict';

// variables for navbar menu toggle
const header = document.querySelector('header');
const nav = document.querySelector('nav');
const navbarMenuBtn = document.querySelector('.navbar-menu-btn');

// variables for navbar search toggle
const navbarForm = document.querySelector('.navbar-form');
const navbarFormCloseBtn = document.querySelector('.navbar-form-close');
const navbarSearchBtn = document.querySelector('.navbar-search-btn');


// navbar menu toggle function
function navIsActive() {
  header.classList.toggle('active');
  nav.classList.toggle('active');
  navbarMenuBtn.classList.toggle('active');
}

navbarMenuBtn.addEventListener('click', navIsActive);

// navbar search toggle function
const searchBarIsActive = () => navbarForm.classList.toggle('active');

navbarSearchBtn.addEventListener('click', searchBarIsActive);
navbarFormCloseBtn.addEventListener('click', searchBarIsActive);

// Login toggle
const loginPopup = document.getElementById('loginPopup');
const loginButton = document.getElementById('loginButton');

loginButton.addEventListener('click', function() {
  if (loginPopup.style.display === 'none') 
  {
    loginPopup.style.display = 'block';  
  }
  else
  {
    loginPopup.style.display = 'none';
  }
});

//dropdown toggle
function toggleDropdown() {
  const dropdownContent = document.querySelector('.dropdown-content');
  dropdownContent.classList.toggle('show');
}