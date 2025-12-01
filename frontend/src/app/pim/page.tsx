'use client';

import React from 'react';
import { CommandLayout } from '@/components/layout/CommandLayout';
import { RoleMatrix } from '@/components/pim/RoleMatrix';
import { PIMTimeline } from '@/components/pim/PIMTimeline';
import { ApprovalPipeline } from '@/components/pim/ApprovalPipeline';
import { Button } from '@/components/ui/Button';
import { UserPlus, Settings } from 'lucide-react';

export default function PIM() {
    return (
        <CommandLayout>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-white text-glow">Privileged Identity Management</h1>
                    <p className="text-text-secondary">Manage, control, and monitor access to important resources</p>
                </div>
                <div className="flex space-x-3">
                    <Button variant="outline">
                        <Settings className="w-4 h-4 mr-2" />
                        Settings
                    </Button>
                    <Button variant="cyber">
                        <UserPlus className="w-4 h-4 mr-2" />
                        Assign Eligibility
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
                <div className="lg:col-span-8 h-[300px]">
                    <PIMTimeline />
                </div>
                <div className="lg:col-span-4 h-[300px]">
                    <ApprovalPipeline />
                </div>
            </div>

            <div className="h-[400px]">
                <RoleMatrix />
            </div>
        </CommandLayout>
    );
}
