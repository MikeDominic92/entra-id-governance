'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';

const data = [
    { name: 'Engineering', reviews: 120 },
    { name: 'Sales', reviews: 80 },
    { name: 'Marketing', reviews: 45 },
    { name: 'HR', reviews: 30 },
    { name: 'IT', reviews: 150 },
];

export function ReviewerWorkload() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Pending Reviews by Department</CardTitle>
            </CardHeader>
            <CardContent className="h-[250px]">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                        <XAxis type="number" hide />
                        <YAxis type="category" dataKey="name" stroke="#71717A" fontSize={12} tickLine={false} axisLine={false} width={80} />
                        <Tooltip
                            cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                            contentStyle={{ backgroundColor: '#18181B', borderColor: '#3F3F46', color: '#FAFAFA' }}
                        />
                        <Bar dataKey="reviews" radius={[0, 4, 4, 0]}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={`rgba(14, 165, 233, ${0.4 + (index * 0.1)})`} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
