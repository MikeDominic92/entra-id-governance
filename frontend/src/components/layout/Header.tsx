'use client';

import React from 'react';
import { Search, Bell, HelpCircle } from 'lucide-react';
import { IdentityBadge } from '../ui/IdentityBadge';

export function Header() {
    return (
        <header className="h-20 glass-panel border-b-0 sticky top-0 z-40 px-6 flex items-center justify-between m-4 rounded-2xl ml-[17rem]">
            <div className="flex items-center flex-1 max-w-xl group">
                <div className="relative w-full">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cyber-cyan/50 group-focus-within:text-cyber-cyan transition-colors" />
                    <input
                        type="text"
                        placeholder="Search users, groups, or policies..."
                        className="w-full bg-black/20 border border-white/10 rounded-xl py-2 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-cyber-cyan/50 focus:ring-1 focus:ring-cyber-cyan/50 transition-all placeholder:text-gray-500 backdrop-blur-sm"
                    />
                </div>
            </div>

            <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-black/40 border border-cyber-green/30">
                    <span className="w-2 h-2 rounded-full bg-cyber-green shadow-[0_0_5px_#10b981] animate-pulse"></span>
                    <span className="text-xs font-mono text-cyber-green">SYSTEM_ONLINE</span>
                </div>

                <button className="relative p-2 rounded-full hover:bg-white/5 text-gray-400 hover:text-cyber-cyan transition-colors group">
                    <Bell className="w-5 h-5 group-hover:animate-pulse" />
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-cyber-purple shadow-[0_0_5px_#7c3aed]"></span>
                </button>

                <button className="p-2 rounded-full hover:bg-white/5 text-gray-400 hover:text-cyber-cyan transition-colors">
                    <HelpCircle className="w-5 h-5" />
                </button>

                <div className="h-8 w-px bg-white/10 mx-2"></div>

                <IdentityBadge />
            </div>
        </header>
    );
}

