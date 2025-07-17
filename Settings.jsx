import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  Settings as SettingsIcon, 
  Database, 
  Zap, 
  Instagram,
  MessageSquare,
  Key,
  Globe,
  Shield,
  Bell,
  Users,
  Activity,
  Save,
  RefreshCw,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react'

const Settings = () => {
  const [activeTab, setActiveTab] = useState('services')

  // Mock service status data
  const services = [
    {
      name: '28Hse Scraper',
      status: 'online',
      url: 'https://28hse-scraper.render.com',
      lastUpdate: '2024-01-15T14:30:00Z',
      version: 'v1.2.3',
      health: 'healthy'
    },
    {
      name: 'Squarefoot Scraper',
      status: 'online',
      url: 'https://squarefoot-scraper.render.com',
      lastUpdate: '2024-01-15T14:25:00Z',
      version: 'v1.2.1',
      health: 'healthy'
    },
    {
      name: 'AI Content Enrichment',
      status: 'online',
      url: 'https://ai-enrichment.render.com',
      lastUpdate: '2024-01-15T14:35:00Z',
      version: 'v2.1.0',
      health: 'healthy'
    },
    {
      name: 'Property CRM',
      status: 'online',
      url: 'https://property-crm.render.com',
      lastUpdate: '2024-01-15T14:20:00Z',
      version: 'v1.5.2',
      health: 'healthy'
    },
    {
      name: 'Analytics Service',
      status: 'warning',
      url: 'https://analytics-service.render.com',
      lastUpdate: '2024-01-15T13:45:00Z',
      version: 'v1.0.8',
      health: 'degraded'
    }
  ]

  const integrations = [
    {
      name: 'Make.com',
      status: 'connected',
      description: 'Automation workflows and data processing',
      scenarios: 5,
      lastRun: '2024-01-15T14:30:00Z'
    },
    {
      name: 'Instagram Business',
      status: 'connected',
      description: 'Content publishing and engagement tracking',
      posts: 156,
      followers: 2847
    },
    {
      name: 'WhatsApp Business',
      status: 'connected',
      description: 'Lead communication and customer support',
      conversations: 89,
      responseRate: '94%'
    },
    {
      name: 'OpenAI API',
      status: 'connected',
      description: 'AI content generation and text processing',
      requests: 12450,
      usage: '78%'
    },
    {
      name: 'Cloudinary',
      status: 'connected',
      description: 'Image processing and storage',
      images: 1234,
      storage: '2.3GB'
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'online':
      case 'connected':
      case 'healthy': return 'bg-green-100 text-green-800'
      case 'warning':
      case 'degraded': return 'bg-yellow-100 text-yellow-800'
      case 'offline':
      case 'error': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'online':
      case 'connected':
      case 'healthy': return <CheckCircle className="w-4 h-4 text-green-600" />
      case 'warning':
      case 'degraded': return <AlertCircle className="w-4 h-4 text-yellow-600" />
      case 'offline':
      case 'error': return <AlertCircle className="w-4 h-4 text-red-600" />
      default: return <Clock className="w-4 h-4 text-gray-600" />
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

  const tabs = [
    { id: 'services', name: 'Services', icon: Database },
    { id: 'integrations', name: 'Integrations', icon: Zap },
    { id: 'api', name: 'API Keys', icon: Key },
    { id: 'automation', name: 'Automation', icon: Activity },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'security', name: 'Security', icon: Shield }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-1">Configure your automation ecosystem and integrations</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh Status
          </Button>
          <Button size="sm">
            <Save className="w-4 h-4 mr-2" />
            Save Changes
          </Button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </div>
              </button>
            )
          })}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'services' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Service Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {services.map((service) => (
                  <div key={service.name} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(service.status)}
                        <div>
                          <h3 className="font-semibold">{service.name}</h3>
                          <p className="text-sm text-gray-600">{service.url}</p>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <Badge className={getStatusColor(service.status)}>
                          {service.status}
                        </Badge>
                        <p className="text-xs text-gray-500 mt-1">
                          {service.version} • Updated {formatDate(service.lastUpdate)}
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <Button size="sm" variant="outline">
                          <Globe className="w-4 h-4 mr-2" />
                          Visit
                        </Button>
                        <Button size="sm" variant="outline">
                          <RefreshCw className="w-4 h-4 mr-2" />
                          Restart
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'integrations' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>External Integrations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {integrations.map((integration) => (
                  <div key={integration.name} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(integration.status)}
                        <div>
                          <h3 className="font-semibold">{integration.name}</h3>
                          <p className="text-sm text-gray-600">{integration.description}</p>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <Badge className={getStatusColor(integration.status)}>
                          {integration.status}
                        </Badge>
                        <div className="text-xs text-gray-500 mt-1">
                          {integration.scenarios && `${integration.scenarios} scenarios`}
                          {integration.posts && `${integration.posts} posts`}
                          {integration.conversations && `${integration.conversations} conversations`}
                          {integration.requests && `${integration.requests} requests`}
                          {integration.images && `${integration.images} images`}
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <Button size="sm" variant="outline">
                          Configure
                        </Button>
                        <Button size="sm" variant="outline">
                          Test
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'api' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>API Configuration</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      OpenAI API Key
                    </label>
                    <Input 
                      type="password" 
                      placeholder="sk-..." 
                      value="sk-••••••••••••••••••••••••••••••••••••••••"
                      readOnly
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Cloudinary Cloud Name
                    </label>
                    <Input 
                      placeholder="your-cloud-name" 
                      value="property-agency-cloud"
                      readOnly
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Instagram Access Token
                    </label>
                    <Input 
                      type="password" 
                      placeholder="IGQ..." 
                      value="IGQ••••••••••••••••••••••••••••••••••••••••"
                      readOnly
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      WhatsApp Business Token
                    </label>
                    <Input 
                      type="password" 
                      placeholder="EAA..." 
                      value="EAA••••••••••••••••••••••••••••••••••••••••"
                      readOnly
                    />
                  </div>
                </div>
                <div className="flex space-x-3">
                  <Button>Update Keys</Button>
                  <Button variant="outline">Test Connections</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'automation' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Automation Rules</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h3 className="font-semibold">Scraping Schedule</h3>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm">28Hse Scraper</span>
                        <Badge variant="outline">Every 2 hours</Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Squarefoot Scraper</span>
                        <Badge variant="outline">Every 3 hours</Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Centaline Scraper</span>
                        <Badge variant="outline">Every 4 hours</Badge>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <h3 className="font-semibold">Content Publishing</h3>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Auto-publish new properties</span>
                        <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">AI caption generation</span>
                        <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Image enhancement</span>
                        <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <h3 className="font-semibold">Lead Management</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Auto-assign leads</span>
                      <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Lead scoring</span>
                      <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Auto-responses</span>
                      <Badge className="bg-yellow-100 text-yellow-800">Partial</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'notifications' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="space-y-4">
                  <h3 className="font-semibold">System Alerts</h3>
                  <div className="space-y-3">
                    {[
                      'Service downtime',
                      'High-priority leads',
                      'Scraping errors',
                      'API rate limits',
                      'Content moderation flags'
                    ].map((alert) => (
                      <div key={alert} className="flex items-center justify-between">
                        <span className="text-sm">{alert}</span>
                        <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="space-y-4">
                  <h3 className="font-semibold">Performance Reports</h3>
                  <div className="space-y-3">
                    {[
                      'Daily summary',
                      'Weekly analytics',
                      'Monthly performance',
                      'Lead conversion reports'
                    ].map((report) => (
                      <div key={report} className="flex items-center justify-between">
                        <span className="text-sm">{report}</span>
                        <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'security' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Security Settings</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="space-y-4">
                  <h3 className="font-semibold">Access Control</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Two-factor authentication</span>
                      <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">API rate limiting</span>
                      <Badge className="bg-green-100 text-green-800">Enabled</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">IP whitelist</span>
                      <Badge className="bg-yellow-100 text-yellow-800">Partial</Badge>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <h3 className="font-semibold">Data Protection</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Data encryption</span>
                      <Badge className="bg-green-100 text-green-800">AES-256</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Backup frequency</span>
                      <Badge variant="outline">Daily</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Data retention</span>
                      <Badge variant="outline">2 years</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

export default Settings

