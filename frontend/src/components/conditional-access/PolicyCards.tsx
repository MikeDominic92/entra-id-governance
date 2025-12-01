'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Shield, Smartphone, Globe, Users } from 'lucide-react';

const policies = [
    { id: 1, name: 'Require MFA for Admins', state: 'On', users: 'All Admins', apps: 'All Cloud Apps', risk: 'High' },
    { id: 2, name: 'Block Legacy Auth', state: 'On', users: 'All Users', apps: 'All Cloud Apps', risk: 'Medium' },
    { id: 3, name: 'Require Compliant Device', state: 'Report-Only', users: 'Finance', apps: 'SharePoint', risk: 'Low' },
    { id: 4, name: 'Block Risky Sign-ins', state: 'On', users: 'All Users', apps: 'All Cloud Apps', risk: 'High' },
];

export function PolicyCards() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {policies.map((policy) => (
                <Card key={policy.id} variant="glass" className="group hover:border-azure/50 cursor-pointer">
                    <CardHeader className="pb-2">
                        <div className="flex justify-between items-start">
                            <div className="flex items-center space-x-3">
                                <div className="p-2 rounded-lg bg-azure/10 text-azure group-hover:text-white group-hover:bg-azure transition-colors">
                                    <Shield size={18} />
                                </div>
                                <div>
                                    <CardTitle className="text-base group-hover:text-azure transition-colors">{policy.name}</CardTitle>
                                    <div className="flex items-center space-x-2 mt-1">
                                        <Badge variant={policy.state === 'On' ? 'success' : 'warning'} className="text-[10px] px-1.5 py-0">
                                            {policy.state}
                                        </Badge>
                                        <span className="text-xs text-text-muted">ID: CA-{100 + policy.id}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-2 gap-2 text-xs text-text-secondary mt-2">
                            <div className="flex items-center space-x-2">
                                <Users size={12} />
                                <span>{policy.users}</span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <Globe size={12} />
                                <span>{policy.apps}</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
