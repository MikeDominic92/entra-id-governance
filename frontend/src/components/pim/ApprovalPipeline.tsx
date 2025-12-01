'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Check, X, Clock, User } from 'lucide-react';
import { Button } from '@/components/ui/Button';

const requests = [
    { id: 1, user: 'Alice Smith', role: 'Global Admin', reason: 'Emergency fix for Exchange', time: '5m ago', status: 'pending' },
    { id: 2, user: 'Bob Jones', role: 'SharePoint Admin', reason: 'Site configuration', time: '1h ago', status: 'approved' },
];

export function ApprovalPipeline() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Approval Pipeline</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {requests.map((req) => (
                        <div key={req.id} className="p-4 rounded-lg bg-void-obsidian/30 border border-white/5 relative overflow-hidden">
                            {req.status === 'pending' && (
                                <div className="absolute top-0 left-0 w-1 h-full bg-warning shadow-[0_0_10px_rgba(245,158,11,0.5)]"></div>
                            )}
                            {req.status === 'approved' && (
                                <div className="absolute top-0 left-0 w-1 h-full bg-teal shadow-[0_0_10px_rgba(20,184,166,0.5)]"></div>
                            )}

                            <div className="flex justify-between items-start pl-3">
                                <div>
                                    <div className="flex items-center space-x-2">
                                        <User size={14} className="text-text-secondary" />
                                        <span className="font-bold text-white">{req.user}</span>
                                        <span className="text-text-muted text-xs">• {req.time}</span>
                                    </div>
                                    <div className="text-sm text-cyber-purple font-medium mt-1">{req.role}</div>
                                    <div className="text-xs text-text-secondary mt-1 italic">"{req.reason}"</div>
                                </div>

                                {req.status === 'pending' ? (
                                    <div className="flex space-x-2">
                                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 text-danger hover:text-danger hover:bg-danger/10">
                                            <X size={16} />
                                        </Button>
                                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 text-teal hover:text-teal hover:bg-teal/10">
                                            <Check size={16} />
                                        </Button>
                                    </div>
                                ) : (
                                    <div className="flex items-center text-teal text-xs font-bold uppercase tracking-wider">
                                        <Check size={14} className="mr-1" /> Approved
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
