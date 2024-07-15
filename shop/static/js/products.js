// Получаем кнопку и список категорий
const catalogButton = document.getElementById('catalog-button');
const categoriesList = document.getElementById('categories-list');

// Функция, которая показывает/скрывает список категорий
function toggleCategories() {
    // categoriesList.classList.toggle('hidden');
    categoriesList.classList.toggle('show');
}

// Добавляем обработчик события на кнопку
catalogButton.addEventListener('click', toggleCategories);

// Скрываем список категорий по умолчанию
categoriesList.classList.add('hidden')  ;

