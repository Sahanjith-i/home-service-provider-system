'use client'

import Header from '@/components/Header'
import Footer from '@/components/Footer'
import LoginForm from '@/components/LoginForm'
import Link from 'next/link'

export default function LoginPage() {
  return (
    <>
      <Header />
      <main className="min-h-screen py-12">
        <div className="max-w-md mx-auto px-4">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h1 className="text-3xl font-bold mb-2">Login</h1>
            <p className="text-gray-600 mb-8">
              Welcome back to HomeServe
            </p>

            <LoginForm />

            <p className="text-center mt-6 text-gray-600">
              Don&apos;t have an account?{' '}
              <Link href="/register" className="text-primary font-bold hover:text-secondary">
                Register here
              </Link>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
