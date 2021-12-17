# My ISP project

## Start project

With development environment

```bash
docker-compose up --build -d
```

With production environment

```bash
docker-compose up -f docker-compose.prod.yml --build -d
```

## Run Migrations

First, connect to docker container

```bash
docker exec -it [container_name] /bin/sh
```


Then, create the migrations

```bash
python manage.py makemigrations
```

Then, run the migrations

```bash
python manage.py migrate
```

## Models

- Account

```py
ser = models.OneToOneField(Realtor, on_delete=models.CASCADE,  primary_key=True, )
id = models.IntegerField()
listing = models.CharField(max_length=200)
listing_id = models.IntegerField()
name = models.CharField(max_length=200)
email = models.CharField(max_length=100)
phone = models.CharField(max_length=100)
```

- Contact

```py
user = models.ManyToManyField(Listing)
listing = models.CharField(max_length=200)
listing_id = models.IntegerField()
name = models.CharField(max_length=200)
email = models.CharField(max_length=100)
phone = models.CharField(max_length=100)
message = models.TextField(blank=True)
contact_date = models.DateTimeField(default=datetime.now, blank=True)
user_id = models.IntegerField(blank=True)
```

- Listing

```py
realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
title = models.CharField(max_length=200)
address = models.CharField(max_length=200)
city = models.CharField(max_length=100)
state = models.CharField(max_length=100)
zipcode = models.CharField(max_length=20)
description = models.TextField(blank=True)
price = models.IntegerField()
bedrooms = models.IntegerField()
bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
garage = models.IntegerField(default=0)
sqft = models.IntegerField()
lot_size = models.DecimalField(max_digits=5, decimal_places=1)
photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
is_published = models.BooleanField(default=True)
list_date = models.DateTimeField(default=datetime.now, blank=True)
```

- Realtor

```py
name = models.CharField(max_length=200)
photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
description = models.TextField(blank=True)
phone = models.CharField(max_length=20)
email = models.CharField(max_length=50)
is_mvp = models.BooleanField(default=False)
hire_date = models.DateTimeField(default=datetime.now, blank=True)
```

## Relations

- ```Listing (many) -> Realtor (one)```
- ```Contact (one) -> Account (one)```
- ```Contact (many) -> Listing (one)```
- ```Account (one) -> Realtor (one)```
- ```Realtor (many) -> Contact (many)```

## Authorization

The Django authentication system handles both authentication and authorization. Briefly, authentication verifies a user is who they claim to be, and authorization determines what an authenticated user is allowed to do. Here the term authentication is used to refer to both tasks.

The auth system consists of:

- Users
- Permissions: Binary (yes/no) flags designating whether a user may perform a certain task.
- Groups: A generic way of applying labels and permissions to more than one user.
- A configurable password hashing system
- Forms and view tools for logging in users, or restricting content
- A pluggable backend system
The authentication system in Django aims to be very generic and doesn’t provide some features commonly found in web authentication systems. Solutions for some of these common problems have been implemented in third-party packages:

- Password strength checking
- Throttling of login attempts
- Authentication against third-parties (OAuth, for example)
- Object-level permissions

```py

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                info_logger.warning('Invalid registration')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    info_logger.warning('Invalid registration')
                    return redirect('register')
                else:

                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)

                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    info_logger.info('Created new customer')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            info_logger.warning('wrong password')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')
        
```
