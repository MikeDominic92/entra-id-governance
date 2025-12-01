'use client';

import React from 'react';
import { Search, Bell, HelpCircle, User } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';

export function Header() {
    return (
        <header className="h-16 border-b border-white/5 bg-void-black/80 backdrop-blur-md flex items-center justify-between px-6 fixed top-0 right-0 left-64 z-40">
            <div className="flex items-center flex-1 max-w-xl">
                <div className="relative w-full">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                    <input
                        type="text"
                        placeholder="Search users, groups, or policies..."
                        className="w-full bg-void-obsidian/50 border border-white/5 rounded-full py-1.5 pl-10 pr-4 text-sm text-text-primary focus:outline-none focus:border-azure/30 focus:ring-1 focus:ring-azure/30 transition-all placeholder:text-text-muted"
                    />
                </div>
            </div>

            <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-void-obsidian border border-white/5">
                    <span className="w-2 h-2 rounded-full bg-teal shadow-[0_0_5px_#14B8A6]"></span>
                    <span className="text-xs font-mono text-text-secondary">SYSTEM_ONLINE</span>
                </div>

                <button className="relative p-2 rounded-full hover:bg-white/5 text-text-secondary hover:text-text-primary transition-colors">
                    <Bell className="w-5 h-5" />
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-danger shadow-[0_0_5px_#EF4444]"></span>
                </button>

                <button className="p-2 rounded-full hover:bg-white/5 text-text-secondary hover:text-text-primary transition-colors">
                    <HelpCircle className="w-5 h-5" />
                </button>

                <div className="h-8 w-px bg-white/10 mx-2"></div>

                <button className="flex items-center space-x-3 pl-2 pr-1 py-1 rounded-full hover:bg-white/5 transition-colors border border-transparent hover:border-white/5">
                    <div className="text-right hidden md:block">
                        <p className="text-sm font-medium text-text-primary leading-none">Admin User</p>
                        <p className="text-xs text-text-muted mt-0.5">Global Administrator</p>
                    </div>
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-azure to-cyber-purple flex items-center justify-center text-white shadow-lg">
                        <User className="w-4 h-4" />
                    </div>
                </button>
            </div>
        </header>
    );
}
