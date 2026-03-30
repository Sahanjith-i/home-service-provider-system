'use client'

import { useState, useEffect } from 'react'
import { customerAPI } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { useRouter } from 'next/navigation'

export default function ProfileForm() {
  const { customer, setCustomer, logout } = useAuthStore()
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isEditMode, setIsEditMode] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    postal_code: '',
  })

  useEffect(() => {
    if (customer) {
      setFormData({
        name: customer.name,
        phone: customer.phone,
        address: customer.address,
        city: customer.city || '',
        state: customer.state || '',
        postal_code: customer.postal_code || '',
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
        city: customer.city || '',
        state: customer.state || '',
        postal_code: customer.postal_code || '',
      })
    }
  }

  const handleDeleteAccount = async () => {
    if (!customer?.customer_id) {
      setError('Customer ID not found')
      return
    }

    setDeleting(true)
    setError('')

    try {
      await customerAPI.deleteAccount(customer.customer_id)
      logout()
      router.push('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete account')
      setShowDeleteConfirm(false)
    } finally {
      setDeleting(false)
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

          {/* City Display */}
          <div className="stagger-item p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-semibold text-gray-600 uppercase mb-1">City</p>
            <p className="text-lg font-semibold text-gray-800">{formData.city || 'Not specified'}</p>
          </div>

          {/* State Display */}
          <div className="stagger-item p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-semibold text-gray-600 uppercase mb-1">State</p>
            <p className="text-lg font-semibold text-gray-800">{formData.state || 'Not specified'}</p>
          </div>

          {/* Postal Code Display */}
          <div className="stagger-item p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-semibold text-gray-600 uppercase mb-1">Postal Code</p>
            <p className="text-lg font-semibold text-gray-800">{formData.postal_code || 'Not specified'}</p>
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

          {/* City Field */}
          <div className="stagger-item">
            <label className="block text-sm font-semibold mb-2 text-gray-800">City</label>
            <input
              type="text"
              name="city"
              value={formData.city}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-blue-50 transition-smooth"
              placeholder="City"
            />
          </div>

          {/* State Field */}
          <div className="stagger-item">
            <label className="block text-sm font-semibold mb-2 text-gray-800">State</label>
            <input
              type="text"
              name="state"
              value={formData.state}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-blue-50 transition-smooth"
              placeholder="State"
            />
          </div>

          {/* Postal Code Field */}
          <div className="stagger-item">
            <label className="block text-sm font-semibold mb-2 text-gray-800">Postal Code</label>
            <input
              type="text"
              name="postal_code"
              value={formData.postal_code}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-blue-50 transition-smooth"
              placeholder="12345"
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

      {/* Danger Zone - Delete Account */}
      <div className="mt-8 p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-bold text-red-800 mb-4">Danger Zone</h3>
        <p className="text-red-700 mb-4">
          Once you delete your account, there is no going back. Please be certain.
        </p>

        {!showDeleteConfirm ? (
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="bg-red-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-700 transition-colors"
          >
            Delete Account
          </button>
        ) : (
          <div className="space-y-4">
            <p className="text-red-800 font-semibold">
              Are you sure you want to delete your account? This action cannot be undone.
            </p>
            <div className="flex gap-3">
              <button
                onClick={handleDeleteAccount}
                disabled={deleting}
                className="bg-red-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {deleting ? (
                  <>
                    <div className="spinner" style={{ width: '16px', height: '16px' }}></div>
                    Deleting...
                  </>
                ) : (
                  'Yes, Delete Account'
                )}
              </button>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                disabled={deleting}
                className="bg-gray-400 text-white px-4 py-2 rounded-lg font-semibold hover:bg-gray-500 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
