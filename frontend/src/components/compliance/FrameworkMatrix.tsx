'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Check, Minus, AlertTriangle } from 'lucide-react';

const frameworks = [
    { name: 'ISO 27001', status: 'Compliant', controls: { access: true, logging: true, encryption: true, incident: true } },
    { name: 'SOC 2 Type II', status: 'In Progress', controls: { access: true, logging: true, encryption: false, incident: true } },
    { name: 'NIST CSF', status: 'Compliant', controls: { access: true, logging: true, encryption: true, incident: true } },
    { name: 'GDPR', status: 'Review Needed', controls: { access: false, logging: true, encryption: true, incident: false } },
];

export function FrameworkMatrix() {
    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle>Framework Alignment</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="text-xs text-text-secondary uppercase bg-void-obsidian/50 border-b border-white/5">
                            <tr>
                                <th className="px-6 py-3">Framework</th>
                                <th className="px-6 py-3 text-center">Access Control</th>
                                <th className="px-6 py-3 text-center">Logging</th>
                                <th className="px-6 py-3 text-center">Encryption</th>
                                <th className="px-6 py-3 text-center">Incident Resp.</th>
                            </tr>
                        </thead>
                        <tbody>
                            {frameworks.map((fw) => (
                                <tr key={fw.name} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                    <td className="px-6 py-4 font-medium text-white">
                                        {fw.name}
                                        <div className={`text-[10px] mt-1 ${fw.status === 'Compliant' ? 'text-teal' : fw.status === 'In Progress' ? 'text-azure' : 'text-warning'}`}>
                                            {fw.status}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-center">
                                        <div className="flex justify-center">
                                            {fw.controls.access ? <Check className="text-teal w-5 h-5 shadow-[0_0_5px_rgba(20,184,166,0.5)]" /> : <AlertTriangle className="text-warning w-5 h-5" />}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-center">
                                        <div className="flex justify-center">
                                            {fw.controls.logging ? <Check className="text-teal w-5 h-5 shadow-[0_0_5px_rgba(20,184,166,0.5)]" /> : <AlertTriangle className="text-warning w-5 h-5" />}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-center">
                                        <div className="flex justify-center">
                                            {fw.controls.encryption ? <Check className="text-teal w-5 h-5 shadow-[0_0_5px_rgba(20,184,166,0.5)]" /> : <Minus className="text-text-muted w-5 h-5" />}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-center">
                                        <div className="flex justify-center">
                                            {fw.controls.incident ? <Check className="text-teal w-5 h-5 shadow-[0_0_5px_rgba(20,184,166,0.5)]" /> : <AlertTriangle className="text-warning w-5 h-5" />}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </CardContent>
        </Card>
    );
}
