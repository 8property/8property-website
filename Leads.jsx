import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  Search, 
  Filter, 
  User, 
  Phone, 
  Mail, 
  MessageSquare,
  Star,
  Calendar,
  MapPin,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  Users,
  Building2
} from 'lucide-react'

const Leads = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFilter, setSelectedFilter] = useState('all')

  // Mock leads data
  const leads = [
    {
      id: 1,
      name: 'Sarah Chen',
      email: 'sarah.chen@email.com',
      phone: '+852 9123 4567',
      source: 'Instagram DM',
      status: 'hot',
      score: 95,
      interestedProperty: 'Modern 2BR Apartment in Central',
      budget: '40000-50000',
      assignedAgent: 'Michael Wong',
      lastContact: '2024-01-15T14:30:00Z',
      createdAt: '2024-01-15T10:15:00Z',
      interactions: [
        { type: 'dm', message: 'Interested in the Central apartment', time: '2024-01-15T10:15:00Z' },
        { type: 'call', message: 'Initial consultation call', time: '2024-01-15T11:30:00Z' },
        { type: 'email', message: 'Sent property details and viewing options', time: '2024-01-15T14:30:00Z' }
      ],
      notes: 'Very interested, looking to move in next month. Prefers modern apartments with good transport links.'
    },
    {
      id: 2,
      name: 'David Liu',
      email: 'david.liu@company.com',
      phone: '+852 9876 5432',
      source: 'WhatsApp',
      status: 'warm',
      score: 78,
      interestedProperty: 'Luxury 3BR Penthouse in Mid-Levels',
      budget: '80000-100000',
      assignedAgent: 'Lisa Zhang',
      lastContact: '2024-01-14T16:45:00Z',
      createdAt: '2024-01-14T09:20:00Z',
      interactions: [
        { type: 'whatsapp', message: 'Inquiry about penthouse availability', time: '2024-01-14T09:20:00Z' },
        { type: 'call', message: 'Discussed requirements and budget', time: '2024-01-14T16:45:00Z' }
      ],
      notes: 'Expatriate executive, flexible on price but specific about location and amenities.'
    },
    {
      id: 3,
      name: 'Emily Wong',
      email: 'emily.wong@gmail.com',
      phone: '+852 9555 1234',
      source: 'Instagram Comment',
      status: 'cold',
      score: 45,
      interestedProperty: 'Cozy Studio in Causeway Bay',
      budget: '25000-30000',
      assignedAgent: null,
      lastContact: '2024-01-13T12:00:00Z',
      createdAt: '2024-01-13T12:00:00Z',
      interactions: [
        { type: 'comment', message: 'Asked about studio availability', time: '2024-01-13T12:00:00Z' }
      ],
      notes: 'First-time renter, needs guidance on rental process.'
    },
    {
      id: 4,
      name: 'James Park',
      email: 'james.park@tech.com',
      phone: '+852 9333 7890',
      source: 'Instagram DM',
      status: 'converted',
      score: 100,
      interestedProperty: 'Spacious Family Home in Tai Koo',
      budget: '50000-60000',
      assignedAgent: 'Michael Wong',
      lastContact: '2024-01-12T10:30:00Z',
      createdAt: '2024-01-10T15:45:00Z',
      interactions: [
        { type: 'dm', message: 'Family home inquiry', time: '2024-01-10T15:45:00Z' },
        { type: 'viewing', message: 'Property viewing scheduled', time: '2024-01-11T14:00:00Z' },
        { type: 'contract', message: 'Lease agreement signed', time: '2024-01-12T10:30:00Z' }
      ],
      notes: 'Signed 2-year lease. Very satisfied with service.'
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'hot': return 'bg-red-100 text-red-800'
      case 'warm': return 'bg-orange-100 text-orange-800'
      case 'cold': return 'bg-blue-100 text-blue-800'
      case 'converted': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-orange-600'
    return 'text-red-600'
  }

  const getInteractionIcon = (type) => {
    switch (type) {
      case 'dm': return <MessageSquare className="w-3 h-3" />
      case 'whatsapp': return <MessageSquare className="w-3 h-3" />
      case 'call': return <Phone className="w-3 h-3" />
      case 'email': return <Mail className="w-3 h-3" />
      case 'viewing': return <Building2 className="w-3 h-3" />
      case 'contract': return <CheckCircle className="w-3 h-3" />
      case 'comment': return <MessageSquare className="w-3 h-3" />
      default: return <MessageSquare className="w-3 h-3" />
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.interestedProperty.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = selectedFilter === 'all' || lead.status === selectedFilter
    return matchesSearch && matchesFilter
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Leads</h1>
          <p className="text-gray-600 mt-1">Manage and track potential clients from all channels</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" size="sm">
            <Filter className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button size="sm">
            <Users className="w-4 h-4 mr-2" />
            Assign Agent
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Leads</p>
                <p className="text-2xl font-bold">{leads.length}</p>
              </div>
              <Users className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Hot Leads</p>
                <p className="text-2xl font-bold text-red-600">
                  {leads.filter(l => l.status === 'hot').length}
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-red-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Converted</p>
                <p className="text-2xl font-bold text-green-600">
                  {leads.filter(l => l.status === 'converted').length}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg. Score</p>
                <p className="text-2xl font-bold">
                  {Math.round(leads.reduce((sum, lead) => sum + lead.score, 0) / leads.length)}
                </p>
              </div>
              <Star className="w-8 h-8 text-yellow-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            placeholder="Search leads..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex space-x-2">
          {['all', 'hot', 'warm', 'cold', 'converted'].map((filter) => (
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

      {/* Leads List */}
      <div className="space-y-4">
        {filteredLeads.map((lead) => (
          <Card key={lead.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <User className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg text-gray-900">{lead.name}</h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <div className="flex items-center">
                          <Mail className="w-4 h-4 mr-1" />
                          {lead.email}
                        </div>
                        <div className="flex items-center">
                          <Phone className="w-4 h-4 mr-1" />
                          {lead.phone}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Status & Score</p>
                      <div className="flex items-center space-x-2">
                        <Badge className={getStatusColor(lead.status)}>
                          {lead.status}
                        </Badge>
                        <span className={`font-semibold ${getScoreColor(lead.score)}`}>
                          {lead.score}
                        </span>
                      </div>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Source</p>
                      <p className="text-sm font-medium">{lead.source}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Budget Range</p>
                      <p className="text-sm font-medium">HKD {lead.budget}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Assigned Agent</p>
                      <p className="text-sm font-medium">
                        {lead.assignedAgent || 'Unassigned'}
                      </p>
                    </div>
                  </div>

                  <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-1">Interested Property</p>
                    <p className="text-sm font-medium text-blue-600">{lead.interestedProperty}</p>
                  </div>

                  <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-2">Recent Interactions</p>
                    <div className="space-y-2">
                      {lead.interactions.slice(0, 3).map((interaction, index) => (
                        <div key={index} className="flex items-center space-x-2 text-sm">
                          <div className="flex-shrink-0 w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center">
                            {getInteractionIcon(interaction.type)}
                          </div>
                          <span className="text-gray-700">{interaction.message}</span>
                          <span className="text-gray-500 text-xs">
                            {formatDate(interaction.time)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {lead.notes && (
                    <div className="bg-gray-50 rounded-lg p-3">
                      <p className="text-xs text-gray-500 mb-1">Notes</p>
                      <p className="text-sm text-gray-700">{lead.notes}</p>
                    </div>
                  )}
                </div>

                <div className="flex flex-col space-y-2 ml-4">
                  <Button size="sm" variant="outline">
                    <MessageSquare className="w-4 h-4 mr-2" />
                    Contact
                  </Button>
                  <Button size="sm" variant="outline">
                    <Calendar className="w-4 h-4 mr-2" />
                    Schedule
                  </Button>
                  <Button size="sm" variant="outline">
                    <Building2 className="w-4 h-4 mr-2" />
                    Show Property
                  </Button>
                </div>
              </div>

              <div className="flex items-center justify-between mt-4 pt-4 border-t">
                <div className="flex items-center space-x-4 text-xs text-gray-500">
                  <div className="flex items-center">
                    <Clock className="w-3 h-3 mr-1" />
                    Created {formatDate(lead.createdAt)}
                  </div>
                  <div className="flex items-center">
                    <MessageSquare className="w-3 h-3 mr-1" />
                    Last contact {formatDate(lead.lastContact)}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button size="sm" variant="ghost">
                    View Details
                  </Button>
                  {!lead.assignedAgent && (
                    <Button size="sm">
                      Assign Agent
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredLeads.length === 0 && (
        <div className="text-center py-12">
          <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No leads found</h3>
          <p className="text-gray-600">Try adjusting your search or filter criteria</p>
        </div>
      )}
    </div>
  )
}

export default Leads

