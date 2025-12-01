'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, Cell } from 'recharts';

const data = [
    { x: 1, y: 1, z: 100, status: 'Protected' },
    { x: 1, y: 2, z: 100, status: 'Protected' },
    { x: 1, y: 3, z: 100, status: 'Protected' },
    { x: 2, y: 1, z: 100, status: 'Protected' },
    { x: 2, y: 2, z: 100, status: 'Gap' },
    { x: 2, y: 3, z: 100, status: 'Protected' },
    { x: 3, y: 1, z: 100, status: 'Gap' },
    { x: 3, y: 2, z: 100, status: 'Protected' },
    { x: 3, y: 3, z: 100, status: 'Protected' },
];

const COLORS = {
    'Protected': '#14B8A6', // Teal
    'Gap': '#EF4444',       // Red
};

export function CoverageHeatmap() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Policy Coverage Map</CardTitle>
            </CardHeader>
            <CardContent className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                        <XAxis type="number" dataKey="x" name="User Group" tickFormatter={(val) => ['Admins', 'Employees', 'Guests'][val - 1]} />
                        <YAxis type="number" dataKey="y" name="App" tickFormatter={(val) => ['Azure Portal', 'Office 365', 'SaaS Apps'][val - 1]} />
                        <ZAxis type="number" dataKey="z" range={[400, 400]} />
                        <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#18181B', borderColor: '#3F3F46', color: '#FAFAFA' }} />
                        <Scatter name="Coverage" data={data} shape="square">
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[entry.status as keyof typeof COLORS]} />
                            ))}
                        </Scatter>
                    </ScatterChart>
                </ResponsiveContainer>
                <div className="flex justify-center space-x-6 mt-2 text-xs">
                    <div className="flex items-center"><span className="w-3 h-3 bg-teal mr-2 rounded-sm"></span> Protected</div>
                    <div className="flex items-center"><span className="w-3 h-3 bg-danger mr-2 rounded-sm"></span> Coverage Gap</div>
                </div>
            </CardContent>
        </Card>
    );
}
