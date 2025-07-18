import { ThemeToggle } from '@/components/ui/theme-toggle';
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

export default function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="relative min-h-screen bg-background overflow-hidden">
      <div className={cn(
        'absolute inset-0 bg-[conic-gradient(from_0deg,_var(--tw-conic-gradient-stops))]',
        '[--tw-conic-gradient-stops:theme(colors.blue.300),theme(colors.violet.300),theme(colors.green.300),theme(colors.blue.300)]',
        'dark:[--tw-conic-gradient-stops:theme(colors.blue.950),theme(colors.violet.950),theme(colors.green.950),theme(colors.blue.950)]',
      )}></div>

      <div className="absolute rounded-full bg-white opacity-30 dark:opacity-5 filter blur-xl bg-blend-overlay aspect-square top-4 left-4 w-128"></div>
      <div className="absolute rounded-full bg-white opacity-50 dark:opacity-10 filter blur-md bg-blend-overlay aspect-square top-1/4 left-1/4 w-64"></div>
      <div className="absolute rounded-full bg-white opacity-50 dark:opacity-10 filter blur-md bg-blend-overlay aspect-square bottom-1/4 right-1/4 w-56"></div>

      <div className="absolute rounded-full bg-white opacity-40 dark:opacity-5 filter blur-sm bg-blend-overlay aspect-square top-1/8 left-1/2 w-32"></div>

      <div className="absolute top-1 right-1 flex gap-4 p-2">
        <ThemeToggle />
      </div>
      {children}
    </div>
  );
}
