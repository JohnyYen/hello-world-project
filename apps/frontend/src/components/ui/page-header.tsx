import * as React from 'react';
import { cn } from '@/lib/utils';

const PageHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col gap-1 border-b pb-4 pt-6 px-6', className)}
    {...props}
  />
));
PageHeader.displayName = 'PageHeader';

const PageHeaderTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h1
    ref={ref}
    className={cn('text-2xl font-semibold tracking-tight', className)}
    {...props}
  />
));
PageHeaderTitle.displayName = 'PageHeaderTitle';

const PageHeaderDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn('text-muted-foreground', className)}
    {...props}
  />
));
PageHeaderDescription.displayName = 'PageHeaderDescription';

export { PageHeader, PageHeaderTitle, PageHeaderDescription };
