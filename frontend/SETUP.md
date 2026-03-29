# Next.js Frontend - Setup Guide

## Quick Start

### 1. Navigate to Frontend Directory
```powershell
cd frontend
```

### 2. Install Dependencies
```powershell
npm install
```

### 3. Configure Environment Variables
Update `.env.local` with your backend API gateway URL:
```
NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8000
```

### 4. Run Development Server
```powershell
npm run dev
```

The frontend will be available at: http://localhost:3000

## Project Structure Overview

```
frontend/
├── app/                          # Next.js 13+ App Router
│   ├── layout.jsx               # Root layout wrapper
│   ├── page.jsx                 # Home page
│   ├── auth/
│   │   ├── login/page.jsx      # Login page
│   │   └── signup/page.jsx     # Registration page
│   ├── services/page.jsx        # Browse services
│   ├── bookings/page.jsx        # View bookings
│   └── profile/page.jsx         # User profile
├── components/                   # Reusable React components
│   ├── Header.jsx
│   ├── ServiceCard.jsx
│   ├── LoadingSpinner.jsx
│   └── ErrorAlert.jsx
├── lib/
│   └── api.js                   # API client and service functions
├── styles/
│   └── globals.css              # Global styles
├── public/                       # Static files
├── package.json                 # Dependencies
├── next.config.js               # Next.js configuration
├── tsconfig.json                # TypeScript configuration
├── tailwind.config.js           # Tailwind CSS configuration
└── postcss.config.js            # PostCSS configuration
```

## Key Features Implemented

### Authentication
- Login page (`/auth/login`)
- Signup page (`/auth/signup`)
- Protected routes with token-based auth
- Automatic redirect to login for unauthorized access

### Services Management
- Browse all available services (`/services`)
- Service cards with detailed information
- Price display and quick booking

### Booking System
- View all user bookings (`/bookings`)
- Booking status tracking
- Create new bookings

### User Profile
- Protected profile page (`/profile`)
- User information display
- Logout functionality

## API Integration

The frontend communicates with your backend services through the API Gateway:

### Endpoints Used

**Customer Service:**
- `POST /customers/login` - User login
- `POST /customers/register` - User registration
- `GET /customers/profile` - Get user profile
- `POST /customers/logout` - User logout

**Service Provider Service:**
- `GET /service-providers/services` - List all services

**Booking Service:**
- `GET /bookings/my-bookings` - Get user's bookings
- `POST /bookings/create` - Create new booking
- `PUT /bookings/{id}` - Update booking
- `DELETE /bookings/{id}` - Cancel booking

**Notification Service:**
- `GET /notifications` - Get user notifications

## Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## Technologies Used

- **React 18** - UI library
- **Next.js 14+** - React framework with file-based routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **JavaScript/JSX** - Frontend language

## Development Tips

### Adding New Pages
1. Create a new folder in `app/` directory
2. Add `page.jsx` file with your component
3. File structure automatically becomes the route

Example:
- `app/dashboard/page.jsx` → `/dashboard` route

### Adding API Endpoints
1. Add new functions to `lib/api.js`
2. Use the `apiClient` instance with built-in auth headers

Example:
```javascript
export const newFeature = async (data) => {
  const response = await apiClient.post('/endpoint', data)
  return response.data
}
```

### Styling Components
- Use Tailwind CSS classes for styling
- Refer to [Tailwind documentation](https://tailwindcss.com)

Example:
```jsx
<div className="bg-white rounded-lg shadow-md p-6">
  <h1 className="text-2xl font-bold text-indigo-600">
    Hello World
  </h1>
</div>
```

### Protected Routes
Use `useEffect` to check for authentication token:
```javascript
useEffect(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/auth/login')
  }
}, [router])
```

## Troubleshooting

### Port Already in Use
If port 3000 is busy, use:
```bash
npm run dev -- -p 3001
```

### API Connection Issues
1. Check API Gateway is running on `http://localhost:8000`
2. Verify `NEXT_PUBLIC_API_GATEWAY_URL` in `.env.local`
3. Check browser console for CORS errors

### Build Errors
Delete node_modules and reinstall:
```bash
npm install
npm run build
```

## Next Steps

1. Customize styling and branding
2. Add more pages and components
3. Implement advanced features (filters, search, etc.)
4. Add form validation
5. Implement real-time notifications
6. Add payment integration

## Deployment

### Build Production
```bash
npm run build
```

### Deploy to Vercel (Recommended for Next.js)
```bash
npm install -g vercel
vercel
```

### Deploy to Other Platforms
- Build the project: `npm run build`
- Upload the `.next` folder and `node_modules` to your hosting platform

## Support

For issues or questions, check:
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [Axios Documentation](https://axios-http.com/docs/)
