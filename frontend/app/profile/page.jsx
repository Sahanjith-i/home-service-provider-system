'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import ProfileForm from '@/components/ProfileForm'
import { useAuthStore } from '@/lib/store'

export default function ProfilePage() {
  const { isAuthenticated } = useAuthStore()
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return null
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 py-12">
        <div className="max-w-2xl mx-auto px-4">
          {/* Profile Header Card */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-lg shadow-lg p-8 mb-8 animate-slide-down">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-16 h-16 rounded-full bg-white bg-opacity-20 flex items-center justify-center text-3xl font-bold">
                {/* Avatar placeholder */}
                {/* removed icon as requested */}
              </div>
              <div>
                <h1 className="text-3xl font-bold">My Profile</h1>
                <p className="text-blue-100">Manage your account information</p>
              </div>
            </div>
          </div>

          {/* Profile Form Card */}
          <div className="bg-white rounded-lg shadow-lg p-8 animate-scale-in">
            <div className="border-b-2 border-gray-200 pb-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-800">Account Settings</h2>
              <p className="text-gray-600 mt-1">Update your profile details below</p>
            </div>

            <ProfileForm />
          </div>

          {/* Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
            {[
              { icon: '🔐', title: 'Security', desc: 'Your account is secure' },
              { icon: '✓', title: 'Verified', desc: 'Account verified' },
              { icon: '📋', title: 'Active', desc: 'Account is active' },
            ].map((info, idx) => (
              <div
                key={idx}
                className="bg-white rounded-lg p-4 shadow hover:shadow-md transition-smooth text-center stagger-item"
              >
                <div className="text-3xl mb-2">{info.icon}</div>
                <h3 className="font-semibold text-gray-800">{info.title}</h3>
                <p className="text-gray-600 text-sm">{info.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
