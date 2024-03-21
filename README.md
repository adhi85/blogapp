# Blog API
- Every Endpoints are documented using SwaggerUI.  
- You can access the deployed APIs here. [AWS](http://ec2-13-127-109-197.ap-south-1.compute.amazonaws.com/docs) or [Render](https://blogapp-0mno.onrender.com/docs). It may take 1-1.5 minutes for loading since it is hosted in Render.   
- Tech-Stack used:  Python, FastAPI, Pydantic, MongoDB, Docker, AWS, Render.

## How to Setup Locally
### Using virtualenv
- Clone the repo `git clone https://github.com/adhi85/blogapp.git`
- Change directory: `cd blogapp`
- Create a new `.env` file and refer to `.env.example` file to fill it. (Use MongoDB as Database)
- Use virtualenv to install the requirements  
        ``pip install virtualenv``   
       ``virtualenv myenv ``  
       ``myenv\Scripts\activate``
- Install by ``pip install -r requirements.txt``
- `uvicorn main:app --reload`
- Access the APIs at [here](http://localhost:8000/docs) `localhost:8000/docs`

### By Docker
- Clone the repo: `git clone https://github.com/adhi85/blogapp.git`
- Change directory: `cd blogapp`
- Make new `.env` file and refer to `.env.example` file to fill it. (Use MongoDB as Database)
- Build the image: `docker build -t blogapp .`
- Run the container: `docker run -p 80:80 blogapp`
- Access at [here](http://localhost:80/docs/) `localhost:80/docs`

## API Endpoints:
### 1. Authentication
1. Register new users
2. Login existing users
3. Update user profiles
4. Add/remove user tags
5. Get current user info
6. Change password
#### 1.1 Only for users with __*'admin'*__ role. (Role based Access Control)
1. Get all Users
2. Delete any user
3. Delete any blog

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

## Security and Performance Measures Followed
1. Password Hashing: Uses passlib to hash passwords and securely store in the database.
2. Implemented Password validation constraints like minimum length, atleast one Uppercase,numbers etc.
3. Dependency Injection: To ensure that only authenticated users can perform the actions like creating, updating, and deleting blogs.
4. Pagination:  Limits the number of results returned per request to prevent excessive data retrieval and potential denial-of-service attacks.
5. Authorization: Check whether the authenticated user is the owner of the blog being manipulated, If not returns a 401 Unauthorized error.
6. JWT (JSON Web Tokens) Authentication.
7. Role-Based Access Control: During registration, the app validates that the role provided by the user is either 'admin' or 'user' to help prevent unauthorized access.
8. Protection Against Username and Email Duplication.
9. Error Handling: The application handles errors gracefully, returning appropriate HTTP status codes and error messages.
10. Data Protection: Only authorized users can access or modify the user data.
