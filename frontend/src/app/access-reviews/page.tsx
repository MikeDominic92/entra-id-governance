'use client';

import React from 'react';
import { CommandLayout } from '@/components/layout/CommandLayout';
import { CampaignCards } from '@/components/access-reviews/CampaignCards';
import { ReviewerWorkload } from '@/components/access-reviews/ReviewerWorkload';
import { ReviewTrends } from '@/components/access-reviews/ReviewTrends';
import { Button } from '@/components/ui/Button';
import { Plus, Download } from 'lucide-react';

export default function AccessReviews() {
    return (
        <CommandLayout>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-white text-glow">Access Reviews</h1>
                    <p className="text-text-secondary">Monitor and manage recertification campaigns</p>
                </div>
                <div className="flex space-x-3">
                    <Button variant="outline">
                        <Download className="w-4 h-4 mr-2" />
                        Export Report
                    </Button>
                    <Button variant="default">
                        <Plus className="w-4 h-4 mr-2" />
                        New Campaign
                    </Button>
                </div>
            </div>

            <div className="h-[180px] mb-6">
                <CampaignCards />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[350px]">
                <ReviewerWorkload />
                <ReviewTrends />
            </div>
        </CommandLayout>
    );
}
