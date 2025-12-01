'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ResponsiveContainer, LineChart, Line, XAxis, Tooltip } from 'recharts';

const data = [
    { day: 'Mon', approved: 40, denied: 10 },
    { day: 'Tue', approved: 55, denied: 15 },
    { day: 'Wed', approved: 30, denied: 5 },
    { day: 'Thu', approved: 70, denied: 20 },
    { day: 'Fri', approved: 45, denied: 12 },
];

export function ReviewTrends() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Review Decisions Trend</CardTitle>
            </CardHeader>
            <CardContent className="h-[250px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="day" stroke="#71717A" fontSize={12} tickLine={false} axisLine={false} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#18181B', borderColor: '#3F3F46', color: '#FAFAFA' }}
                        />
                        <Line type="monotone" dataKey="approved" stroke="#14B8A6" strokeWidth={2} dot={{ r: 4, fill: '#14B8A6' }} />
                        <Line type="monotone" dataKey="denied" stroke="#EF4444" strokeWidth={2} dot={{ r: 4, fill: '#EF4444' }} />
                    </LineChart>
                </ResponsiveContainer>
                <div className="flex justify-center space-x-6 mt-2 text-xs">
                    <div className="flex items-center"><span className="w-3 h-3 bg-teal mr-2 rounded-full"></span> Approved</div>
                    <div className="flex items-center"><span className="w-3 h-3 bg-danger mr-2 rounded-full"></span> Denied</div>
                </div>
            </CardContent>
        </Card>
    );
}
