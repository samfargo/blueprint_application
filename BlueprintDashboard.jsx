import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

const ProductAnalysisDashboard = () => {
  // Sample data modeling Blueprint's product performance
  const productPerformance = [
    { month: 'Jan', revenue: 120000, subscriptions: 850, newCustomers: 320 },
    { month: 'Feb', revenue: 145000, subscriptions: 920, newCustomers: 290 },
    { month: 'Mar', revenue: 168000, subscriptions: 1050, newCustomers: 380 },
    { month: 'Apr', revenue: 182000, subscriptions: 1150, newCustomers: 340 },
    { month: 'May', revenue: 195000, subscriptions: 1280, newCustomers: 420 },
    { month: 'Jun', revenue: 215000, subscriptions: 1400, newCustomers: 450 }
  ];

  const productCategories = [
    { name: 'Essential Supplements', value: 45, stockLevel: 85 },
    { name: 'Performance Boosters', value: 25, stockLevel: 72 },
    { name: 'Sleep Optimization', value: 15, stockLevel: 90 },
    { name: 'Cognitive Enhancement', value: 10, stockLevel: 65 },
    { name: 'Other Products', value: 5, stockLevel: 95 }
  ];

  const customerSegments = [
    { segment: 'Protocol Adherent', percentage: 65, retention: 92 },
    { segment: 'Supplement Only', percentage: 20, retention: 78 },
    { segment: 'New Users', percentage: 15, retention: 45 }
  ];

  const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#6366f1', '#84cc16'];

  return (
    <div className="w-full max-w-6xl mx-auto p-4 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Blueprint Product & Customer Analytics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Revenue and Subscription Trends */}
            <div className="h-96">
              <h3 className="text-lg font-semibold mb-4">Revenue & Subscription Growth</h3>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={productPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis yAxisId="left" orientation="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="revenue" stroke="#2563eb" name="Revenue ($)" />
                  <Line yAxisId="right" type="monotone" dataKey="subscriptions" stroke="#10b981" name="Active Subscriptions" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Product Category Distribution */}
            <div className="h-96">
              <h3 className="text-lg font-semibold mb-4">Product Category Distribution</h3>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={productCategories}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={120}
                    fill="#8884d8"
                    dataKey="value"
                    label={({name, value}) => `${name} (${value}%)`}
                  >
                    {productCategories.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Customer Segments Analysis */}
            <div className="h-96">
              <h3 className="text-lg font-semibold mb-4">Customer Segment Performance</h3>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={customerSegments}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="segment" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="percentage" fill="#2563eb" name="Segment Size (%)" />
                  <Bar dataKey="retention" fill="#10b981" name="Retention Rate (%)" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Inventory Health */}
            <div className="h-96">
              <h3 className="text-lg font-semibold mb-4">Inventory Health by Category</h3>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={productCategories}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="stockLevel" fill="#f59e0b" name="Stock Level (%)" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProductAnalysisDashboard;
