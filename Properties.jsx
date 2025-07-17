import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  Search, 
  Filter, 
  MapPin, 
  Bed, 
  Bath, 
  Square, 
  Eye,
  Heart,
  MessageSquare,
  Share,
  Calendar,
  DollarSign,
  Building2,
  Zap,
  Instagram,
  ExternalLink
} from 'lucide-react'

const Properties = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFilter, setSelectedFilter] = useState('all')

  // Mock property data
  const properties = [
    {
      id: 1,
      title: 'Modern 2BR Apartment in Central',
      location: 'Central, Hong Kong Island',
      price: 45000,
      currency: 'HKD',
      period: 'month',
      bedrooms: 2,
      bathrooms: 2,
      area: 800,
      image: '/api/placeholder/400/300',
      source: '28hse',
      status: 'published',
      engagement: {
        views: 1250,
        likes: 89,
        comments: 12,
        shares: 5
      },
      aiGenerated: {
        caption: 'Stunning modern apartment in the heart of Central! ✨ This beautifully designed 2-bedroom unit offers breathtaking city views and premium finishes. Perfect for professionals seeking luxury living in Hong Kong\'s financial district. 🏙️ #CentralLiving #ModernApartment #HongKongRental',
        hashtags: ['#CentralLiving', '#ModernApartment', '#HongKongRental', '#LuxuryLiving', '#CityViews'],
        style: 'engaging'
      },
      postedAt: '2024-01-15T10:30:00Z',
      scrapedAt: '2024-01-15T09:15:00Z'
    },
    {
      id: 2,
      title: 'Cozy Studio in Causeway Bay',
      location: 'Causeway Bay, Hong Kong Island',
      price: 28000,
      currency: 'HKD',
      period: 'month',
      bedrooms: 0,
      bathrooms: 1,
      area: 450,
      image: '/api/placeholder/400/300',
      source: 'squarefoot',
      status: 'pending',
      engagement: {
        views: 0,
        likes: 0,
        comments: 0,
        shares: 0
      },
      aiGenerated: {
        caption: 'Charming studio apartment in vibrant Causeway Bay! 🌟 Perfectly located near shopping and dining, this cozy space is ideal for young professionals. Efficient layout maximizes every square foot. 🏠 #CausewayBay #StudioApartment #ConvenientLiving',
        hashtags: ['#CausewayBay', '#StudioApartment', '#ConvenientLiving', '#YoungProfessionals'],
        style: 'professional'
      },
      postedAt: null,
      scrapedAt: '2024-01-15T11:45:00Z'
    },
    {
      id: 3,
      title: 'Luxury 3BR Penthouse in Mid-Levels',
      location: 'Mid-Levels, Hong Kong Island',
      price: 85000,
      currency: 'HKD',
      period: 'month',
      bedrooms: 3,
      bathrooms: 3,
      area: 1200,
      image: '/api/placeholder/400/300',
      source: 'centaline',
      status: 'published',
      engagement: {
        views: 2100,
        likes: 156,
        comments: 28,
        shares: 15
      },
      aiGenerated: {
        caption: 'Exclusive penthouse living in prestigious Mid-Levels! 🏙️ This magnificent 3-bedroom residence features panoramic harbor views, premium appliances, and elegant finishes throughout. Experience the pinnacle of Hong Kong luxury. ✨ #MidLevels #PenthouseLiving #LuxuryRental',
        hashtags: ['#MidLevels', '#PenthouseLiving', '#LuxuryRental', '#HarborViews', '#Exclusive'],
        style: 'professional'
      },
      postedAt: '2024-01-14T16:20:00Z',
      scrapedAt: '2024-01-14T15:30:00Z'
    },
    {
      id: 4,
      title: 'Spacious Family Home in Tai Koo',
      location: 'Tai Koo, Hong Kong Island',
      price: 55000,
      currency: 'HKD',
      period: 'month',
      bedrooms: 3,
      bathrooms: 2,
      area: 950,
      image: '/api/placeholder/400/300',
      source: '28hse',
      status: 'draft',
      engagement: {
        views: 0,
        likes: 0,
        comments: 0,
        shares: 0
      },
      aiGenerated: {
        caption: 'Perfect family home in peaceful Tai Koo! 🏡 This spacious 3-bedroom apartment offers comfort and convenience for growing families. Close to schools, parks, and MTR station. Your family\'s new chapter starts here! 👨‍👩‍👧‍👦 #TaiKoo #FamilyHome #SpaciousLiving',
        hashtags: ['#TaiKoo', '#FamilyHome', '#SpaciousLiving', '#FamilyFriendly', '#Convenient'],
        style: 'casual'
      },
      postedAt: null,
      scrapedAt: '2024-01-15T12:00:00Z'
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'draft': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getSourceColor = (source) => {
    switch (source) {
      case '28hse': return 'bg-blue-100 text-blue-800'
      case 'squarefoot': return 'bg-green-100 text-green-800'
      case 'centaline': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const formatPrice = (price, currency, period) => {
    return `${currency} ${price.toLocaleString()}/${period}`
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Not posted'
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const filteredProperties = properties.filter(property => {
    const matchesSearch = property.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         property.location.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = selectedFilter === 'all' || property.status === selectedFilter
    return matchesSearch && matchesFilter
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Properties</h1>
          <p className="text-gray-600 mt-1">Manage scraped properties and their AI-generated content</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" size="sm">
            <Filter className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button size="sm">
            <Zap className="w-4 h-4 mr-2" />
            Generate Content
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            placeholder="Search properties..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex space-x-2">
          {['all', 'published', 'pending', 'draft'].map((filter) => (
            <Button
              key={filter}
              variant={selectedFilter === filter ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedFilter(filter)}
              className="capitalize"
            >
              {filter}
            </Button>
          ))}
        </div>
      </div>

      {/* Properties Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredProperties.map((property) => (
          <Card key={property.id} className="overflow-hidden hover:shadow-lg transition-shadow">
            <div className="relative">
              <img
                src={property.image}
                alt={property.title}
                className="w-full h-48 object-cover"
              />
              <div className="absolute top-3 left-3 flex space-x-2">
                <Badge className={getSourceColor(property.source)}>
                  {property.source}
                </Badge>
                <Badge className={getStatusColor(property.status)}>
                  {property.status}
                </Badge>
              </div>
              {property.status === 'published' && (
                <div className="absolute top-3 right-3">
                  <Button size="sm" variant="secondary" className="bg-white/90 hover:bg-white">
                    <Instagram className="w-4 h-4" />
                  </Button>
                </div>
              )}
            </div>

            <CardContent className="p-4">
              <div className="space-y-3">
                <div>
                  <h3 className="font-semibold text-lg text-gray-900 line-clamp-2">
                    {property.title}
                  </h3>
                  <div className="flex items-center text-gray-600 mt-1">
                    <MapPin className="w-4 h-4 mr-1" />
                    <span className="text-sm">{property.location}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="text-xl font-bold text-blue-600">
                    {formatPrice(property.price, property.currency, property.period)}
                  </div>
                  <div className="flex items-center space-x-3 text-gray-500">
                    {property.bedrooms > 0 && (
                      <div className="flex items-center">
                        <Bed className="w-4 h-4 mr-1" />
                        <span className="text-sm">{property.bedrooms}</span>
                      </div>
                    )}
                    <div className="flex items-center">
                      <Bath className="w-4 h-4 mr-1" />
                      <span className="text-sm">{property.bathrooms}</span>
                    </div>
                    <div className="flex items-center">
                      <Square className="w-4 h-4 mr-1" />
                      <span className="text-sm">{property.area}ft²</span>
                    </div>
                  </div>
                </div>

                {/* AI Generated Content Preview */}
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-gray-600">AI Generated Caption</span>
                    <Badge variant="outline" className="text-xs">
                      {property.aiGenerated.style}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-700 line-clamp-3">
                    {property.aiGenerated.caption}
                  </p>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {property.aiGenerated.hashtags.slice(0, 3).map((tag, index) => (
                      <span key={index} className="text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                    {property.aiGenerated.hashtags.length > 3 && (
                      <span className="text-xs text-gray-500">
                        +{property.aiGenerated.hashtags.length - 3} more
                      </span>
                    )}
                  </div>
                </div>

                {/* Engagement Stats */}
                {property.status === 'published' && (
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center">
                        <Eye className="w-4 h-4 mr-1" />
                        {property.engagement.views}
                      </div>
                      <div className="flex items-center">
                        <Heart className="w-4 h-4 mr-1" />
                        {property.engagement.likes}
                      </div>
                      <div className="flex items-center">
                        <MessageSquare className="w-4 h-4 mr-1" />
                        {property.engagement.comments}
                      </div>
                    </div>
                    <div className="text-xs text-gray-500">
                      Posted {formatDate(property.postedAt)}
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex space-x-2 pt-2">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Eye className="w-4 h-4 mr-2" />
                    View Details
                  </Button>
                  {property.status === 'draft' && (
                    <Button size="sm" className="flex-1">
                      <Instagram className="w-4 h-4 mr-2" />
                      Publish
                    </Button>
                  )}
                  {property.status === 'pending' && (
                    <Button size="sm" variant="secondary" className="flex-1">
                      <Calendar className="w-4 h-4 mr-2" />
                      Schedule
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredProperties.length === 0 && (
        <div className="text-center py-12">
          <Building2 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No properties found</h3>
          <p className="text-gray-600">Try adjusting your search or filter criteria</p>
        </div>
      )}
    </div>
  )
}

export default Properties

