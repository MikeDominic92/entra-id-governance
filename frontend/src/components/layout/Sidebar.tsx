'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
    LayoutDashboard,
    ShieldAlert,
    Users,
    FileText,
    PieChart,
    Settings,
    LogOut,
    Activity
} from 'lucide-react';

const navItems = [
    { name: 'Command Center', href: '/', icon: LayoutDashboard },
    { name: 'Conditional Access', href: '/conditional-access', icon: ShieldAlert },
    { name: 'PIM', href: '/pim', icon: Users },
    { name: 'Access Reviews', href: '/access-reviews', icon: FileText },
    { name: 'Compliance', href: '/compliance', icon: PieChart },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="w-64 h-screen bg-void-obsidian border-r border-white/5 flex flex-col fixed left-0 top-0 z-50">
            <div className="p-6 flex items-center space-x-3 border-b border-white/5">
                <div className="w-8 h-8 rounded-lg bg-azure/20 flex items-center justify-center border border-azure/30 shadow-[0_0_10px_rgba(14,165,233,0.2)]">
                    <Activity className="w-5 h-5 text-azure" />
                </div>
                <span className="font-bold text-lg tracking-tight text-text-primary">Entra<span className="text-azure">Gov</span></span>
            </div>

            <nav className="flex-1 p-4 space-y-1">
                <div className="px-2 mb-2 text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Operations
                </div>
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group",
                                isActive
                                    ? "bg-azure/10 text-azure border border-azure/20 shadow-[0_0_10px_rgba(14,165,233,0.1)]"
                                    : "text-text-secondary hover:bg-white/5 hover:text-text-primary"
                            )}
                        >
                            <item.icon className={cn(
                                "w-5 h-5 mr-3 transition-colors",
                                isActive ? "text-azure" : "text-text-muted group-hover:text-text-primary"
                            )} />
                            {item.name}
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-white/5">
                <button className="flex items-center w-full px-3 py-2.5 rounded-lg text-sm font-medium text-text-secondary hover:bg-white/5 hover:text-text-primary transition-colors">
                    <Settings className="w-5 h-5 mr-3 text-text-muted" />
                    Settings
                </button>
                <button className="flex items-center w-full px-3 py-2.5 rounded-lg text-sm font-medium text-text-secondary hover:bg-danger/10 hover:text-danger transition-colors mt-1">
                    <LogOut className="w-5 h-5 mr-3 text-text-muted group-hover:text-danger" />
                    Sign Out
                </button>
            </div>
        </div>
    );
}
