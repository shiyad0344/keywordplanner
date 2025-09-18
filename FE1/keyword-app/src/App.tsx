import { useState } from 'react'
import axios from 'axios'

interface FormData {
  brand_url: string
  brand_competitor_url: string
  service_location: string[]
  shopping_ad_budget: number
  search_ad_budget: number
  pmax_ad_budget: number
}

interface Keyword {
  text: string
  avg_monthly_searches: number
}

interface KeywordResponse {
  success: boolean
  keywords: Keyword[]
  message: string
}

function App() {
  const [formData, setFormData] = useState<FormData>({
    brand_url: '',
    brand_competitor_url: '',
    service_location: [],
    shopping_ad_budget: 0,
    search_ad_budget: 0,
    pmax_ad_budget: 0
  })

  const [locationInput, setLocationInput] = useState('')
  const [keywords, setKeywords] = useState<Keyword[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    if (name.includes('budget')) {
      setFormData(prev => ({
        ...prev,
        [name]: parseFloat(value) || 0
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }))
    }
  }

  const handleLocationAdd = () => {
    if (locationInput.trim()) {
      setFormData(prev => ({
        ...prev,
        service_location: [...prev.service_location, locationInput.trim()]
      }))
      setLocationInput('')
    }
  }

  const handleLocationRemove = (index: number) => {
    setFormData(prev => ({
      ...prev,
      service_location: prev.service_location.filter((_, i) => i !== index)
    }))
  }

  const formatSearchVolume = (searches: number) => {
    if (searches >= 1000000) {
      return `${(searches / 1000000).toFixed(1)}M`
    } else if (searches >= 1000) {
      return `${(searches / 1000).toFixed(1)}K`
    }
    return searches.toString()
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setKeywords([])

    try {
      const response = await axios.post<KeywordResponse>(
          'https://keywordplanner-back.vercel.app/api/keyword-list',
          formData
      )
      if (response.data.success) {
        setKeywords(response.data.keywords)
      } else {
        setError(response.data.message || 'Failed to generate keywords')
      }
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } }
      setError(error.response?.data?.detail || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-teal-900 relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(20,184,166,0.2)_0%,transparent_50%)]"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_80%,rgba(13,148,136,0.3)_0%,transparent_50%)]"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_40%_40%,rgba(6,78,59,0.4)_0%,transparent_50%)]"></div>
        </div>

        <div className="relative z-10 py-6 sm:py-8 lg:py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            {/* Header with Branding */}
            <div className="text-center mb-8 sm:mb-10 lg:mb-12">
              <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-teal-400 via-teal-500 to-teal-600 rounded-2xl mb-4 sm:mb-6 shadow-2xl">
                <svg className="w-8 h-8 sm:w-10 sm:h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-3 sm:mb-4 bg-gradient-to-r from-teal-200 via-teal-300 to-teal-400 bg-clip-text text-transparent">
                Keyword Generator
              </h1>
              <p className="text-base sm:text-lg lg:text-xl text-teal-200 max-w-2xl mx-auto px-4">
                Generate powerful, AI-driven keywords for your digital marketing campaigns with advanced targeting and budget optimization
              </p>
            </div>

            <form onSubmit={handleSubmit} className="bg-white/10 backdrop-blur-lg border border-white/20 shadow-2xl rounded-2xl p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8">
              <div className="group">
                <label htmlFor="brand_url" className="block text-sm font-semibold text-white mb-2 flex items-center">
                  <svg className="w-4 h-4 mr-2 text-teal-300" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clipRule="evenodd" />
                  </svg>
                  Brand URL
                </label>
                <input
                    type="url"
                    id="brand_url"
                    name="brand_url"
                    value={formData.brand_url}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition-all duration-300 group-hover:bg-white/25"
                    placeholder="https://example.com"
                />
              </div>

              <div className="group">
                <label htmlFor="brand_competitor_url" className="block text-sm font-semibold text-white mb-2 flex items-center">
                  <svg className="w-4 h-4 mr-2 text-teal-300" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                  </svg>
                  Competitor URL
                </label>
                <input
                    type="url"
                    id="brand_competitor_url"
                    name="brand_competitor_url"
                    value={formData.brand_competitor_url}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition-all duration-300 group-hover:bg-white/25"
                    placeholder="https://competitor.com"
                />
              </div>

              <div className="group">
                <label className="block text-sm font-semibold text-white mb-2 flex items-center">
                  <svg className="w-4 h-4 mr-2 text-teal-300" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                  </svg>
                  Service Locations
                </label>
                <div className="flex gap-3 mb-3">
                  <input
                      type="text"
                      value={locationInput}
                      onChange={(e) => setLocationInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleLocationAdd())}
                      className="flex-1 px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition-all duration-300"
                      placeholder="Enter a city and press Enter or click Add"
                  />
                  <button
                      type="button"
                      onClick={handleLocationAdd}
                      className="px-6 py-3 bg-gradient-to-r from-teal-500 to-teal-600 text-white font-semibold rounded-xl hover:from-teal-600 hover:to-teal-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.service_location.map((location, index) => (
                      <span
                          key={index}
                          className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-teal-500/80 to-teal-600/80 backdrop-blur-sm text-white rounded-full text-sm font-medium border border-white/20 shadow-lg"
                      >
                  {location}
                        <button
                            type="button"
                            onClick={() => handleLocationRemove(index)}
                            className="text-white/80 hover:text-white hover:bg-white/20 rounded-full w-5 h-5 flex items-center justify-center transition-all duration-200"
                        >
                    ×
                  </button>
                </span>
                  ))}
                </div>
              </div>

              <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-4 sm:p-6 border border-white/10">
                <h3 className="text-base sm:text-lg font-semibold text-white mb-4 sm:mb-6 flex items-center">
                  <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-teal-300" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.51-1.31c-.562-.649-1.413-1.076-2.353-1.253V5z" clipRule="evenodd" />
                  </svg>
                  Budget Allocation
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
                  <div className="group">
                    <label htmlFor="shopping_ad_budget" className="block text-sm font-semibold text-white mb-2 flex items-center">
                      <span className="w-2 h-2 bg-teal-400 rounded-full mr-2"></span>
                      Shopping Ads ($)
                    </label>
                    <input
                        type="number"
                        id="shopping_ad_budget"
                        name="shopping_ad_budget"
                        value={formData.shopping_ad_budget}
                        onChange={handleInputChange}
                        required
                        min="0"
                        step="0.01"
                        className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition-all duration-300 group-hover:bg-white/25"
                        placeholder="5000.00"
                    />
                  </div>

                  <div className="group">
                    <label htmlFor="search_ad_budget" className="block text-sm font-semibold text-white mb-2 flex items-center">
                      <span className="w-2 h-2 bg-teal-500 rounded-full mr-2"></span>
                      Search Ads ($)
                    </label>
                    <input
                        type="number"
                        id="search_ad_budget"
                        name="search_ad_budget"
                        value={formData.search_ad_budget}
                        onChange={handleInputChange}
                        required
                        min="0"
                        step="0.01"
                        className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition-all duration-300 group-hover:bg-white/25"
                        placeholder="3000.00"
                    />
                  </div>

                  <div className="group">
                    <label htmlFor="pmax_ad_budget" className="block text-sm font-semibold text-white mb-2 flex items-center">
                      <span className="w-2 h-2 bg-teal-600 rounded-full mr-2"></span>
                      Performance Max ($)
                    </label>
                    <input
                        type="number"
                        id="pmax_ad_budget"
                        name="pmax_ad_budget"
                        value={formData.pmax_ad_budget}
                        onChange={handleInputChange}
                        required
                        min="0"
                        step="0.01"
                        className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition-all duration-300 group-hover:bg-white/25"
                        placeholder="2000.00"
                    />
                  </div>
                </div>
              </div>

              <button
                  type="submit"
                  disabled={loading || formData.service_location.length === 0}
                  className="w-full py-3 sm:py-4 bg-gradient-to-r from-teal-500 via-teal-600 to-teal-700 text-white font-bold text-base sm:text-lg rounded-2xl hover:from-teal-600 hover:via-teal-700 hover:to-teal-800 transition-all duration-300 shadow-xl hover:shadow-2xl transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none group relative overflow-hidden"
              >
            <span className="relative z-10 flex items-center justify-center">
              {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating Keywords...
                  </>
              ) : (
                  <>
                    <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
                    </svg>
                    Generate AI Keywords
                  </>
              )}
            </span>
                <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/25 to-white/0 -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
              </button>
            </form>

            {error && (
                <div className="mt-6 sm:mt-8 p-4 sm:p-6 bg-red-500/20 backdrop-blur-sm border border-red-300/30 rounded-2xl">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 sm:w-6 sm:h-6 text-red-300 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <p className="text-red-200 font-medium text-sm sm:text-base">{error}</p>
                  </div>
                </div>
            )}

            {keywords.length > 0 && (
                <div className="mt-6 sm:mt-8 bg-white/10 backdrop-blur-lg border border-white/20 shadow-2xl rounded-2xl p-4 sm:p-6 lg:p-8">
                  <div className="flex flex-col sm:flex-row sm:items-center mb-4 sm:mb-6 gap-3 sm:gap-0">
                    <div className="w-6 h-6 sm:w-8 sm:h-8 bg-gradient-to-br from-teal-400 to-teal-600 rounded-lg flex items-center justify-center mr-3 flex-shrink-0">
                      <svg className="w-4 h-4 sm:w-5 sm:h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <h2 className="text-xl sm:text-2xl font-bold text-white">Generated Keywords</h2>
                    <span className="px-3 py-1 bg-teal-500/20 text-teal-300 rounded-full text-sm font-medium border border-teal-400/30 self-start sm:ml-auto">
                {keywords.length} keywords
              </span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {keywords.map((keyword, index) => (
                        <div
                            key={index}
                            className="px-4 py-4 bg-gradient-to-r from-slate-700/50 to-slate-600/50 backdrop-blur-sm border border-white/10 rounded-xl text-white hover:from-slate-600/50 hover:to-slate-500/50 transition-all duration-300 hover:scale-[1.02] cursor-pointer group"
                        >
                          <div className="flex items-start justify-between mb-2">
                    <span className="font-medium text-sm group-hover:text-teal-300 transition-colors flex-1">
                      {keyword.text}
                    </span>
                            <svg className="w-4 h-4 text-gray-400 group-hover:text-teal-300 transition-colors flex-shrink-0 ml-2" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M8 2a1 1 0 000 2h2a1 1 0 100-2H8z" />
                              <path d="M3 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v6h-4.586l1.293-1.293a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L10.414 13H15v3a2 2 0 01-2 2H5a2 2 0 01-2-2V5zM15 11h2V9h-2v2z" />
                            </svg>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-xs text-gray-300">Monthly searches</span>
                            <span className="text-sm font-bold text-teal-300">
                      {formatSearchVolume(keyword.avg_monthly_searches)}
                    </span>
                          </div>
                        </div>
                    ))}
                  </div>
                </div>
            )}
          </div>
        </div>
      </div>
  )
}

export default App