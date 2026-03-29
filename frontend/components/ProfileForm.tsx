'use client'

import { useState, useEffect } from 'react'
import { customerAPI } from '@/lib/api'
import { useAuthStore } from '@/lib/store'

export default function ProfileForm() {
  const { customer, setCustomer } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isEditMode, setIsEditMode] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: '',
  })

  useEffect(() => {
    if (customer) {
      setFormData({
        name: customer.name,
        phone: customer.phone,
        address: customer.address,
      })
    }
  }, [customer])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setSaving(true)

    try {
      if (!customer?.customer_id) {
        setError('Customer ID not found')
        return
      }

      const response = await customerAPI.updateProfile(
        customer.customer_id,
        formData
      )

      const updated = response.data.customer
      setCustomer(updated)
      setSuccess('Profile updated successfully!')
      setIsEditMode(false)
      setTimeout(() => setSuccess(''), 3000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update profile')
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    setIsEditMode(false)
    setError('')
    if (customer) {
      setFormData({
        name: customer.name,
        phone: customer.phone,
        address: customer.address,
      })
    }
  }

  return (
    <div className="space-y-6 animate-slide-up">
      {/* Error Alert */}
      {error && (
        <div className="p-4 rounded-lg font-medium bg-red-100 border border-red-400 text-red-700 animate-shake flex items-center gap-2">
          <span>⚠️</span>
          {error}
        </div>
      )}

      {/* Success Alert */}
      {success && (
        <div className="p-4 rounded-lg font-medium bg-green-100 border border-green-400 text-green-700 animate-bounce-in flex items-center gap-2">
          <span>✓</span>
          {success}
        </div>
      )}

      {/* Account Info Card */}
      <div className="bg-gradient-to-r from-blue-50 to-blue-100 border-l-4 border-blue-600 p-6 rounded-lg stagger-item">
        <h3 className="font-bold text-gray-800 mb-4 text-lg">Account Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-xs font-semibold text-gray-600 uppercase">Customer ID</p>
            <p className="text-gray-800 font-mono">{customer?.customer_id}</p>
          </div>
          <div>
            <p className="text-xs font-semibold text-gray-600 uppercase">Email</p>
            <p className="text-gray-800">{customer?.email}</p>
          </div>
          <div>
            <p className="text-xs font-semibold text-gray-600 uppercase">Member Since</p>
            <p className="text-gray-800">
              {customer?.created_at ? new Date(customer.created_at).toLocaleDateString() : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* View Mode */}
      {!isEditMode && (
        <div className="space-y-4 animate-fade-in">
          {/* Full Name Display */}
          <div className="stagger-item p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-semibold text-gray-600 uppercase mb-1">Full Name</p>
            <p className="text-lg font-semibold text-gray-800">{formData.name}</p>
          </div>

          {/* Phone Display */}
          <div className="stagger-item p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-semibold text-gray-600 uppercase mb-1">Phone Number</p>
            <p className="text-lg font-semibold text-gray-800">{formData.phone}</p>
          </div>

          {/* Address Display */}
          <div className="stagger-item p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-semibold text-gray-600 uppercase mb-1">Address</p>
            <p className="text-gray-800 whitespace-pre-wrap">{formData.address}</p>
          </div>

          {/* Edit Button */}
          <button
            onClick={() => setIsEditMode(true)}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-smooth stagger-item flex items-center justify-center gap-2 group"
          >
            <span>✏️</span>
            <span>Edit Profile</span>
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </button>
        </div>
      )}

      {/* Edit Mode Form */}
      {isEditMode && (
        <form onSubmit={handleSubmit} className="space-y-4 animate-scale-in">
          {/* Full Name Field */}
          <div className="stagger-item">
            <label className="block text-sm font-semibold mb-2 text-gray-800">Full Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-blue-50 transition-smooth"
              placeholder="Your full name"
            />
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
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-blue-50 transition-smooth"
              placeholder="+1 (555) 123-4567"
            />
          </div>

          {/* Address Field */}
          <div className="stagger-item">
            <label className="block text-sm font-semibold mb-2 text-gray-800">Address</label>
            <textarea
              name="address"
              value={formData.address}
              onChange={handleChange}
              required
              rows={4}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-blue-50 transition-smooth resize-none"
              placeholder="123 Main St, City, State 12345"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4 stagger-item">
            {/* Save Button */}
            <button
              type="submit"
              disabled={saving}
              className="flex-1 bg-gradient-to-r from-green-600 to-green-800 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-smooth disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {saving ? (
                <>
                  <div className="spinner" style={{ width: '18px', height: '18px' }}></div>
                  <span>Saving...</span>
                </>
              ) : (
                <>
                  <span>✓</span>
                  <span>Save Changes</span>
                </>
              )}
            </button>

            {/* Cancel Button */}
            <button
              type="button"
              onClick={handleCancel}
              disabled={saving}
              className="flex-1 bg-gray-400 text-white py-3 rounded-lg font-semibold hover:bg-gray-500 transition-smooth disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
