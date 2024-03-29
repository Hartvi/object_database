# How to launch
Assuming that you are on Linux and have python 3.6-3.10:

```
git clone git@github.com:Hartvi/object_database.git
cd object_database
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd main
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then go to [http://127.0.0.1:8000](http://127.0.0.1:8000) (note: some files may be missing)

NOTE: `python manage.py runserver` is by default only for http, for SSL or PostgreSQL support see [Deployment](#Deployment) 2. & 3. tutorials

## Deployment
1. [official deployment website](https://docs.djangoproject.com/en/4.0/howto/deployment/)
2. [Deploy with Apache2](https://dev.to/ninahwang/deploying-a-django-application-using-apache2-94g)
3. [Deploy with Apache & PostgreSQL](https://dev.to/ajithklepsydra/how-to-set-up-and-deploy-a-django-application-on-a-linux-server-2dff)

### TODO
- TODO: data visualization
- cache measurements connected to object instances so the browser loads quickly
  - doing it for images now
- better tutorial how to upload things - maybe video?
- done: link to REST object instance from the visual browser
- done: add how to run post_measurement() in the tutorial
- add measurement method field, e.g. grasp, poke, to the serializer and view create method
- add drag & drop + its tutorial
- benchmark
- upload OSF things - formatting is done
  - a new need has arisen
  - TODO: always use files to save sensor outputs. even raw JSON can be 15 MB which is extremely slow to load even from my own disc, let alone over the internet as a gazillion lines of text
  - add PNGs to the black foam and white foam measurements when uploading to the database
- Done: object browser - USER FRIENDLY STUFF
  - Done: object : pictures, how measurements
  - Done: search for objects
    - Done: how many objects measured, properties - find out how to do frontend image embedding

#### done
- links to examples, documentation, repositories

Advanced things:
- Differentiate between physical objects
  - compare images from the png; this could serve as something akin to the instance id

### 10/14
- added quantities to measurements/entries/sensor outputs
- todo: frontend for the benchmark
- todo: add quantities to existing objects on startup

### 07/28
- done object instance updating/unifying (CANNOT SPLIT FUSED OBJECTS) in the item view

### 07/19
- Done object browser

### 07/12
- some tutorials & database summaries on home page

### 05/01
- some bugfixes
- TODO: automatic gripper\_pose + object\_pose => grasp generation

### 04/29
- final step?


### 04/28
- class decorator

### 04/18
- add file processing for `entry.values.property\_element`
- todo: 
  - "webpage" home, sphinx docs
  - last: deployment on some online server
- done webpage home basic buttons

### 04/17
- sensor\_output files are now processed after uploading 

### 04/12
- fixed the setup adding/updating in the measurement uploading section
- TODO: 
  - extra files uploading
  - norach - functions to upload: measurements, entries

### 04/10
- updated the database structure to reflect the newer structure according to the thesis
- added some better validation
  - it seems that the "Python schema validation library" doesn't have the proper (or at least I couldn't find them) functions to check nested conditional types and keys

### 03/20
- some validation in the `EntrySerializer`
- thesis: willy wonka television is basically what's needed, except that it clones the chocolate bar every time

### 03/18
- first full measurement entry test done
- done most validation in serizalizers.py
  - TODO: full test of validation
- TODO: entry uploading
- TOODO: THESIS - WRITE STUFF

### 03/17
- simplified models & structure


### PI day
- the error ```Could not resolve URL for hyperlinked relationship using view name "continuousproperty-detail". You may have failed to include the related model in your API, or incorrectly configured the `lookup_field` attribute on this field.``` is caused by not having created the `ContinuousPropertyViewSet` **and** not having it registered in the `url router` in `database/urls.py`
- make the `Property` have N `PropertyElement` children, each with the same fields as the old `ContinuousProperty`, where quantity is also material/class, units mug/bottle/etc., value probability, std=0 for categories


### 03/12
- added category & continous property adding - not tested yet

### 03/11
- `Setup` & `SetupElement` are created in `perform_create()` in `views.py`
- added some todos in `views.py`
- gotta find out how to override all the saves and properly create the object hierarchies and interlink them in the correct way
- generated a new graph

### 03/10
- created test measurement json
- created some validations
- begin making `perform_create` in `views.py`

### 03/07
- begin writing tests for uploading
- image uploading test done
- begin validation
- **data can be at most a one layer deep dictionary**

### 28/02
- ObjectClass - ClassInstance (real object with unique id) - measurement of a property that one specific real object - grasp

### 26/02 - too many things to keep in mind
- tested out how to create objects on server when `perform_create()` in a viewset is called
- authenticated post command:
  - `http -a jeff:jeff POST http://127.0.0.1:8000/rest/snippets/ code="print(456)"`
the same can be done with the requests library
- **IDEA**: maybe upload the setup in the `data` field in the request in json format. This way the setup parameters can be found and matched on the server.

### 14/02
- start learning django rest & django


### random tricks
- sometimes you need to add models in `admin.py`
- migrate every time `models.py` is updated

show all urls
`py manage.py show_urls > urls_views_names.txt`

create snippet model
`python manage.py makemigrations snippets`
`python manage.py migrate snippets`

manual reset & migration
`rm -f db.sqlite3`
`rm -r snippets/migrations`
`python manage.py makemigrations snippets`
`python manage.py migrate`



