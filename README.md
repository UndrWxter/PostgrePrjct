<H1 align="center">~~ Наш совместный проект "Дом В Миг" ~~</H1>

<img src="https://img.freepik.com/premium-photo/monkey-suit-sits-desk-front-laptop_868783-212.jpg" alt="404">

<h1 color="red" align="center">!.! Установка !.!</h1>

1)Создайте PythonProject в Pycharm.

2)Переместите содержимое папки(Dom_V_Mig-main) в папку проекта

3)Содержимое должно вглядеть примерно так![image](https://github.com/Alim-Rakhmet/Dom_V_Mig/assets/159979728/1b517cf3-2818-484e-81f8-4abd2fda563e)

4)Откройте терминал и выполните данные команды:

cd library-main

pip install -r requirements.txt

5)Выполните миграций:

python manage.py makemigrations

python manage.py migrate

6)Запустите проект и радуйтесь :) :

python manage.py runserver

<h1 color="red" align="center">///Другое///</h1>
Так же перед первым запуском советуем через консоль создать суперюзера:

python manage.py createsuperuser 

После чего следуйте инструкциям, и в конце готов ╰(*°▽°*)╯
