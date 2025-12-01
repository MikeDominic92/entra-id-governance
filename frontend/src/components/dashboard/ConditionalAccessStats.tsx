'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { ShieldCheck, ShieldAlert, Users, Globe } from 'lucide-react';

const stats = [
    { label: 'Active Policies', value: '24', icon: ShieldCheck, color: 'text-azure', glow: 'shadow-[0_0_10px_rgba(14,165,233,0.2)]' },
    { label: 'Coverage Gaps', value: '3', icon: ShieldAlert, color: 'text-danger', glow: 'shadow-[0_0_10px_rgba(239,68,68,0.2)]' },
    { label: 'Users Protected', value: '1,240', icon: Users, color: 'text-cyber-purple', glow: 'shadow-[0_0_10px_rgba(168,85,247,0.2)]' },
    { label: 'Sign-ins (24h)', value: '14.2k', icon: Globe, color: 'text-teal', glow: 'shadow-[0_0_10px_rgba(20,184,166,0.2)]' },
];

export function ConditionalAccessStats() {
    return (
        <div className="grid grid-cols-2 gap-4 h-full">
            {stats.map((stat) => (
                <Card key={stat.label} className="flex flex-col justify-center items-center p-4 hover:bg-white/5 transition-colors group">
                    <div className={`p-3 rounded-full bg-void-obsidian border border-white/10 mb-3 ${stat.glow} group-hover:scale-110 transition-transform duration-300`}>
                        <stat.icon className={`w-6 h-6 ${stat.color}`} />
                    </div>
                    <div className="text-2xl font-bold text-white tracking-tight">{stat.value}</div>
                    <div className="text-xs text-text-secondary uppercase tracking-wider mt-1">{stat.label}</div>
                </Card>
            ))}
        </div>
    );
}
