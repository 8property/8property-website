import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  TrendingUp, 
  Users, 
  Building2, 
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Play,
  Pause,
  RefreshCw,
  Eye,
  MessageSquare,
  Heart
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'

const Dashboard = () => {
  // Mock data for charts
  const leadTrendData = [
    { name: 'Mon', leads: 12, conversions: 3 },
    { name: 'Tue', leads: 19, conversions: 5 },
    { name: 'Wed', leads: 15, conversions: 4 },
    { name: 'Thu', leads: 22, conversions: 7 },
    { name: 'Fri', leads: 28, conversions: 8 },
    { name: 'Sat', leads: 35, conversions: 12 },
    { name: 'Sun', leads: 31, conversions: 10 }
  ]

  const contentPerformanceData = [
    { name: 'Property Photos', engagement: 85 },
    { name: 'Collages', engagement: 92 },
    { name: 'Market News', engagement: 67 },
    { name: 'Agent Highlights', engagement: 74 }
  ]

  const sourceDistribution = [
    { name: '28Hse', value: 45, color: '#3B82F6' },
    { name: 'Squarefoot', value: 35, color: '#10B981' },
    { name: 'Centaline', value: 20, color: '#F59E0B' }
  ]

  const recentActivities = [
    { type: 'scrape', message: 'New properties scraped from 28Hse', time: '2 minutes ago', count: 15 },
    { type: 'lead', message: 'High-quality lead generated', time: '5 minutes ago', score: 95 },
    { type: 'post', message: 'Instagram post published', time: '12 minutes ago', engagement: '2.3k views' },
    { type: 'conversion', message: 'Lead converted to viewing', time: '18 minutes ago', agent: 'Sarah Chen' },
    { type: 'ai', message: 'Content enrichment completed', time: '25 minutes ago', count: 8 }
  ]

  const getActivityIcon = (type) => {
    switch (type) {
      case 'scrape': return <Building2 className="w-4 h-4 text-blue-600" />
      case 'lead': return <Users className="w-4 h-4 text-green-600" />
      case 'post': return <Eye className="w-4 h-4 text-purple-600" />
      case 'conversion': return <TrendingUp className="w-4 h-4 text-orange-600" />
      case 'ai': return <Activity className="w-4 h-4 text-pink-600" />
      default: return <Activity className="w-4 h-4 text-gray-600" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back! Here's what's happening with your property automation.</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh Data
          </Button>
          <Button size="sm">
            <Play className="w-4 h-4 mr-2" />
            Run Scraper
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,247</div>
            <div className="flex items-center text-xs text-green-600">
              <ArrowUpRight className="w-3 h-3 mr-1" />
              +12.5% from last week
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Properties</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">342</div>
            <div className="flex items-center text-xs text-green-600">
              <ArrowUpRight className="w-3 h-3 mr-1" />
              +8.2% from last week
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24.8%</div>
            <div className="flex items-center text-xs text-red-600">
              <ArrowDownRight className="w-3 h-3 mr-1" />
              -2.1% from last week
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">System Uptime</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">99.9%</div>
            <div className="flex items-center text-xs text-green-600">
              <ArrowUpRight className="w-3 h-3 mr-1" />
              +0.1% from last week
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Lead Generation Trend */}
        <Card>
          <CardHeader>
            <CardTitle>Lead Generation Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={leadTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="leads" stroke="#3B82F6" strokeWidth={2} />
                <Line type="monotone" dataKey="conversions" stroke="#10B981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Content Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Content Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={contentPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="engagement" fill="#8B5CF6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Data Sources */}
        <Card>
          <CardHeader>
            <CardTitle>Data Sources</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={sourceDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {sourceDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {sourceDistribution.map((source) => (
                <div key={source.name} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div 
                      className="w-3 h-3 rounded-full mr-2" 
                      style={{ backgroundColor: source.color }}
                    />
                    <span className="text-sm">{source.name}</span>
                  </div>
                  <span className="text-sm font-medium">{source.value}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <div className="flex items-center space-x-2 mt-1">
                      <p className="text-xs text-gray-500">{activity.time}</p>
                      {activity.count && (
                        <Badge variant="secondary" className="text-xs">
                          {activity.count} items
                        </Badge>
                      )}
                      {activity.score && (
                        <Badge variant="secondary" className="text-xs">
                          Score: {activity.score}
                        </Badge>
                      )}
                      {activity.engagement && (
                        <Badge variant="secondary" className="text-xs">
                          {activity.engagement}
                        </Badge>
                      )}
                      {activity.agent && (
                        <Badge variant="secondary" className="text-xs">
                          Agent: {activity.agent}
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

