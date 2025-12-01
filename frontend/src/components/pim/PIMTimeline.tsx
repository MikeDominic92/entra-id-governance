'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ResponsiveContainer, AreaChart, Area, XAxis, Tooltip } from 'recharts';

const data = [
    { time: '08:00', activations: 2 },
    { time: '10:00', activations: 8 },
    { time: '12:00', activations: 5 },
    { time: '14:00', activations: 12 },
    { time: '16:00', activations: 6 },
    { time: '18:00', activations: 3 },
];

export function PIMTimeline() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Role Activation Timeline (24h)</CardTitle>
            </CardHeader>
            <CardContent className="h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorActivations" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#A855F7" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#A855F7" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="time" stroke="#71717A" fontSize={12} tickLine={false} axisLine={false} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#18181B', borderColor: '#3F3F46', color: '#FAFAFA' }}
                            itemStyle={{ color: '#A855F7' }}
                        />
                        <Area
                            type="monotone"
                            dataKey="activations"
                            stroke="#A855F7"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorActivations)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
