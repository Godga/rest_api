# rest_api
<br/>
Приветствую!<br/>
Для запуска rest_api нужен Python 2.7+ или 3.6+ с установленным pip.<br/>
Список расширений, нужных для работы содержится в requirements.txt,<br/>
необходимо установить их с помощью:<br/>
<strong>pip install -r requirements.txt</strong><br/>
и запустить локальный сервер командой:<br/>
<strong>flask run</strong><br/>
API предоставляет доступ к набору сущностей Article<br/>
Сущность содержит следующие поля:<br/>
id: integer, — идентификатор статьи<br/>
author: string — автор<br/>
created: isodatetime — дата, время создания статьи, присваивается автоматически при<br/>
создании записи<br/>
updated: isodatetime — дата, время обновления статьи, присваивается автоматически при<br/>
создании и обновлении записи<br/>
content: text — содержимое статьи<br/>
В качестве транспортного протокола API используется протокол HTTP<br/>
API возвращает и принимает данные в формате JSON<br/>
Список вызовов:<br/>
<table>
  <tr>
    <td>URL</td><td>HTTP метод</td><td>Описание</td>
  </tr>
  <tr>
    <td>/api/articles</td> <td>GET</td> <td>Получить список статей</td>
  </tr>
  <tr>
    <td>/api/articles</td> <td>POST</td> <td>Добавить статью</td>
  </tr>
  <tr>
    <td>/api/articles/<id></td> <td>GET</td> <td>Получить данные статьи с идентификатором id</td>
  </tr>
  <tr>
    <td>/api/articles/<id></td> <td>PUT, PATCH</td> <td>Обновить данные статьи с идентификатором id</td>
  </tr>
    <td>/api/articles/<id></td> <td>DELETE</td> <td>Удалить статью и идентификатором id</td>
 </table>
