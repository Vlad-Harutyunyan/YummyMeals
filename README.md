<p align="center">
  <h1 style="font-size:35px; text-align:center;"> YummyMeals </h1>
</p>
<p align="center">
  <img width="340" height="340" src="https://github.com/Vlad-Harutyunyan/YummyMeals/blob/master/app/index/static/media/logo1.png">
</p>
Here's our ACA second course final Flask project. 

Authors: Vlad Harutyunyan, Hayk Sahakyan, Zhora Karyan and Ruzanna Ordyan

[LICENSE file](https://github.com/Vlad-Harutyunyan/YummyMeals/blob/master/LICENSE.md)

## Project setup instruction
Stable python version for application - python 3.7 - 3.7.7


###### —-    1 step     —-

commands
for Linux,Mac
```sh
pip3 install -r requirements.txt
```

Or
for Windows
```sh
pip install -r requirements.txt
```


###### —-    2 step     —-

for Linux,Mac
```sh
python3 wsgi.py 
```
Or
for Windows
```sh 
python wsgi.py 
```


###### —-    3 step     —-

visit [127.0.0.1/home](http://127.0.0.1:5000/) in browser




## ------- Migration System -------

After changing database model , write this commands in project folder 
 
 [1] : ```sh flask db init ``` OR -  ```sh flask db stamp head ``` (if migration folder alredy exsist)

 [2] : ``` flask db migrate ```

 [3] : ``` flask db upgrade ```
