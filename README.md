# Blog API

You can access the APIs [here](https://blogapp-0mno.onrender.com/docs).

## Setup Locally
### Using virtualenv
- Clone the repo `git clone https://github.com/adhi85/blogapp.git`
- Use virtualenv to install the requirements  
        ``pip install virtualenv``   
       ``virtualenv myenv ``  
       ``myenv\Scripts\activate``
- Install by ``pip install -r requirements.txt``
- `uvicorn main:app --reload`
- Access the APIs at `localhost:8080/docs`

### By Docker
- Clone the repo
- docker build -t blogapp .
- docker run -p 80:80 blogapp
- Access at `localhost:80/docs`

## API Endpoints:
### 1. Authentication
1. Register new users
2. Login existing users
3. Update user profiles
4. Add/remove user tags
5. Get current user info
6. Change password
#### 1.1 Only for admin users (Role based Authorization)
1. Get all Users
2. Delete any user

### 2. Blogs
1. Create new blogs
2. Retrieve all blogs
3. Retrieve only the blogs of current logged in User
4. Retrieve a specific blog by ID
5. Update existing blogs
6. Delete blogs

### 3. Dashboard
1. Fetch all blogs matching user's followed tags
2. Fetch all blogs with a specific tag


