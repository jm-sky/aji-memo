'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useUser } from '@/lib/hooks/useAuth'
import { Building2, CreditCard, Activity, TrendingUp, Brain } from 'lucide-react'

export default function DashboardPage() {
  const { data: user } = useUser()

  const stats = [
    {
      name: 'Memories Stored',
      value: '127',
      icon: Brain,
      change: '+12%',
      changeType: 'positive' as const,
    },
    {
      name: 'API Calls This Month',
      value: '89',
      icon: Activity,
      change: '+8%',
      changeType: 'positive' as const,
    },
    {
      name: 'Plan Usage',
      value: user?.subscription_tier === 'free' ? '89/100' : '89/1000', // TODO: change to actual usage
      icon: TrendingUp,
      change: user?.subscription_tier === 'free' ? '89%' : '8.9%', // TODO: change to actual usage
      changeType: user?.subscription_tier === 'free' ? 'warning' : 'positive' as const, // TODO: change to actual usage
    },
  ]

  const quickActions = [
    {
      title: 'Upgrade Plan',
      description: 'Get more API calls and features',
      icon: CreditCard,
      href: '/dashboard/subscription',
      color: 'bg-purple-500',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">
          Welcome back, {user?.name ?? user?.email}. Here&apos;s what&apos;s happening with your account.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <stat.icon className="size-4 text-gray-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className={`text-xs ${
                stat.changeType === 'positive'
                  ? 'text-green-600'
                  : stat.changeType === 'warning'
                  ? 'text-yellow-600'
                  : 'text-red-600'
              }`}>
                {stat.change} from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => (
            <Card key={action.title} className="cursor-pointer hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${action.color}`}>
                    <action.icon className="size-5 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-base">{action.title}</CardTitle>
                  </div>
                </div>
                <CardDescription>{action.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" size="sm" asChild>
                  <a href={action.href}>Get Started</a>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Your latest memories and API calls</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-2">
              <div className="flex items-center space-x-3">
                <Building2 className="size-4 text-gray-400" />
                <div>
                  <p className="text-sm font-medium">Memory: Pizza with cheese and ham</p>
                  <p className="text-xs text-gray-500">User likes pizza with cheese and ham on thin crust</p>
                </div>
              </div>
              <p className="text-xs text-gray-500">2 hours ago</p>
            </div>
            <div className="flex items-center justify-between py-2">
              <div className="flex items-center space-x-3">
                <Building2 className="size-4 text-gray-400" />
                <div>
                  <p className="text-sm font-medium">Memory: Typescript is a programming language</p>
                  <p className="text-xs text-gray-500">User likes typescript and uses it for web development</p>
                </div>
              </div>
              <p className="text-xs text-gray-500">1 day ago</p>
            </div>
            <div className="flex items-center justify-between py-2">
              <div className="flex items-center space-x-3">
                <Activity className="size-4 text-gray-400" />
                <div>
                  <p className="text-sm font-medium">API Call: Get available memory for Ai</p>
                  <p className="text-xs text-gray-500">Called by GET request from ChatGPT</p>
                </div>
              </div>
              <p className="text-xs text-gray-500">2 days ago</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
