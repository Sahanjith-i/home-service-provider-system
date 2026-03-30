'use client'

import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'
import { useAuthStore } from '@/lib/store'

export default function Home() {
  const { isAuthenticated } = useAuthStore()

  const features = [
    {
      icon: '🔐',
      title: 'Secure & Safe',
      description: 'Your information is protected with enterprise-grade security and encryption',
    },
    {
      icon: '⚡',
      title: 'Fast & Easy',
      description: 'Book services quickly and easily through our intuitive platform',
    },
    {
      icon: '⭐',
      title: 'Trusted Partners',
      description: 'Join thousands of satisfied customers and verified service providers',
    },
    {
      icon: '📱',
      title: 'Always Available',
      description: '24/7 support and service booking at your fingertips',
    },
    {
      icon: '✓',
      title: 'Quality Guaranteed',
      description: 'Only verified professionals with excellent ratings and reviews',
    },
    {
      icon: '💰',
      title: 'Best Prices',
      description: 'Competitive rates and transparent pricing with no hidden fees',
    },
  ]

  return (
    <>
      <Header />
      <main className="min-h-screen">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-blue-900 text-white py-24 md:py-32 relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>

          <div className="max-w-6xl mx-auto px-4 text-center relative z-10">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-slide-up text-balance">
              Welcome to <span className="text-blue-200">HomeServe</span>
            </h1>
            <p className="text-xl md:text-2xl text-blue-100 mb-10 animate-slide-up leading-relaxed" style={{ animationDelay: '0.2s' }}>
              Your trusted partner for quality home services. Connect with verified professionals and get things done.
            </p>
            {!isAuthenticated && (
              <div className="flex gap-4 justify-center flex-wrap animate-slide-up" style={{ animationDelay: '0.4s' }}>
                <Link
                  href="/register"
                  className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-smooth hover:scale-105 inline-block"
                >
                  Get Started Free
                </Link>
                <Link
                  href="/login"
                  className="border-2 border-white text-white px-8 py-4 rounded-lg font-bold hover:bg-white hover:text-blue-600 transition-smooth hover:scale-105 inline-block"
                >
                  Login
                </Link>
              </div>
            )}
          </div>
        </section>

        {/* Features Section */}
        <section className="max-w-6xl mx-auto px-4 py-20 md:py-28">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 animate-fade-in">Why Choose HomeServe?</h2>
            <p className="text-xl text-gray-600 animate-fade-in" style={{ animationDelay: '0.2s' }}>
              Everything you need to find and book trusted home services
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="bg-gradient-to-br from-gray-50 to-gray-100 p-8 rounded-xl shadow-md hover:shadow-xl transition-smooth hover:-translate-y-2 group stagger-item border border-gray-200"
              >
                <div className="text-5xl mb-4 group-hover:scale-125 transition-smooth inline-block">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3 text-gray-800 group-hover:text-blue-600 transition-smooth">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Stats Section */}
        <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-16">
          <div className="max-w-6xl mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
              {[
                { stat: '10K+', label: 'Happy Customers' },
                { stat: '500+', label: 'Verified Professionals' },
                { stat: '50+', label: 'Service Categories' },
                { stat: '98%', label: 'Satisfaction Rate' },
              ].map((item, idx) => (
                <div key={idx} className="stagger-item">
                  <div className="text-4xl md:text-5xl font-bold mb-2">{item.stat}</div>
                  <p className="text-blue-100">{item.label}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-br from-blue-50 to-gray-50 py-20 md:py-28">
          <div className="max-w-4xl mx-auto px-4 text-center animate-fade-in">
            <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
            <p className="text-xl text-gray-600 mb-10">
              Join thousands of customers who trust HomeServe for their service needs. Sign up in minutes and book your first service today.
            </p>
            {!isAuthenticated && (
              <Link
                href="/register"
                className="inline-block bg-gradient-to-r from-blue-600 to-blue-800 text-white px-10 py-4 rounded-lg font-bold hover:shadow-lg transition-smooth hover:scale-105 text-lg"
              >
                Create Free Account →
              </Link>
            )}
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
