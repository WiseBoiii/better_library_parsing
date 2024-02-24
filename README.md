 # Парсинг книг из бесплатной [онлайн-библиотеки](https://tululu.org)
**better_future_salary** - это скрипт, который позволит спарсить текст книги, её обложку, автора и отзывы к ней, а также сохранить все данные на вашей локальной машине для последующего ознакомления.

### Как установить?

С установкой все просто. Вам достаточно склонировать себе репозиторий с кодом и можно начинать работу, однако перед этим стоит убедиться, что:

+ Python 3.11 должен быть уже установлен.


### Нужные вам команды

1) Вы перейдете в папку с репозиторием
```
cd C:\Path to repository
``` 
2) С помощью этого вы установите нужные вам библиотеки
```
pip install -r requirements.txt
``` 
3) Это запустит код и покажет вам возможные аргументы для запуска:
   + `--start_page` - аргумент, отвечающий за то, с какого id книги начнется парсинг.
   + `--end_page` - аргумент, отвечающий за то, до какого id книги будет продолжаться парсинг.
     + По умолчанию значения данных аргументов установлены на 1 и 20 соответственно.
```
python main.py 
```
4) После некоторого ожидания вы получите следующий результат, который будет выглядеть примерно так:

![Вывод в консоль после работы скрипта](https://github.com/WiseBoiii/better_library_parsing/blob/main/MD%20pictures/изображение_2024-02-24_170550007.png)

![Сохраненные файлы после работы скрипта](https://github.com/WiseBoiii/better_library_parsing/blob/main/MD%20pictures/изображение_2024-02-24_170729364.png)
 
+ После отработки скрипта вы увидите две созданные у себя папки - previews(обложки) и books(сами книги с txt формате) - в которых будут сохранены соответствующие файлы.

![alt text](https://github.com/WiseBoiii/better_library_parsing/blob/main/MD%20pictures/cat-nodding.gif)
