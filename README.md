# YummyMeals
[Logo](https://github.com/Vlad-Harutyunyan/YummyMeals/blob/master/app/index/static/media/logo1.png)

Here's our ACA second course final Flask project. 

Authors: Vlad Harutyunyan, Hayk Sahakyan, Zhora Karyan and Ruzanna Ordyan

[LICENSE file](https://github.com/Vlad-Harutyunyan/YummyMeals/blob/master/LICENSE.md)

## Project setup instruction
Stable python version for application - python 3.7 - 3.7.7


###### —-    1 step     —-

commands

``` pip3 install -r requirements.txt ``` (Linux,Mac)
Or
``` pip install -r requirements.txt ``` (Windows)


###### —-    2 step     —-

commands

``` python3 wsgi.py ```(Linux,Mac)
Or
``` python wsgi.py ```(Windows)


###### —-    3 step     —-

visit [127.0.0.1/home](http://127.0.0.1:5000/) in browser




## ------- Migration System -------

After changing database model , write this commands in project folder 
 
 [1] : ``` flask db init ``` OR -  ``` flask db stamp head ``` (if migration folder alredy exsist)

 [2] : ``` flask db migrate ```

 [3] : ``` flask db upgrade ```
