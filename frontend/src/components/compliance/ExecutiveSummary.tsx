'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { ShieldCheck, FileCheck, AlertOctagon, Calendar } from 'lucide-react';

const metrics = [
    { label: 'Overall Compliance', value: '92%', change: '+2%', icon: ShieldCheck, color: 'text-teal' },
    { label: 'Controls Passed', value: '145/158', change: '+5', icon: FileCheck, color: 'text-azure' },
    { label: 'Critical Issues', value: '0', change: '-2', icon: AlertOctagon, color: 'text-danger' },
    { label: 'Next Audit', value: '14 Days', change: '', icon: Calendar, color: 'text-cyber-purple' },
];

export function ExecutiveSummary() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 h-full">
            {metrics.map((metric) => (
                <Card key={metric.label} className="flex flex-col justify-between p-6 hover:bg-white/5 transition-colors">
                    <div className="flex justify-between items-start">
                        <div className={`p-2 rounded-lg bg-void-obsidian border border-white/10 ${metric.color}`}>
                            <metric.icon size={24} />
                        </div>
                        {metric.change && (
                            <span className={`text-xs font-bold ${metric.change.startsWith('+') ? 'text-teal' : 'text-danger'}`}>
                                {metric.change}
                            </span>
                        )}
                    </div>
                    <div className="mt-4">
                        <div className="text-3xl font-bold text-white tracking-tight">{metric.value}</div>
                        <div className="text-sm text-text-secondary mt-1">{metric.label}</div>
                    </div>
                </Card>
            ))}
        </div>
    );
}
