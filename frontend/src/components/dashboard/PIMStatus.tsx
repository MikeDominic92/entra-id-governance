'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { UserCheck, Clock } from 'lucide-react';

export function PIMStatus() {
    return (
        <Card className="h-full">
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>PIM Status</CardTitle>
                <Badge variant="cyber">Live</Badge>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-void-obsidian/50 rounded-lg border border-white/5 hover:border-cyber-purple/30 transition-colors">
                    <div className="flex items-center space-x-3">
                        <div className="p-2 rounded-md bg-cyber-purple/10 text-cyber-purple">
                            <UserCheck size={18} />
                        </div>
                        <div>
                            <div className="text-sm font-medium text-white">Active Global Admins</div>
                            <div className="text-xs text-text-muted">Currently elevated</div>
                        </div>
                    </div>
                    <div className="text-xl font-bold text-cyber-purple text-glow">2</div>
                </div>

                <div className="flex items-center justify-between p-3 bg-void-obsidian/50 rounded-lg border border-white/5 hover:border-azure/30 transition-colors">
                    <div className="flex items-center space-x-3">
                        <div className="p-2 rounded-md bg-azure/10 text-azure">
                            <Clock size={18} />
                        </div>
                        <div>
                            <div className="text-sm font-medium text-white">Pending Requests</div>
                            <div className="text-xs text-text-muted">Awaiting approval</div>
                        </div>
                    </div>
                    <div className="text-xl font-bold text-azure">5</div>
                </div>
            </CardContent>
        </Card>
    );
}
