'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { ArrowRight } from 'lucide-react';

const campaigns = [
    { id: 1, name: 'Q4 All Employees', progress: 75, due: '2 days' },
    { id: 2, name: 'Guest Access Review', progress: 30, due: '5 days' },
    { id: 3, name: 'Admin Role Audit', progress: 90, due: 'Tomorrow' },
];

const COLORS = ['#14B8A6', '#27272A'];

export function CampaignCards() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 h-full">
            {campaigns.map((camp) => (
                <Card key={camp.id} className="relative overflow-hidden group hover:border-teal/50 transition-colors cursor-pointer">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-base truncate">{camp.name}</CardTitle>
                        <p className="text-xs text-text-secondary">Due: {camp.due}</p>
                    </CardHeader>
                    <CardContent className="flex items-center justify-between">
                        <div className="h-[80px] w-[80px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={[{ value: camp.progress }, { value: 100 - camp.progress }]}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={25}
                                        outerRadius={35}
                                        startAngle={90}
                                        endAngle={-270}
                                        dataKey="value"
                                        stroke="none"
                                    >
                                        <Cell fill={COLORS[0]} />
                                        <Cell fill={COLORS[1]} />
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="text-right">
                            <div className="text-2xl font-bold text-white">{camp.progress}%</div>
                            <div className="text-xs text-text-muted">Completed</div>
                        </div>

                        <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                            <ArrowRight className="text-teal w-5 h-5" />
                        </div>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
