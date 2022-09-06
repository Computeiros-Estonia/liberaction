let time = 5000;
let currentImageIndex = 0;
let currentCircleIndex = 0;
let images = document.querySelectorAll(".banner img");
let max = images.length;
const mobileMenu = document.querySelector('.mobile-menu');
const banner = document.querySelector('.banner');
const content = document.querySelector('.content');
const control = document.querySelectorAll('.control div');
const mobileSearch = document.querySelector('.mobile-search');
const searchIcon = document.querySelector('.search-icon');
const clearIcon = document.querySelector('.clear');
const circleImages = document.querySelectorAll('.circle')

function clearText() {
    const searchText = document.querySelector('#search-text');
    searchText.value = '';
}

function toggleSearch() {
    mobileSearch.classList.toggle('active');
}

function toggleMenu() {
    const menuContainer = document.querySelector('.menu-container');
    menuContainer.classList.toggle('active');
    banner.classList.toggle('inactive');
    content.classList.toggle('active');
    mobileMenu.classList.toggle('active');
}

function nextImage() {
    images[currentImageIndex].classList.remove("selected")
    control[currentCircleIndex].classList.remove("selected")
    currentImageIndex++
    currentCircleIndex++

    if (currentImageIndex >= max) {
        currentImageIndex = 0
    }
    if (currentCircleIndex >= max) {
        currentCircleIndex = 0
    }

    // Colocar condição para não ativar mais de um círculo
    images[currentImageIndex].classList.add("selected")
    control[currentCircleIndex].classList.add("selected")
}

function start() {
    setInterval(() => {
        // troca de image
        nextImage()
    }, time)
}

window.addEventListener("load", start)
mobileMenu.addEventListener('click', toggleMenu)
searchIcon.addEventListener('click', toggleSearch)
clearIcon.addEventListener('click', clearText)


// Controle Manual - Carrossel Imagens
circleImages[0].addEventListener('click', () => {
    images[0].classList.toggle("selected")
    images[currentImageIndex].classList.toggle("selected")
    control[currentCircleIndex].classList.remove("selected")
    control[0].classList.toggle("selected")
})

circleImages[1].addEventListener('click', () => {
    images[1].classList.toggle("selected")
    images[currentImageIndex].classList.toggle("selected")
    control[currentCircleIndex].classList.remove("selected")
    control[1].classList.toggle("selected")
})

circleImages[2].addEventListener('click', () => {
    images[2].classList.toggle("selected")
    images[currentImageIndex].classList.toggle("selected")
    control[currentCircleIndex].classList.remove("selected")
    control[2].classList.toggle("selected")
})