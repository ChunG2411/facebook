const signup = document.querySelector('.create');
const card = document.querySelector('.signup');
const exit = document.querySelector('#exit-create');



signup.addEventListener('click', () => {
    card.style.display = 'grid';
})
exit.addEventListener('click', () => {
    card.style.display = 'none';
})



