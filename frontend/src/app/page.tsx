'use client';

import React from 'react';
import { CommandLayout } from '@/components/layout/CommandLayout';
import { ComplianceScore } from '@/components/dashboard/ComplianceScore';
import { ConditionalAccessStats } from '@/components/dashboard/ConditionalAccessStats';
import { PIMStatus } from '@/components/dashboard/PIMStatus';
import { ActivityFeed } from '@/components/dashboard/ActivityFeed';
import { Button } from '@/components/ui/Button';
import { RefreshCw, Shield } from 'lucide-react';

export default function Dashboard() {
  return (
    <CommandLayout>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight text-glow">Governance Command Center</h1>
          <p className="text-text-secondary mt-1">Real-time identity security monitoring</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh Data
          </Button>
          <Button variant="default" size="sm">
            <Shield className="w-4 h-4 mr-2" />
            Run Quick Scan
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
        {/* Top Row */}
        <div className="lg:col-span-3 h-[280px]">
          <ComplianceScore />
        </div>
        <div className="lg:col-span-5 h-[280px]">
          <ConditionalAccessStats />
        </div>
        <div className="lg:col-span-4 h-[280px]">
          <PIMStatus />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[400px]">
        {/* Bottom Row */}
        <div className="lg:col-span-8 h-full">
          <ActivityFeed />
        </div>
        <div className="lg:col-span-4 h-full bg-void-obsidian/40 border border-white/5 rounded-xl p-6 backdrop-blur-sm">
          <h3 className="text-lg font-bold text-white mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Button variant="secondary" className="w-full justify-start">
              <span className="w-2 h-2 rounded-full bg-azure mr-3"></span>
              Review Access Packages
            </Button>
            <Button variant="secondary" className="w-full justify-start">
              <span className="w-2 h-2 rounded-full bg-cyber-purple mr-3"></span>
              Approve PIM Requests
            </Button>
            <Button variant="secondary" className="w-full justify-start">
              <span className="w-2 h-2 rounded-full bg-danger mr-3"></span>
              Investigate Risky Sign-ins
            </Button>
            <Button variant="secondary" className="w-full justify-start">
              <span className="w-2 h-2 rounded-full bg-teal mr-3"></span>
              Export Compliance Report
            </Button>
          </div>
        </div>
      </div>
    </CommandLayout>
  );
}
