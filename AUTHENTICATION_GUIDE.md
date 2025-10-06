# Authentication System Guide

## ✅ **What's Been Implemented**

The authentication system is now fully connected between frontend and backend!

### Backend (Already Complete)
- ✅ JWT token generation and validation
- ✅ Password hashing with pbkdf2_sha256
- ✅ `/auth/register` - Create new user account
- ✅ `/auth/login` - Login and receive JWT token
- ✅ `/auth/me` - Get current user info (requires auth)
- ✅ `/auth/logout` - Logout endpoint
- ✅ CORS configured for frontend communication

### Frontend (Just Completed)
- ✅ AuthContext connected to real backend API
- ✅ Token storage in localStorage
- ✅ Auto-login on app load (persists sessions)
- ✅ Axios interceptors for automatic token inclusion
- ✅ Protected routes component
- ✅ Loading states during auth operations
- ✅ Error handling for failed auth

## 🧪 **How to Test**

### 1. Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 2. Test Registration Flow

1. Navigate to `http://localhost:5173`
2. Click "Register" in the header
3. Fill out the registration form:
   - Email: `test@example.com`
   - Password: `password123` (must be 8+ characters)
   - First Name: `John`
   - Last Name: `Doe`
4. Click "Create Account"
5. ✅ You should be automatically logged in and redirected to products page
6. ✅ Header should show "John Doe" and "Logout" button

### 3. Test Logout Flow

1. Click "Logout" in the header
2. ✅ You should be logged out
3. ✅ Header should show "Login" and "Register" buttons
4. ✅ If you check localStorage (F12 → Application → Local Storage), `auth_token` and `auth_user` should be cleared

### 4. Test Login Flow

1. Click "Login" in the header
2. Enter the credentials you registered with:
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Login"
4. ✅ You should be logged in
5. ✅ Header should show your name

### 5. Test Session Persistence

1. While logged in, refresh the page (F5)
2. ✅ You should remain logged in (auto-login works!)
3. ✅ Header still shows your name

### 6. Test Invalid Credentials

1. Logout if you're logged in
2. Try to login with wrong password
3. ✅ You should see an error message
4. ✅ You should remain on the login page

### 7. Test Password Requirements

1. Try to register with a short password (less than 8 characters)
2. ✅ You should see an error message
3. Try with 8+ characters
4. ✅ Registration should succeed

## 🔒 **How Authentication Works**

### Registration Flow
```
1. User fills registration form
   ↓
2. Frontend sends POST /auth/register
   ↓
3. Backend creates user with hashed password
   ↓
4. Backend returns user data
   ↓
5. Frontend automatically logs user in
   ↓
6. Token stored in localStorage
   ↓
7. User redirected to products page
```

### Login Flow
```
1. User enters email/password
   ↓
2. Frontend sends POST /auth/login
   ↓
3. Backend verifies credentials
   ↓
4. Backend generates JWT token
   ↓
5. Frontend stores token in localStorage
   ↓
6. Frontend fetches user data with GET /auth/me
   ↓
7. User data stored in context and localStorage
   ↓
8. User redirected to products page
```

### Auto-Login Flow (On Page Load)
```
1. App loads
   ↓
2. Check if token exists in localStorage
   ↓
3. If yes, send GET /auth/me with token
   ↓
4. If valid, user is logged in
   ↓
5. If invalid (expired), clear storage and stay logged out
```

### API Request Flow (With Auth)
```
1. User makes API request (e.g., create order)
   ↓
2. Axios interceptor adds: Authorization: Bearer <token>
   ↓
3. Backend validates token
   ↓
4. If valid, processes request
   ↓
5. If invalid, returns 401
   ↓
6. Frontend intercepts 401, clears auth, redirects to login
```

## 🗂️ **File Structure**

### Frontend Auth Files

```
frontend/src/
├── contexts/
│   └── AuthContext.tsx         # Auth state management
├── services/
│   └── api.ts                  # API calls with token handling
├── utils/
│   └── auth.ts                 # Token storage utilities
├── components/
│   └── ProtectedRoute.tsx      # Protected route wrapper
└── pages/
    ├── LoginPage.tsx           # Login form
    └── RegisterPage.tsx        # Registration form
```

### Backend Auth Files

```
backend/app/
├── main.py                     # Auth endpoints + CORS
├── auth.py                     # JWT token management
└── database.py                 # User storage & password hashing
```

## 🎯 **What's Stored Where**

### localStorage (Browser)
```javascript
{
  "auth_token": "eyJhbGciOiJIUzI1NiIs...",  // JWT token
  "auth_user": {                              // User data
    "id": 1,
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### AuthContext (React State)
```javascript
{
  user: {
    id: 1,
    email: "test@example.com",
    first_name: "John",
    last_name: "Doe"
  },
  isLoading: false,
  login: [Function],
  logout: [Function],
  register: [Function]
}
```

## 🛡️ **Security Features**

1. **Password Hashing**: Passwords never stored in plain text
2. **JWT Tokens**: Secure, stateless authentication
3. **Token Expiration**: Tokens expire after 24 hours
4. **Automatic Token Inclusion**: All API requests include auth token
5. **Auto-Logout on 401**: Invalid tokens trigger automatic logout
6. **CORS Protection**: Only allows requests from authorized origins
7. **HTTPS Ready**: When deployed, use HTTPS for secure token transmission

## 🔧 **Troubleshooting**

### "Login failed" Error
- Check backend is running on `http://localhost:8000`
- Verify email/password are correct
- Check browser console for detailed error

### Token Not Persisting
- Check browser localStorage (F12 → Application → Local Storage)
- Verify token is being stored
- Try hard refresh (Ctrl+Shift+R)

### CORS Errors
- Ensure backend CORS middleware is configured
- Verify frontend is running on `http://localhost:5173`
- Restart backend server after CORS changes

### 401 Unauthorized on Every Request
- Token might be expired or invalid
- Try logging out and logging in again
- Clear localStorage and try again

## 📝 **Next Steps**

Now that authentication is working, you can:

1. **Add Protected Routes**: Wrap order pages with `<ProtectedRoute>`
2. **Implement Order Management**: Users can create orders
3. **Add User Profile Page**: Display/edit user information
4. **Add Password Reset**: Forgot password functionality
5. **Add Email Verification**: Verify email on registration
6. **Add OAuth**: Google, GitHub login options

## 🎉 **Testing Checklist**

- [ ] Register new user
- [ ] Login with correct credentials
- [ ] Login with wrong credentials (should fail)
- [ ] Logout
- [ ] Refresh page while logged in (should stay logged in)
- [ ] Refresh page while logged out (should stay logged out)
- [ ] Register with short password (should fail)
- [ ] Check localStorage has token after login
- [ ] Check localStorage cleared after logout
- [ ] Header shows user name when logged in
- [ ] Header shows Login/Register when logged out

---

**Authentication is now fully functional! 🎉**

