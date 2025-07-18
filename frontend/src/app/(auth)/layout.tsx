import { ThemeToggle } from '@/components/ui/theme-toggle';
import { ReactNode } from 'react';

export default function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="relative min-h-screen bg-background bg-gradient-to-b from-brand-50/80 to-brand-200/80 dark:from-brand-800/10 dark:to-brand-950/10">
      <div className="absolute top-0 left-0 w-1/3 aspect-square rounded-full bg-white opacity-50 blur-md pointer-events-none z-0 mix-blend-overlay" />
      <div className="absolute bottom-0 right-0 w-1/6 aspect-square rounded-full bg-white opacity-50 blur-lg pointer-events-none z-0 mix-blend-overlay" />
      <div className="absolute top-1 right-1 flex gap-4 p-2">
        <ThemeToggle />
      </div>
      {children}
    </div>
  );
}
