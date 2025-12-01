'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const data = [
    { name: 'Compliant', value: 85 },
    { name: 'Non-Compliant', value: 15 },
];

const COLORS = ['#14B8A6', '#18181B'];

export function ComplianceScore() {
    return (
        <Card variant="neon" className="h-full">
            <CardHeader>
                <CardTitle className="text-teal">Compliance Score</CardTitle>
            </CardHeader>
            <CardContent className="h-[200px] relative flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={80}
                            startAngle={180}
                            endAngle={0}
                            paddingAngle={0}
                            dataKey="value"
                            stroke="none"
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                    </PieChart>
                </ResponsiveContainer>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center mt-4">
                    <div className="text-4xl font-bold text-white text-glow">85%</div>
                    <div className="text-xs text-teal uppercase tracking-widest mt-1">Secure</div>
                </div>
            </CardContent>
        </Card>
    );
}
