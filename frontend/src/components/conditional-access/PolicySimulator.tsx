'use client';

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Play, RotateCcw } from 'lucide-react';

export function PolicySimulator() {
    const [output, setOutput] = useState<string[]>([
        '> Initializing policy engine...',
        '> Loading 24 active policies...',
        '> Ready for simulation.'
    ]);

    const runSimulation = () => {
        setOutput([
            '> Simulating sign-in event...',
            '> User: jane.doe@contoso.com',
            '> App: Salesforce',
            '> Location: London, UK (IP: 212.x.x.x)',
            '> Device: Unmanaged iOS',
            '----------------------------------------',
            '> Evaluating Policy: "Block Legacy Auth"... [MATCH] -> ALLOW',
            '> Evaluating Policy: "Require MFA"... [MATCH] -> REQUIRE MFA',
            '> Evaluating Policy: "Require Compliant Device"... [MATCH] -> BLOCK',
            '----------------------------------------',
            '> FINAL RESULT: BLOCK (Device non-compliant)',
        ]);
    };

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between border-b border-white/5 bg-void-obsidian/80">
                <CardTitle>Policy Simulator</CardTitle>
                <div className="flex space-x-2">
                    <Button size="sm" variant="ghost" onClick={() => setOutput(['> Ready.'])}>
                        <RotateCcw className="w-4 h-4" />
                    </Button>
                    <Button size="sm" onClick={runSimulation}>
                        <Play className="w-4 h-4 mr-2" />
                        Simulate
                    </Button>
                </div>
            </CardHeader>
            <CardContent className="flex-1 p-0 bg-black/50 font-mono text-sm">
                <div className="p-4 space-y-2 h-[300px] overflow-y-auto">
                    {output.map((line, i) => (
                        <div key={i} className={`${line.includes('BLOCK') ? 'text-danger' : line.includes('ALLOW') ? 'text-teal' : line.includes('REQUIRE') ? 'text-warning' : 'text-text-secondary'}`}>
                            {line}
                        </div>
                    ))}
                    <div className="animate-pulse text-azure">_</div>
                </div>
            </CardContent>
        </Card>
    );
}
