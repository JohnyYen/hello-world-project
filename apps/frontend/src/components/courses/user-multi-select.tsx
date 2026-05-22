"use client";

import { useState, useMemo } from "react";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import { Search, X } from "lucide-react";

interface UserOption {
  id: string;
  label: string;
  subtitle?: string;
}

interface UserMultiSelectProps {
  options: UserOption[];
  selected: string[];
  onChange: (ids: string[]) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  emptyMessage?: string;
  label?: string;
  filterFn?: (option: UserOption) => boolean;
}

export default function UserMultiSelect({
  options,
  selected,
  onChange,
  placeholder = "Seleccionar...",
  searchPlaceholder = "Buscar...",
  emptyMessage = "Sin resultados",
  label,
  filterFn,
}: UserMultiSelectProps) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const filteredOptions = useMemo(
    () =>
      options
        .filter(
          (opt) =>
            opt.label.toLowerCase().includes(search.toLowerCase()) ||
            (opt.subtitle && opt.subtitle.toLowerCase().includes(search.toLowerCase()))
        )
        .filter((opt) => (filterFn ? filterFn(opt) : true)),
    [options, search, filterFn]
  );

  const selectedOptions = useMemo(
    () => options.filter((opt) => selected.includes(opt.id)),
    [options, selected]
  );

  const handleToggle = (id: string) => {
    if (selected.includes(id)) {
      onChange(selected.filter((s) => s !== id));
    } else {
      onChange([...selected, id]);
    }
  };

  const handleRemove = (id: string) => {
    onChange(selected.filter((s) => s !== id));
  };

  return (
    <div className="space-y-2">
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
          {label}
        </label>
      )}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
          <Button
            variant="outline"
            className="w-full justify-start text-left font-normal h-auto min-h-10 py-2"
          >
            {selectedOptions.length > 0 ? (
              <div className="flex flex-wrap gap-1">
                {selectedOptions.map((opt) => (
                  <Badge
                    key={opt.id}
                    variant="secondary"
                    className="mr-1"
                  >
                    {opt.label}
                    <button
                      type="button"
                      className="ml-1 ring-offset-background rounded-full outline-hidden focus:ring-2 focus:ring-ring focus:ring-offset-2"
                      onPointerDown={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                      }}
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        handleRemove(opt.id);
                      }}
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            ) : (
              <span className="text-muted-foreground">{placeholder}</span>
            )}
          </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>{label || placeholder}</DialogTitle>
          </DialogHeader>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder={searchPlaceholder}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
          <ScrollArea className="h-72">
            <div className="space-y-1">
              {filteredOptions.length > 0 ? (
                filteredOptions.map((opt) => (
                  <label
                    key={opt.id}
                    className={cn(
                      "flex items-center gap-3 rounded-md px-3 py-2.5 cursor-pointer transition-colors",
                      selected.includes(opt.id)
                        ? "bg-primary/10 hover:bg-primary/15"
                        : "hover:bg-muted"
                    )}
                  >
                    <Checkbox
                      checked={selected.includes(opt.id)}
                      onCheckedChange={() => handleToggle(opt.id)}
                    />
                    <div className="flex flex-col">
                      <span className="text-sm font-medium">{opt.label}</span>
                      {opt.subtitle && (
                        <span className="text-xs text-muted-foreground">
                          {opt.subtitle}
                        </span>
                      )}
                    </div>
                  </label>
                ))
              ) : (
                <p className="text-center text-sm text-muted-foreground py-8">
                  {emptyMessage}
                </p>
              )}
            </div>
          </ScrollArea>
        </DialogContent>
      </Dialog>
    </div>
  );
}
