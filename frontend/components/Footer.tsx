'use client'

import Link from 'next/link'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  const footerSections = [
    {
      title: 'HomeServe',
      items: ['Your trusted home service provider platform', 'Connecting customers with quality service providers'],
      isInfo: true,
    },
    {
      title: 'Quick Links',
      items: [
        { label: 'Home', href: '/' },
        { label: 'About Us', href: '#' },
        { label: 'Services', href: '#' },
        { label: 'Contact', href: '#' },
      ],
    },
    {
      title: 'Support',
      items: [
        { label: 'Help Center', href: '#' },
        { label: 'Privacy Policy', href: '#' },
        { label: 'Terms of Service', href: '#' },
        { label: 'FAQs', href: '#' },
      ],
    },
    {
      title: 'Contact',
      items: [
        'Email: support@homeserve.com',
        'Phone: 1-800-SERVE',
        'Available 24/7',
      ],
      isInfo: true,
    },
  ]

  return (
    <footer className="bg-gradient-to-b from-gray-900 to-black text-white mt-20 animate-fade-in">
      {/* Main Footer Content */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {footerSections.map((section, idx) => (
            <div key={idx} className="stagger-item">
              <h3 className="font-bold text-lg mb-4 text-white group inline-block">
                {section.title}
                <span className="block w-0 h-0.5 bg-gradient-to-r from-blue-600 to-blue-400 group-hover:w-full transition-all duration-300 mt-1"></span>
              </h3>

              {section.isInfo ? (
                <div className="space-y-2">
                  {section.items.map((item, i) => (
                    <p key={i} className="text-gray-400 hover:text-blue-400 transition-smooth">
                      {item}
                    </p>
                  ))}
                </div>
              ) : (
                <ul className="space-y-2">
                  {section.items.map((item, i) => (
                    <li key={i}>
                      <Link
                        href={item.href}
                        className="text-gray-400 hover:text-blue-400 transition-smooth relative group inline-block"
                      >
                        {item.label}
                        <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-400 group-hover:w-full transition-all duration-300"></span>
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>

        {/* Social Links */}
        <div className="border-t border-gray-700 pt-8 mb-8">
          <div className="flex justify-center gap-6 mb-6">
            {['Facebook', 'Twitter', 'Instagram', 'LinkedIn'].map((social, idx) => (
              <a
                key={idx}
                href="#"
                className="w-10 h-10 rounded-full bg-gray-800 hover:bg-blue-600 flex items-center justify-center transition-smooth transform hover:scale-110 text-sm font-semibold stagger-item"
              >
                {social.charAt(0)}
              </a>
            ))}
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-700 pt-8 text-center text-gray-500">
          <p className="mb-2">
            &copy; {currentYear} HomeServe. All rights reserved. | Built with care for quality service
          </p>
          <p className="text-xs text-gray-600">
            Made with ❤️ to connect customers with trusted service providers
          </p>
        </div>
      </div>
    </footer>
  )
}
