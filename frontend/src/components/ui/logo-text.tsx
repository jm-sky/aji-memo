import { cn } from '@/lib/utils';

interface LogoTextProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  foreground?: string;
}

export function LogoText({ className, size = 'md', foreground = 'text-foreground' }: LogoTextProps) {
  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl'
  };

  return (
    <span className={cn('font-bold', sizeClasses[size], className)}>
      <span className={foreground}>Aji</span>
      <span className="bg-gradient-to-r from-brand-400 via-violet-400 to-brand-400 bg-clip-text text-transparent">Memo</span>
    </span>
  );
}
