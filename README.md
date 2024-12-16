<h1>Инструкция по развертке базы данных</h1>

- ***установить модули requirements.txt***
  ```bash
  pip install requirements.txt
  ```
- ***запустить файл data.py***
  ```bash
  python data.py
  ```
  или через IDE


все функции, связанные с бд находятся также в этом файле


список функций:
- вывод столбцов
  ```python
  output()
  ```
- вывод записей
  ```python
  outputDeliveries()
  ```
- удаление таблицы
  ```python
  delete()
  ```
- создание таблицы
  ```python
  create()
  ```

<h2>Настройка url запросов к API</h2>


все url запросы к api находятся в файле main.py
