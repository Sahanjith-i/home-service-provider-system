'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { customerAPI } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import {
  validateEmail,
  validatePhone,
  validatePassword,
  validateName,
  validateAddress,
  validatePasswordMatch,
  getPasswordStrengthColor,
  getPasswordStrengthText,
} from '@/lib/validation'

interface FieldErrors {
  name?: string
  email?: string
  phone?: string
  address?: string
  password?: string
  confirmPassword?: string
}

export default function RegisterForm() {
  const router = useRouter()
  const { setCustomer, setToken, setAuthenticated } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [passwordStrength, setPasswordStrength] = useState({ score: 'weak', strength: 0 })
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    password: '',
    confirmPassword: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setFieldErrors((prev) => ({ ...prev, [name]: '' }))
    setError('')

    // Real-time password strength check
    if (name === 'password') {
      const validation = validatePassword(value)
      setPasswordStrength({ score: validation.score, strength: validation.strength })
    }
  }

  const validateForm = (): boolean => {
    const errors: FieldErrors = {}

    if (!validateName(formData.name)) {
      errors.name = 'Name must be between 2 and 100 characters'
    }

    if (!validateEmail(formData.email)) {
      errors.email = 'Please enter a valid email address'
    }

    if (!validatePhone(formData.phone)) {
      errors.phone = 'Please enter a valid phone number'
    }

    if (!validateAddress(formData.address)) {
      errors.address = 'Address must be between 5 and 200 characters'
    }

    const pwValidation = validatePassword(formData.password)
    if (!pwValidation.isValid) {
      errors.password = 'Password must be at least 8 characters with uppercase, lowercase, and numbers'
    }

    if (!validatePasswordMatch(formData.password, formData.confirmPassword)) {
      errors.confirmPassword = 'Passwords do not match'
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
      // Register the customer
      const registerResponse = await customerAPI.register({
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        address: formData.address,
        password: formData.password,
      })

      if (registerResponse.data.success) {
        setSuccess(true)
        // Auto-login after successful registration
        const loginResponse = await customerAPI.login({
          email: formData.email,
          password: formData.password,
        })

        const { customer, token } = loginResponse.data
        if (customer && token) {
          setCustomer(customer)
          setToken(token)
          setAuthenticated(true)
          setTimeout(() => router.push('/profile'), 1500)
        }
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Registration failed'
      setError(errorMessage)
      console.log('[v0] Registration error:', errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 animate-slide-up">
      {/* Error Alert */}
      {error && (
        <div className={`p-4 rounded-lg font-medium animate-shake ${error ? 'bg-red-100 border border-red-400 text-red-700' : ''}`}>
          {error}
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="p-4 rounded-lg font-medium bg-green-100 border border-green-400 text-green-700 animate-bounce-in">
          Account created successfully! Redirecting...
        </div>
      )}

      {/* Full Name Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Full Name</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className={`w-full px-4 py-3 border-2 rounded-lg transition-smooth focus:outline-none ${
            fieldErrors.name
              ? 'border-red-500 focus:border-red-600 bg-red-50'
              : 'border-gray-300 focus:border-blue-500'
          }`}
          placeholder="John Doe"
        />
        {fieldErrors.name && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.name}</p>}
      </div>

      {/* Email Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Email Address</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className={`w-full px-4 py-3 border-2 rounded-lg transition-smooth focus:outline-none ${
            fieldErrors.email
              ? 'border-red-500 focus:border-red-600 bg-red-50'
              : 'border-gray-300 focus:border-blue-500'
          }`}
          placeholder="you@example.com"
        />
        {fieldErrors.email && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.email}</p>}
      </div>

      {/* Phone Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Phone Number</label>
        <input
          type="tel"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          required
          className={`w-full px-4 py-3 border-2 rounded-lg transition-smooth focus:outline-none ${
            fieldErrors.phone
              ? 'border-red-500 focus:border-red-600 bg-red-50'
              : 'border-gray-300 focus:border-blue-500'
          }`}
          placeholder="+1 (555) 123-4567"
        />
        {fieldErrors.phone && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.phone}</p>}
      </div>

      {/* Address Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Address</label>
        <textarea
          name="address"
          value={formData.address}
          onChange={handleChange}
          required
          rows={3}
          className={`w-full px-4 py-3 border-2 rounded-lg transition-smooth focus:outline-none resize-none ${
            fieldErrors.address
              ? 'border-red-500 focus:border-red-600 bg-red-50'
              : 'border-gray-300 focus:border-blue-500'
          }`}
          placeholder="123 Main St, City, State 12345"
        />
        {fieldErrors.address && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.address}</p>}
      </div>

      {/* Password Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className={`w-full px-4 py-3 border-2 rounded-lg transition-smooth focus:outline-none ${
            fieldErrors.password
              ? 'border-red-500 focus:border-red-600 bg-red-50'
              : 'border-gray-300 focus:border-blue-500'
          }`}
          placeholder="••••••••"
        />
        {formData.password && (
          <div className="mt-2 animate-slide-up">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-semibold text-gray-600">Strength:</span>
              <span className={`text-xs font-bold ${passwordStrength.score === 'weak' ? 'text-red-600' : passwordStrength.score === 'fair' ? 'text-yellow-600' : passwordStrength.score === 'good' ? 'text-blue-600' : 'text-green-600'}`}>
                {passwordStrength.score.charAt(0).toUpperCase() + passwordStrength.score.slice(1)}
              </span>
            </div>
            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all duration-300 ${getPasswordStrengthColor(passwordStrength.score)}`}
                style={{ width: `${(passwordStrength.strength / 5) * 100}%` }}
              ></div>
            </div>
          </div>
        )}
        {fieldErrors.password && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.password}</p>}
      </div>

      {/* Confirm Password Field */}
      <div className="stagger-item">
        <label className="block text-sm font-semibold mb-2 text-gray-800">Confirm Password</label>
        <input
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          className={`w-full px-4 py-3 border-2 rounded-lg transition-smooth focus:outline-none ${
            fieldErrors.confirmPassword
              ? 'border-red-500 focus:border-red-600 bg-red-50'
              : formData.confirmPassword && formData.password === formData.confirmPassword
              ? 'border-green-500 focus:border-green-600'
              : 'border-gray-300 focus:border-blue-500'
          }`}
          placeholder="••••••••"
        />
        {formData.confirmPassword && formData.password === formData.confirmPassword && (
          <p className="text-green-600 text-sm mt-1">✓ Passwords match</p>
        )}
        {fieldErrors.confirmPassword && <p className="text-red-600 text-sm mt-1 animate-slide-down">{fieldErrors.confirmPassword}</p>}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || success}
        className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-smooth disabled:opacity-50 disabled:cursor-not-allowed stagger-item flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <div className="spinner" style={{ width: '20px', height: '20px' }}></div>
            Creating Account...
          </>
        ) : (
          'Create Account'
        )}
      </button>
    </form>
  )
}
