import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
    "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
    {
        variants: {
            variant: {
                default:
                    "border-transparent bg-azure/10 text-azure border-azure/20 shadow-[0_0_10px_rgba(14,165,233,0.1)]",
                secondary:
                    "border-transparent bg-void-obsidian text-text-secondary border-white/10",
                destructive:
                    "border-transparent bg-danger/10 text-danger border-danger/20 shadow-[0_0_10px_rgba(239,68,68,0.1)]",
                outline: "text-text-primary",
                success: "border-transparent bg-teal/10 text-teal border-teal/20 shadow-[0_0_10px_rgba(20,184,166,0.1)]",
                warning: "border-transparent bg-warning/10 text-warning border-warning/20 shadow-[0_0_10px_rgba(245,158,11,0.1)]",
                cyber: "border-transparent bg-cyber-purple/10 text-cyber-purple border-cyber-purple/20 shadow-[0_0_10px_rgba(168,85,247,0.1)]",
            },
        },
        defaultVariants: {
            variant: "default",
        },
    }
)

export interface BadgeProps
    extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> { }

function Badge({ className, variant, ...props }: BadgeProps) {
    return (
        <div className={cn(badgeVariants({ variant }), className)} {...props} />
    )
}

export { Badge, badgeVariants }
