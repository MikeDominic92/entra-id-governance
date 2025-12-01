'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Terminal } from 'lucide-react';

const logs = [
    { time: '10:42:05', type: 'INFO', msg: 'Policy "Require MFA" updated by admin@contoso.com' },
    { time: '10:41:12', type: 'WARN', msg: 'Risky sign-in detected: user.test@contoso.com (IP: 192.168.1.5)' },
    { time: '10:38:55', type: 'SUCCESS', msg: 'Access Review "Q4 Engineers" completed' },
    { time: '10:35:20', type: 'INFO', msg: 'PIM Role "Exchange Admin" activated for 2 hours' },
    { time: '10:30:01', type: 'ERROR', msg: 'Sync failure: HR-Connector-01 timeout' },
];

export function ActivityFeed() {
    return (
        <Card className="h-full font-mono text-sm">
            <CardHeader className="border-b border-white/5 bg-void-obsidian/80">
                <div className="flex items-center space-x-2">
                    <Terminal size={16} className="text-text-secondary" />
                    <CardTitle className="text-sm text-text-secondary">LIVE_OPERATIONS_LOG</CardTitle>
                </div>
            </CardHeader>
            <CardContent className="p-0">
                <div className="h-[250px] overflow-y-auto p-4 space-y-2 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
                    {logs.map((log, i) => (
                        <div key={i} className="flex space-x-3 hover:bg-white/5 p-1 rounded transition-colors">
                            <span className="text-text-muted select-none">[{log.time}]</span>
                            <span className={`font-bold ${log.type === 'INFO' ? 'text-azure' :
                                    log.type === 'WARN' ? 'text-warning' :
                                        log.type === 'ERROR' ? 'text-danger' :
                                            'text-teal'
                                }`}>{log.type}</span>
                            <span className="text-text-primary truncate">{log.msg}</span>
                        </div>
                    ))}
                    <div className="flex space-x-2 animate-pulse">
                        <span className="text-azure">{'>'}</span>
                        <span className="w-2 h-4 bg-azure"></span>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
