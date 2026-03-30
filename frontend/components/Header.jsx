'use client'

import Link from 'next/link'
import { useAuthStore } from '@/lib/store'
import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'

export default function Header() {
  const { isAuthenticated, customer, logout } = useAuthStore()
  const router = useRouter()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [isHydrated, setIsHydrated] = useState(false)

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/register', label: 'Register' },
    { href: '/login', label: 'Login' },
  ]

  useEffect(() => {
    setIsHydrated(true)
  }, [])

  const showAuth = isHydrated ? isAuthenticated : false

  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg sticky top-0 z-50 animate-slide-down">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="text-2xl font-bold group-hover:scale-110 transition-smooth">
            HomeServe
          </div>
          <div className="hidden sm:block text-xs bg-white bg-opacity-20 px-2 py-1 rounded-full font-semibold">Premium</div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          {!showAuth && navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-white font-medium relative group hover:text-blue-100 transition-smooth"
            >
              {link.label}
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-white group-hover:w-full transition-all duration-300"></span>
            </Link>
          ))}
        </nav>

        {/* Auth Section */}
        <div className="hidden md:flex gap-4 items-center">
          {showAuth ? (
            <>
              <div className="flex items-center gap-3 px-4 py-2 rounded-lg bg-white bg-opacity-10 backdrop-blur">
                <div className="w-8 h-8 rounded-full bg-white bg-opacity-20 flex items-center justify-center text-white text-sm font-bold">
                  {customer?.name?.charAt(0).toUpperCase() || 'U'}
                </div>
                <span className="text-sm font-medium">{customer?.name || 'User'}</span>
              </div>
              <Link
                href="/profile"
                className="text-white px-4 py-2 rounded-lg hover:bg-white hover:bg-opacity-20 transition-smooth font-medium"
              >
                Profile
              </Link>
              <button
                onClick={handleLogout}
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-smooth font-medium shadow-md hover:shadow-lg"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-white px-4 py-2 rounded-lg hover:bg-white hover:bg-opacity-20 transition-smooth font-medium"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="bg-white text-blue-600 px-6 py-2 rounded-lg hover:shadow-lg transition-smooth font-medium hover:scale-105"
              >
                Register
              </Link>
            </>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden flex flex-col gap-1.5"
          aria-label="Toggle menu"
        >
          <span className={`w-6 h-0.5 bg-white transition-smooth ${mobileMenuOpen ? 'rotate-45 translate-y-2' : ''}`}></span>
          <span className={`w-6 h-0.5 bg-white transition-smooth ${mobileMenuOpen ? 'opacity-0' : ''}`}></span>
          <span className={`w-6 h-0.5 bg-white transition-smooth ${mobileMenuOpen ? '-rotate-45 -translate-y-2' : ''}`}></span>
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden animate-slide-down border-t border-blue-500 border-opacity-30">
          <div className="max-w-6xl mx-auto px-4 py-4 flex flex-col gap-3">
            {!showAuth && navLinks.map((link, index) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="text-white font-medium hover:text-blue-100 transition-smooth stagger-item"
              >
                {link.label}
              </Link>
            ))}
            {showAuth ? (
              <>
                <Link
                  href="/profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-white font-medium hover:text-blue-100 transition-smooth"
                >
                  Profile ({customer?.name})
                </Link>
                <button
                  onClick={() => {
                    handleLogout()
                    setMobileMenuOpen(false)
                  }}
                  className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-smooth font-medium w-full"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-white font-medium hover:text-blue-100 transition-smooth"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium text-center hover:shadow-lg"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  )
}
