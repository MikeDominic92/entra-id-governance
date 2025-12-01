'use client';

import React from 'react';
import { CommandLayout } from '@/components/layout/CommandLayout';
import { PolicyCards } from '@/components/conditional-access/PolicyCards';
import { CoverageHeatmap } from '@/components/conditional-access/CoverageHeatmap';
import { PolicySimulator } from '@/components/conditional-access/PolicySimulator';
import { Button } from '@/components/ui/Button';
import { Plus, Sliders } from 'lucide-react';

export default function ConditionalAccess() {
    return (
        <CommandLayout>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-white text-glow">Conditional Access Analyzer</h1>
                    <p className="text-text-secondary">Visualize coverage gaps and simulate policy impacts</p>
                </div>
                <div className="flex space-x-3">
                    <Button variant="outline">
                        <Sliders className="w-4 h-4 mr-2" />
                        Templates
                    </Button>
                    <Button>
                        <Plus className="w-4 h-4 mr-2" />
                        New Policy
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-180px)]">
                {/* Left Column: Policies */}
                <div className="lg:col-span-4 h-full overflow-y-auto pr-2">
                    <h3 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-4">Active Policies</h3>
                    <PolicyCards />
                </div>

                {/* Right Column: Analysis */}
                <div className="lg:col-span-8 h-full flex flex-col gap-6">
                    <div className="flex-1">
                        <CoverageHeatmap />
                    </div>
                    <div className="h-[350px]">
                        <PolicySimulator />
                    </div>
                </div>
            </div>
        </CommandLayout>
    );
}
