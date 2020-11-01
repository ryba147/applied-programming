# Hello world API using Flask
**Poetry, python 3.8.***

1. Посилання для клонування репозиторію https://github.com/ryba147/applied-programming.git <br>
Для розгортання проекту необхідно мати Flask, Gunicorn (чи інший WSGI-сервер), додати їх в залежності проекту; Poetry (чи інше віртуальне середовище) та мати підтримувану версію Python 3. <br><br>
2. При роботі з Poetry -> Віртуальне середовище запускається за допомогою *poetry shell*. <br>
3. Проект запускається WSGI-сервером Gunicorn за допомогою точки входу wsgi командою *gunicorn wsgi:application*.  
4. Перехід за адресою http://localhost:8000 спричинить **переадресацію** на http://localhost:8000/api/v1/hello-world-3. Також можна одразу переходити за адресою http://localhost:8000/api/v1/hello-world-3 (замість 3 можна вказати й інший номер варіанту). <br>
Очікуваний результат: ```Hello World! 3``` й **response 200 OK** на GET запит.
 
