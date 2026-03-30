'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { customerAPI } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { validateEmail } from '@/lib/validation'

interface FieldErrors {
  email?: string
  password?: string
}

export default function LoginForm() {
  const router = useRouter()
  const { setCustomer, setToken, setAuthenticated } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setFieldErrors((prev) => ({ ...prev, [name]: '' }))
    setError('')
  }

  const validateForm = (): boolean => {
    const errors: FieldErrors = {}

    if (!validateEmail(formData.email)) {
      errors.email = 'Please enter a valid email address'
    }

    if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters'
    }

    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess(false)

    if (!validateForm()) {
      return
    }

    setLoading(true)

    try {
      const response = await customerAPI.login({
        email: formData.email,
        password: formData.password,
      })

      const { customer, token } = response.data
      
      if (customer && token) {
        setSuccess(true)
        setCustomer(customer)
        setToken(token)
        setAuthenticated(true)
        setTimeout(() => router.push('/profile'), 1500)
      } else {
        setError('Invalid response from server')
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Login failed'
      setError(errorMessage)
      console.log('[v0] Login error:', errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 animate-slide-up">
      {/* Error Alert */}
      {error && (
        <div className="p-4 rounded-lg font-medium bg-red-100 border border-red-400 text-red-700 animate-shake">
          {error}
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="p-4 rounded-lg font-medium bg-green-100 border border-green-400 text-green-700 animate-bounce-in flex items-center gap-2">
          <span>✓</span>
          <span>Login successful! Redirecting...</span>
        </div>
      )}

      {/* Email Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Email Address</label>
        <div className="relative">
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className={`w-full px-4 py-3 pl-10 border-2 rounded-lg transition-smooth focus:outline-none ${
              fieldErrors.email
                ? 'border-red-500 focus:border-red-600 bg-red-50'
                : 'border-gray-300 focus:border-blue-500'
            }`}
            placeholder="you@example.com"
          />
          <span className="absolute left-3 top-3.5 text-gray-400">✉️</span>
        </div>
        {fieldErrors.email && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.email}</p>}
      </div>

      {/* Password Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Password</label>
        <div className="relative">
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className={`w-full px-4 py-3 pl-10 border-2 rounded-lg transition-smooth focus:outline-none ${
              fieldErrors.password
                ? 'border-red-500 focus:border-red-600 bg-red-50'
                : 'border-gray-300 focus:border-blue-500'
            }`}
            placeholder="••••••••"
          />
          <span className="absolute left-3 top-3.5 text-gray-400">🔒</span>
        </div>
        {fieldErrors.password && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.password}</p>}
      </div>

      {/* Remember Me & Forgot Password */}
      <div className="flex items-center justify-between text-sm stagger-item">
        <label className="flex items-center gap-2 cursor-pointer hover:text-blue-600 transition-smooth">
          <input type="checkbox" className="rounded" />
          <span>Remember me</span>
        </label>
        <a href="#" className="text-blue-600 hover:text-blue-800 transition-smooth font-medium">
          Forgot password?
        </a>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || success}
        className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-smooth disabled:opacity-50 disabled:cursor-not-allowed stagger-item flex items-center justify-center gap-2 group"
      >
        {loading ? (
          <>
            <div className="spinner" style={{ width: '20px', height: '20px' }}></div>
            <span>Logging in...</span>
          </>
        ) : (
          <>
            <span>Login</span>
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </>
        )}
      </button>

      {/* Sign Up Link */}
      <p className="text-center text-gray-600 stagger-item">
        Don&apos;t have an account?{' '}
        <a href="/register" className="text-blue-600 font-semibold hover:text-blue-800 transition-smooth">
          Sign up here
        </a>
      </p>
    </form>
  )
}
