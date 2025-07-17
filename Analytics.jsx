import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  TrendingUp, 
  TrendingDown,
  Users, 
  Building2, 
  Activity,
  Eye,
  Heart,
  MessageSquare,
  Share,
  Calendar,
  Download,
  RefreshCw
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  AreaChart,
  Area
} from 'recharts'

const Analytics = () => {
  // Mock analytics data
  const performanceMetrics = [
    { name: 'Jan', leads: 45, conversions: 12, revenue: 540000 },
    { name: 'Feb', leads: 52, conversions: 15, revenue: 675000 },
    { name: 'Mar', leads: 48, conversions: 11, revenue: 495000 },
    { name: 'Apr', leads: 61, conversions: 18, revenue: 810000 },
    { name: 'May', leads: 55, conversions: 16, revenue: 720000 },
    { name: 'Jun', leads: 67, conversions: 22, revenue: 990000 },
    { name: 'Jul', leads: 73, conversions: 25, revenue: 1125000 }
  ]

  const contentEngagement = [
    { name: 'Property Photos', views: 12500, likes: 890, comments: 156, shares: 45 },
    { name: 'Collages', views: 15200, likes: 1240, comments: 203, shares: 78 },
    { name: 'Market Updates', views: 8900, likes: 567, comments: 89, shares: 23 },
    { name: 'Agent Stories', views: 6700, likes: 445, comments: 67, shares: 12 },
    { name: 'Virtual Tours', views: 18900, likes: 1567, comments: 234, shares: 89 }
  ]

  const sourcePerformance = [
    { name: '28Hse', properties: 145, leads: 67, conversion: 24.5, color: '#3B82F6' },
    { name: 'Squarefoot', properties: 112, leads: 52, conversion: 28.1, color: '#10B981' },
    { name: 'Centaline', properties: 89, leads: 38, conversion: 22.3, color: '#F59E0B' }
  ]

  const weeklyActivity = [
    { day: 'Mon', scrapes: 45, posts: 12, leads: 8, responses: 15 },
    { day: 'Tue', scrapes: 52, posts: 14, leads: 11, responses: 18 },
    { day: 'Wed', scrapes: 48, posts: 13, leads: 9, responses: 16 },
    { day: 'Thu', scrapes: 61, posts: 16, leads: 14, responses: 22 },
    { day: 'Fri', scrapes: 55, posts: 15, leads: 12, responses: 20 },
    { day: 'Sat', scrapes: 67, posts: 18, leads: 16, responses: 25 },
    { day: 'Sun', scrapes: 43, posts: 11, leads: 7, responses: 13 }
  ]

  const agentPerformance = [
    { name: 'Michael Wong', leads: 45, conversions: 12, rate: 26.7 },
    { name: 'Lisa Zhang', leads: 38, conversions: 11, rate: 28.9 },
    { name: 'Sarah Chen', leads: 42, conversions: 9, rate: 21.4 },
    { name: 'David Liu', leads: 35, conversions: 8, rate: 22.9 }
  ]

  const formatCurrency = (value) => {
    return `HK$${(value / 1000).toFixed(0)}K`
  }

  const formatPercentage = (value) => {
    return `${value.toFixed(1)}%`
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600 mt-1">Comprehensive insights into your automation performance</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
          <Button variant="outline" size="sm">
            <Calendar className="w-4 h-4 mr-2" />
            Date Range
          </Button>
          <Button size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Key Performance Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">HK$5.36M</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +18.2% from last month
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">25.4%</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +3.1% from last month
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Response Time</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4.2min</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingDown className="w-3 h-3 mr-1" />
              -12% faster than last month
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Content Engagement</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8.7%</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +2.3% from last month
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Lead Generation & Conversion Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={performanceMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="leads" stackId="1" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.6} />
                <Area type="monotone" dataKey="conversions" stackId="2" stroke="#10B981" fill="#10B981" fillOpacity={0.8} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Revenue Growth</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis tickFormatter={formatCurrency} />
                <Tooltip formatter={(value) => [formatCurrency(value), 'Revenue']} />
                <Line type="monotone" dataKey="revenue" stroke="#8B5CF6" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Content Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Content Engagement Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={contentEngagement} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="views" fill="#3B82F6" name="Views" />
              <Bar dataKey="likes" fill="#10B981" name="Likes" />
              <Bar dataKey="comments" fill="#F59E0B" name="Comments" />
              <Bar dataKey="shares" fill="#EF4444" name="Shares" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Source Performance & Weekly Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Data Source Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {sourcePerformance.map((source) => (
                <div key={source.name} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div 
                      className="w-4 h-4 rounded-full" 
                      style={{ backgroundColor: source.color }}
                    />
                    <div>
                      <p className="font-medium">{source.name}</p>
                      <p className="text-sm text-gray-600">{source.properties} properties</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">{source.leads} leads</p>
                    <p className="text-sm text-gray-600">{formatPercentage(source.conversion)} conversion</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Weekly Activity Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyActivity}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="scrapes" stroke="#3B82F6" strokeWidth={2} name="Scrapes" />
                <Line type="monotone" dataKey="posts" stroke="#10B981" strokeWidth={2} name="Posts" />
                <Line type="monotone" dataKey="leads" stroke="#F59E0B" strokeWidth={2} name="Leads" />
                <Line type="monotone" dataKey="responses" stroke="#EF4444" strokeWidth={2} name="Responses" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Agent Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Agent Performance Comparison</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {agentPerformance.map((agent) => (
              <div key={agent.name} className="p-4 border rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold">{agent.name}</h3>
                  <Badge variant={agent.rate > 25 ? 'default' : 'secondary'}>
                    {formatPercentage(agent.rate)}
                  </Badge>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Leads</span>
                    <span className="font-medium">{agent.leads}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Conversions</span>
                    <span className="font-medium">{agent.conversions}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full" 
                      style={{ width: `${agent.rate}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* AI Performance Insights */}
      <Card>
        <CardHeader>
          <CardTitle>AI Performance Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <Activity className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <h3 className="font-semibold text-blue-900">Content Generation</h3>
              <p className="text-2xl font-bold text-blue-600 mt-2">94.2%</p>
              <p className="text-sm text-blue-700">Success Rate</p>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <TrendingUp className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <h3 className="font-semibold text-green-900">Lead Scoring</h3>
              <p className="text-2xl font-bold text-green-600 mt-2">87.5%</p>
              <p className="text-sm text-green-700">Accuracy Rate</p>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <Building2 className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <h3 className="font-semibold text-purple-900">Property Matching</h3>
              <p className="text-2xl font-bold text-purple-600 mt-2">91.8%</p>
              <p className="text-sm text-purple-700">Match Quality</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Analytics

