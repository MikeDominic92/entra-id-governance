'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { User, Shield, AlertTriangle } from 'lucide-react';

const roles = [
    { name: 'Global Admin', active: 2, eligible: 5, risk: 'Critical' },
    { name: 'Exchange Admin', active: 1, eligible: 8, risk: 'High' },
    { name: 'User Admin', active: 4, eligible: 12, risk: 'Medium' },
    { name: 'Security Reader', active: 10, eligible: 20, risk: 'Low' },
];

export function RoleMatrix() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Privileged Role Matrix</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {roles.map((role) => (
                        <div key={role.name} className="flex items-center justify-between p-4 bg-void-obsidian/50 border border-white/5 rounded-lg hover:border-azure/30 transition-all group">
                            <div className="flex items-center space-x-4">
                                <div className={`p-2 rounded-lg ${role.risk === 'Critical' ? 'bg-danger/10 text-danger' : role.risk === 'High' ? 'bg-warning/10 text-warning' : 'bg-azure/10 text-azure'}`}>
                                    <Shield size={20} />
                                </div>
                                <div>
                                    <div className="font-bold text-white group-hover:text-azure transition-colors">{role.name}</div>
                                    <div className="flex items-center space-x-2 mt-1">
                                        <Badge variant="outline" className="text-[10px] border-white/10">
                                            {role.active} Active
                                        </Badge>
                                        <Badge variant="secondary" className="text-[10px]">
                                            {role.eligible} Eligible
                                        </Badge>
                                    </div>
                                </div>
                            </div>

                            {role.risk === 'Critical' && (
                                <div className="animate-pulse">
                                    <AlertTriangle className="text-danger w-5 h-5" />
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
