import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-foreground h-9 w-full min-w-0 rounded-md border-2 bg-transparent px-3 py-1 text-base transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm font-mono",
        "focus-visible:border-blue-600 focus-visible:ring-0 focus-visible:shadow-[0_0_0_3px_rgba(30,64,175,0.3),0_0_0_5px_rgba(59,130,246,0.2)]",
        "dark:focus-visible:border-blue-400 dark:focus-visible:shadow-[0_0_0_3px_rgba(59,130,246,0.3),0_0_0_5px_rgba(96,165,250,0.2)]",
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
        className
      )}
      {...props}
    />
  )
}

export { Input }
