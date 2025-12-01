'use client';

import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface CommandLayoutProps {
    children: React.ReactNode;
}

export function CommandLayout({ children }: CommandLayoutProps) {
    return (
        <div className="min-h-screen bg-void-black text-text-primary font-sans selection:bg-azure/30">
            <Sidebar />
            <Header />
            <main className="pl-64 pt-16 min-h-screen">
                <div className="p-6 max-w-7xl mx-auto animate-in fade-in duration-500">
                    {children}
                </div>
            </main>

            {/* Scanning line effect */}
            <div className="fixed top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-azure/50 to-transparent opacity-20 animate-scan pointer-events-none z-50"></div>
        </div>
    );
}
