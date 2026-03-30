'use client'

import Header from '@/components/Header'
import Footer from '@/components/Footer'
import RegisterForm from '@/components/RegisterForm'
import Link from 'next/link'

export default function RegisterPage() {
  return (
    <>
      <Header />
      <main className="min-h-screen py-12">
        <div className="max-w-md mx-auto px-4">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h1 className="text-3xl font-bold mb-2">Create Account</h1>
            <p className="text-gray-600 mb-8">
              Join HomeServe today and start booking services
            </p>

            <RegisterForm />

            <p className="text-center mt-6 text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="text-primary font-bold hover:text-secondary">
                Login here
              </Link>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
