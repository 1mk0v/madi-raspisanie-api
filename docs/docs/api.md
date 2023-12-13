# About API

## Department
  <h3>GET</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Retrieves departments from the site and parses it</i></code>
  <br/><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  <pre><code>http://127.0.0.1:8000/department/</code></pre>
  <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>PARAMS</b><br/>
   &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;<code>None</code><br/><br/>
  
  <h3>POST</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Add department to DB</i></code>
  <br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/department/add</code></pre>
  <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>BODY</b><br/>
  <pre><code>{
    "id": 0,
    "value": "string"
}</code></pre>
    

  <h3>DELETE</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Delete data from DB</i></code>
  <br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/department/{id}/delete</code></pre>

## Teachers
  <h3>GET</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Retrieves teachers from the site and parses it</i></code>
  <br/><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  <pre><code>http://127.0.0.1:8000/teacher/</code></pre>
  <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>PARAMS</b><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>sem:INTEGER (>= 1 and <=2) (Calculates the current semester by default)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>year:INTEGER | YY (>=19 and <= current year) (Calculates the current year by default)</code><br/><br/>
  
  <h3>POST</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Add department to DB</i></code>
  <br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/teacher/add</code></pre>
  <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>BODY</b><br/>
  <pre><code>{
    "id": 0,
    "value": "string",
    "depatment_id":0
}</code></pre>
    

  <h3>DELETE</h3>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Delete teacher from DB</i></code>
  <br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/teacher/{id}/delete</code></pre>


## Groups
  <h3>GET</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Retrieves Groups from the site and parses it</i></code>
  <br/><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  <pre><code>http://127.0.0.1:8000/group/</code></pre>
  <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>PARAMS</b><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>sem:INTEGER (>= 1 and <=2) (Calculates the current semester by default)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>year:INTEGER | YY (>=19 and <= current year) (Calculates the current year by default)</code><br/><br/>
  
  <h3>POST</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Add group to DB</i></code><br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/group/add</code></pre>
  <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>BODY</b><br/>
  <pre><code>{
    "id": 0,
    "value": "string",
    "depatment_id":0
}</code></pre>
    

  <h3>DELETE</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Delete group from DB</i></code>
  <br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/group/{id}/delete</code></pre>


  ## Schedule
  <h3>GET</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Retrieves group schudule from the site and parses it</i></code><br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  <pre><code>http://127.0.0.1:8000/schedule/group/{id}</code></pre>
  <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>PARAMS</b><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>id:INTEGER (required)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>name:STRING</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>sem:INTEGER (>= 1 and <=2) (Calculates the current semester by default)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>year:INTEGER | YY (>=19 and <= current year) (Calculates the current year by default)</code><br/>
   <br/><br/>
  
  <h3>GET</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Retrieves teacher schedule from the site and parses it</i></code><br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  <pre><code>http://127.0.0.1:8000/schedule/group/{id}</code></pre>
  <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>PARAMS</b><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>id:INTEGER (required)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>name:STRING</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>sem:INTEGER (>= 1 and <=2) (Calculates the current semester by default)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>year:INTEGER | YY (>=19 and <= current year) (Calculates the current year by default)</code><br/>
   <br/><br/>
     
  <h3>POST</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Add schedule to DB</i></code><br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/schedule/add</code></pre>
  <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>BODY</b><br/>
  <pre><code>{
  "date": {
    "day": "string",
    "friequency": "string",
    "time": {
      "start": "15:24:51.312Z",
      "end": "15:24:51.312Z"
    }
  },
  "discipline": "string",
  "type": "string",
  "auditorium": "string",
  "group": {
    "id": 0,
    "value": "string",
    "department_id": 0
  },
  "teacher": {
    "id": 0,
    "value": "string",
    "department_id": 0
  },
  "weekday": "string"
}</code></pre>
    

  <h3>DELETE</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<i>Delete schedule from DB</i>
  <br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/schedule/{id}/delete</code></pre>


  ## Examinations
  <h3>GET</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Retrieves group exam from the site and parses it</i></code><br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  <pre><code>http://127.0.0.1:8000/exam/group/{id}</code></pre>
  <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>PARAMS</b><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>id:INTEGER (required)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>name:STRING</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>sem:INTEGER (>= 1 and <=2) (Calculates the current semester by default)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>year:INTEGER | YY (>=19 and <= current year) (Calculates the current year by default)</code><br/>
   <br/><br/>
  
  <h3>GET</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Retrieves teacher exam from the site and parses it</i></code><br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  <pre><code>http://127.0.0.1:8000/exam/teacher/{id}</code></pre>
  <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<b>PARAMS</b><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>id:INTEGER (required)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>name:STRING</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>sem:INTEGER (>= 1 and <=2) (Calculates the current semester by default)</code><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;<code>year:INTEGER | YY (>=19 and <= current year) (Calculates the current year by default)</code><br/>
   <br/><br/>
     
  <h3>POST</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>Description</b><br/>
  <code><i>Add exam to DB</i></code><br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/exam/add</code></pre>
  <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>BODY</b><br/>
  <pre><code>{
  "date": {
    "day": "string",
    "friequency": "string",
    "time": {
      "start": "15:24:51.312Z",
      "end": "15:24:51.312Z"
    }
  },
  "discipline": "string",
  "type": "string",
  "auditorium": "string",
  "group": {
    "id": 0,
    "value": "string",
    "department_id": 0
  },
  "teacher": {
    "id": 0,
    "value": "string",
    "department_id": 0
  }
}</code></pre>
    

  <h3>DELETE</h3>
  &nbsp;&nbsp;&nbsp;&nbsp;<i>Delete exam from DB</i>
  <br/><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;<b>URL</b>
  &nbsp;&nbsp;&nbsp;&nbsp;<pre><code>http://127.0.0.1:8000/exam/{id}/delete</code></pre>
