# HomeService Provider - Frontend (Next.js)

A modern, responsive Next.js frontend for the Home Service Provider system.

## Features

- 🎨 Beautiful UI with Tailwind CSS
- 🔐 Authentication (Login/Signup)
- 📱 Responsive Design
- 🔄 API Integration with backend services
- 📊 Service Browsing & Booking
- 👤 User Profile Management
- 🔔 Notification Support

## Getting Started

### Prerequisites

- Node.js 18.x or later
- npm or yarn package manager

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file with API configuration:
```bash
NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8000
```

### Running Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                 # Next.js app directory
│   ├── auth/           # Authentication pages (login, signup)
│   ├── bookings/       # Booking management
│   ├── services/       # Service listing
│   ├── profile/        # User profile
│   └── layout.jsx      # Root layout
├── components/         # Reusable React components
├── lib/                # Utility functions and API client
├── styles/             # Global CSS and Tailwind config
├── public/             # Static assets
└── package.json        # Dependencies and scripts
```

## Available Pages

- **Home** `/` - Landing page
- **Services** `/services` - Browse available services
- **Bookings** `/bookings` - View and manage bookings
- **Login** `/auth/login` - User login
- **Signup** `/auth/signup` - Create new account
- **Profile** `/profile` - User profile management

## API Integration

The frontend connects to the following backend services:

- **Customer Service** - User authentication and profiles
- **Service Provider Service** - Service listings
- **Booking Service** - Booking management
- **Notification Service** - User notifications
- **API Gateway** - Main entry point for all API calls

## Technologies Used

- **Framework**: Next.js 14+
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Language**: JavaScript/JSX
- **Package Manager**: npm

## Environment Variables

- `NEXT_PUBLIC_API_GATEWAY_URL` - API Gateway base URL (default: http://localhost:8000)

## Development Tips

1. Use `npm run dev` for hot-reloading development
2. Check [Next.js documentation](https://nextjs.org/docs) for advanced features
3. Tailwind CSS classes are used for styling - see [Tailwind docs](https://tailwindcss.com)

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

This project is part of the MTIT project.
