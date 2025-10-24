# Authentication Setup Guide

## Overview
This project now includes a simple and secure authentication system using JWT tokens and MySQL database.

## Database Setup

### 1. Create the required tables
Make sure you have created the following tables in your `ml_project` database:

```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table (optional, for session management)
CREATE TABLE user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    session_token VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 2. Database Configuration
Update your environment variables or create a `.env` file:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=33060
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ml_project

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
```

## API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "confirm_password": "SecurePassword123"
}
```

#### Login User
```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "SecurePassword123"
}
```

#### Get User Profile
```http
GET /api/v1/auth/profile
Authorization: Bearer <your-jwt-token>
```

#### Validate Token
```http
POST /api/v1/auth/validate-token
Authorization: Bearer <your-jwt-token>
```

#### Refresh Token
```http
POST /api/v1/auth/refresh-token
Authorization: Bearer <your-jwt-token>
```

## Frontend Integration

### 1. Authentication Context
The frontend uses React Context for authentication state management. The `AuthContext` provides:

- `user`: Current user object
- `isAuthenticated`: Boolean authentication status
- `isLoading`: Loading state
- `login(email, password)`: Login function
- `register(userData)`: Registration function
- `logout()`: Logout function

### 2. Protected Routes
Use the `ProtectedRoute` component to protect routes that require authentication:

```jsx
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Layout>
        <DashboardPage />
      </Layout>
    </ProtectedRoute>
  }
/>
```

### 3. API Integration
The frontend automatically includes JWT tokens in API requests via axios interceptors.

## Testing

### 1. Run the test script
```bash
cd backend
python test_auth.py
```

This will test:
- User registration
- User login
- Protected endpoint access
- Token validation
- Token refresh
- Invalid credentials handling
- Unauthorized access handling

### 2. Manual testing with curl

#### Register a user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123",
    "confirm_password": "TestPassword123"
  }'
```

#### Login:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

#### Access protected endpoint:
```bash
curl -X GET http://localhost:8000/api/v1/auth/profile \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Security Features

### 1. Password Security
- Passwords are hashed using bcrypt
- Minimum 8 characters required
- Must contain uppercase, lowercase, and numbers
- Passwords are never stored in plain text

### 2. JWT Tokens
- Tokens expire after 1 hour (configurable)
- Tokens include user ID, username, and email
- Automatic token refresh capability
- Secure token validation

### 3. Input Validation
- Email format validation
- Username validation (minimum 2 characters)
- Password strength validation
- SQL injection protection via parameterized queries

### 4. CORS Protection
- Configured for development (localhost:3000)
- Can be configured for production domains

## Production Considerations

### 1. Environment Variables
- Change `JWT_SECRET_KEY` to a strong, random secret
- Use environment-specific database credentials
- Set `DEBUG=false` for production

### 2. Database Security
- Use strong database passwords
- Limit database user permissions
- Enable SSL connections in production

### 3. HTTPS
- Always use HTTPS in production
- Update CORS settings for production domains

### 4. Rate Limiting
Consider adding rate limiting for authentication endpoints to prevent brute force attacks.

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check database credentials
   - Ensure MySQL is running on port 33060
   - Verify database `ml_project` exists

2. **JWT Token Invalid**
   - Check `JWT_SECRET_KEY` is set
   - Verify token hasn't expired
   - Ensure token is sent in Authorization header

3. **CORS Errors**
   - Check CORS configuration in `main.py`
   - Ensure frontend URL is in allowed origins

4. **User Already Exists**
   - Check if email/username is already registered
   - Use different credentials for testing

### Debug Mode
Set `DEBUG=true` in your environment to enable:
- Detailed error messages
- API documentation at `/docs`
- ReDoc documentation at `/redoc`

## Next Steps

1. **User Management**: Add user profile update functionality
2. **Password Reset**: Implement password reset via email
3. **Role-Based Access**: Add user roles and permissions
4. **Session Management**: Implement session tracking and management
5. **Audit Logging**: Add authentication event logging

