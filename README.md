# _“Новости друзей”_
![Labyrinth.jpg](https://github.com/GluKhovKirill/Flask/raw/master/news.png)
##### *Проект ученика Яндекс.Лицея* <br> *Глухова Кирилла*
<p>Проект представляет собой "кусок" социальной сети, а именно - новостную ленту.<br>Вы можете добавлять/удалять новости, подписываться/отписываться на новости других людей.</p>
<p>Основными элементами являются: <br>
<ul>
<li>db_editor.py:</li>
<ul>
<li>class DB (работа с самой базой данных)</li>
<li>class NewsModel (взаимодействие с таблицей новостей)</li>
<li>class UsersModel (взаимодействие с таблицей пользователей)</li>
<li>class FriendsModel (взаимодействие с таблицей "подписок на новости")</li>
</ul>
<li>forms.py:</li>
<ul>
<li>class LoginForm (форма входа)</li>
<li>class SignInForm (форма регистрации)</li>
<li>class AddNewsForm (форма добавления новости)</li>
</ul>
<li>main.py</li>
</ul></p>
<p>“Новости друзей” были написаны на языке Python с помощью фреймворка Flask, библиотек sqlite3 и werkzeug.security.</p>
<p>В дальнейшем я собираюсь:<br>
:black_square_button: Добавить возможность прикреплять файлы к постам<br>
:black_square_button: Добавить возможность одновременного использования сети несколькими людьми<br>
:black_square_button: Улучшить цветовую гамму и оформление в целом<br>
:black_square_button: Перейти на HTTPS</p>
