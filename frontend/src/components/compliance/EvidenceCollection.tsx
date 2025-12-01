'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { FileText, Download, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';

const evidence = [
    { name: 'Access_Policy_Export_Q4.pdf', size: '2.4 MB', date: 'Oct 24, 2024', status: 'Ready' },
    { name: 'PIM_Activation_Logs.csv', size: '14.2 MB', date: 'Oct 23, 2024', status: 'Ready' },
    { name: 'MFA_Registration_Report.xlsx', size: '1.1 MB', date: 'Oct 22, 2024', status: 'Ready' },
    { name: 'Sign_In_Risk_Analysis.pdf', size: '5.8 MB', date: 'Oct 20, 2024', status: 'Ready' },
];

export function EvidenceCollection() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Evidence Locker</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-3">
                    {evidence.map((file) => (
                        <div key={file.name} className="flex items-center justify-between p-3 bg-void-obsidian/50 border border-white/5 rounded-lg hover:border-azure/30 transition-colors group">
                            <div className="flex items-center space-x-3">
                                <div className="p-2 rounded bg-void-black border border-white/10 text-text-secondary group-hover:text-white transition-colors">
                                    <FileText size={20} />
                                </div>
                                <div>
                                    <div className="text-sm font-medium text-white group-hover:text-azure transition-colors">{file.name}</div>
                                    <div className="text-xs text-text-muted">{file.size} • {file.date}</div>
                                </div>
                            </div>
                            <Button size="sm" variant="ghost" className="text-text-secondary hover:text-azure">
                                <Download size={16} />
                            </Button>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
