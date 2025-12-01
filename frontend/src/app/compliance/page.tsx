'use client';

import React from 'react';
import { CommandLayout } from '@/components/layout/CommandLayout';
import { ExecutiveSummary } from '@/components/compliance/ExecutiveSummary';
import { FrameworkMatrix } from '@/components/compliance/FrameworkMatrix';
import { EvidenceCollection } from '@/components/compliance/EvidenceCollection';
import { Button } from '@/components/ui/Button';
import { FileText, Calendar } from 'lucide-react';

export default function Compliance() {
    return (
        <CommandLayout>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-white text-glow">Compliance Reporting</h1>
                    <p className="text-text-secondary">Audit readiness and framework alignment</p>
                </div>
                <div className="flex space-x-3">
                    <Button variant="outline">
                        <Calendar className="w-4 h-4 mr-2" />
                        Schedule Report
                    </Button>
                    <Button variant="cyber">
                        <FileText className="w-4 h-4 mr-2" />
                        Generate Audit Pack
                    </Button>
                </div>
            </div>

            <div className="h-[140px] mb-6">
                <ExecutiveSummary />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[400px]">
                <div className="lg:col-span-8 h-full">
                    <FrameworkMatrix />
                </div>
                <div className="lg:col-span-4 h-full">
                    <EvidenceCollection />
                </div>
            </div>
        </CommandLayout>
    );
}
